from langchain_google_genai import GoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.tools import tool
from langchain_core.runnables import RunnableSequence
from dotenv import load_dotenv
import os

load_dotenv()

llm = GoogleGenerativeAI(
    model="gemini-1.5-flash",
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

prompt_template = PromptTemplate(
    template="You are a tool caller: You have to call the tool named calorie_count in case any addition and subtraction is required. Please don't send any explanation while calling the function, just send three numbers, gender, and activity level that the user provided in a comma. e.g., 5, 2, 3, male, sedentary. If a condition exists in a function to check the gender and activity level, use the result according to that. After the follow-up questions, you will provide the diet plan based on the calorie count and question answers. Even if the user has sent a sentence, you have to find three numbers, gender, and activity level, then pass them to the function. User input is {input}\n.",
    inputVariable=["input"]
)

@tool
def calorie_and_diet_plan(user_input: str) -> dict:
    """Calculate calories based on user input and generate a diet plan."""
    # Step 1: Calculate calories
    try:
        data = user_input.split(",")
        if len(data) != 5:
            return {
                "error": "Invalid input. Please provide three numbers (age, weight, height), gender, and activity level."
            }

        age, weight, height, gender, activity_level = (
            float(data[0]),
            float(data[1]),
            float(data[2]),
            data[3].strip().lower(),
            data[4].strip().lower(),
        )

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

    # Step 2: Ask follow-up questions
    questions = [
        "What are your current eating habits like? (e.g., Do you eat breakfast? How often do you eat out?)",
        "What are your favorite foods? (This helps me create a plan you'll actually enjoy!)",
        "What are your activity levels like? (Are you sedentary, moderately active, or very active?)",
        "Do you have any dietary restrictions or allergies? (e.g., gluten-free, vegetarian, lactose intolerant)",
        "What is your weight loss goal? (e.g., 1-2 pounds per week)"
    ]

    answers = {}
    for question in questions:
        answer = input(question + "\n")
        answers[question] = answer

    # Step 3: Generate diet plan based on calorie count and user answers
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

chain = RunnableSequence(
    prompt_template,
    llm,
    calorie_and_diet_plan,
)

while True:
    user_input = input("Please provide me the age, weight, height, gender, and activity level: ")
    calorie_output = chain.invoke(user_input)
    print("Calorie Calculation Output:", calorie_output)