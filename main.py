from langchain.agents import AgentExecutor
from langchain.agents import create_tool_calling_agent
from langchain_google_genai import ChatGoogleGenerativeAI,GoogleGenerativeAIEmbeddings
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.tools.retriever import create_retriever_tool
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain import hub
from langchain.tools import tool
import os
from dotenv import load_dotenv

load_dotenv()

llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash",
                         google_api_key=os.getenv("GOOGLE_API_KEY"))

search = TavilySearchResults(tavily_api_key=os.getenv("TAVILY_API_KEY"))

loader = WebBaseLoader("https://www.healthline.com/nutrition/1500-calorie-diet#foods-to-eat")
docs = loader.load()
documents = RecursiveCharacterTextSplitter(
    chunk_size=1000, chunk_overlap=200
).split_documents(docs)
vector = FAISS.from_documents(documents, GoogleGenerativeAIEmbeddings(model="models/embedding-001"))

retriever = vector.as_retriever()

retriever_tool = create_retriever_tool(
    retriever,
    "healthline_search",
    "Search for information about healthline, food and nutrition. For any questions about food and nutrition, healthy diet related and just answer the question don't explain much, you must use this tool!",
)

@tool
def calorie_and_diet_plan() -> dict:
    """Prompt the user for age, weight, height, gender, and activity level, then calculate calories and generate a diet plan."""
    # Step 1: Collect user information
    age = input("Please enter your age: ")
    weight_input = input("Please enter your weight (e.g., 70 kg or 154 lbs): ")
    height_input = input("Please enter your height (e.g., 175 cm or 69 in): ")
    gender = input("Please enter your gender (male/female): ").strip().lower()
    activity_level = input("Please enter your activity level (sedentary, lightly active, moderately active, very active, super active): ").strip().lower()

    # Step 2: Calculate calories
    try:
        data = [age, weight_input, height_input, gender, activity_level]

        if len(data) != 5:
            return {
                "error": "Invalid input. Please provide five values (age, weight, height, gender, and activity level)."
            }

        age = float(data[0])
        weight_input = data[1].strip()
        height_input = data[2].strip()
        gender = data[3].strip().lower()
        activity_level = data[4].strip().lower()

        # Detecting units for weight and height
        if weight_input[-2:].lower() == 'kg':
            weight = float(weight_input[:-2])
        elif weight_input[-3:].lower() == 'lbs':
            weight = float(weight_input[:-3]) * 0.453592  # Convert lbs to kg
        else:
            return {
                "error": "Weight must be in kg or lbs."
            }

        if height_input[-2:].lower() == 'cm':
            height = float(height_input[:-2])
        elif height_input[-2:].lower() == 'in':
            height = float(height_input[:-2]) * 2.54  # Convert inches to cm
        else:
            return {
                "error": "Height must be in cm or in."
            }

        activity_multipliers = {
            "sedentary": 1.2,
            "lightly active": 1.375,
            "moderately active": 1.55,
            "very active": 1.725,
            "super active": 1.9,
        }

        if activity_level not in activity_multipliers:
            return {
                "error": "Invalid activity level. Please choose from: sedentary, lightly active, moderately active, very active, or super active."
            }

        if gender in ["male", "men"]:
            base_result = 10 * weight + 6.25 * height - 5 * age + 5
        elif gender in ["female", "women"]:
            base_result = 10 * weight + 6.25 * height - 5 * age - 161
        else:
            return {
                "error": "Gender must be either 'male' or 'female'."
            }

        # Apply activity multiplier
        calories = base_result * activity_multipliers[activity_level]

    except (ValueError, IndexError):
        return {
            "error": "No valid numbers found or insufficient input."
        }

    # Step 3: Ask follow-up questions for diet planning
    questions = [
        "What are your current eating habits like? (e.g., Do you eat breakfast? How often do you eat out?)",
        "What are your favorite foods? (This helps me create a plan you'll actually enjoy!)",
        "Do you have any dietary restrictions or allergies? (e.g., gluten-free, vegetarian, lactose intolerant)",
        "What is your weight loss goal? (e.g., 1-2 pounds per week)"
    ]

    answers = {}
    for question in questions:
        answer = input(question + "\n")
        answers[question] = answer

    # Step 4: Generate diet plan based on calorie count and user answers
    diet_plan = {
        "caloric_needs": calories,
        "meals": {
            "breakfast": [],
            "lunch": [],
            "dinner": [],
            "snacks": []
        },
        "exercise": []
    }

    # Create a diet plan
    if calories > 2000:
        diet_plan["meals"]["breakfast"].append("Oatmeal with fruits")
        diet_plan["meals"]["lunch"].append("Grilled chicken salad")
        diet_plan["meals"]["dinner"].append("Quinoa with steamed vegetables")
        diet_plan["meals"]["snacks"].append("Nuts or yogurt")
        diet_plan["exercise"].append("30 minutes of jogging")
    else:
        diet_plan["meals"]["breakfast"].append("Smoothie with spinach and banana")
        diet_plan["meals"]["lunch"].append("Lentil soup with whole-grain bread")
        diet_plan["meals"]["dinner"].append("Baked salmon with asparagus")
        diet_plan["meals"]["snacks"].append("Carrot sticks with hummus")
        diet_plan["exercise"].append("30 minutes of brisk walking")

    if answers.get("What are your favorite foods?"):
        favorite_foods = answers["What are your favorite foods?"].split(',')
        diet_plan["meals"]["lunch"].extend(favorite_food.strip() for favorite_food in favorite_foods)

    return {
        "calories": calories,
        "diet_plan": diet_plan
    }


tools = [calorie_and_diet_plan, search, retriever_tool]

prompt = hub.pull("hwchase17/openai-functions-agent")

agent = create_tool_calling_agent(llm, tools, prompt)

agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

message_history = ChatMessageHistory()

agent_with_chat_history = RunnableWithMessageHistory(
    agent_executor,
    # This is needed because in most real world scenarios, a session id is needed
    # It isn't really used here because we are using a simple in memory ChatMessageHistory
    lambda session_id: message_history,
    input_messages_key="input",
    history_messages_key="chat_history",
)

while True:
    agent_with_chat_history.invoke(
        {"input": input("How can I help you today? : ")},
        config={"configurable": {"session_id": "test123"}},
    )