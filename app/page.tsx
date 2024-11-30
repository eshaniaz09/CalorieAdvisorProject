"use client";

import { useState } from 'react';

// Define the Message type
interface Message {
  type: 'user' | 'bot';
  text: string;
}

const ChatPage = () => {
  const [input, setInput] = useState('');
  const [messages, setMessages] = useState<Message[]>([]);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);

    // Add user's message to the chat
    const newMessage: Message = { type: 'user', text: input };
    setMessages((prev) => [...prev, newMessage]);

    try {
      // Adjusted fetch request to match backend setup
      const response = await fetch('http://127.0.0.1:8000/generateanswer', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: input }), // Update key to "message"
      });

      if (!response.ok) {
        throw new Error('Network response was not ok');
      }

      const data = await response.json();
      // Access bot response from the `data.response` structure
      const botResponse: Message = { type: 'bot', text: JSON.stringify(data.response) };
      setMessages((prev) => [...prev, botResponse]);
    } catch (error) {
      console.error('Error fetching response:', error);
      const errorMessage: Message = { type: 'bot', text: 'Error generating response. Please try again.' };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setLoading(false);
      setInput('');
    }
  };

  return (
    <div
      className="flex flex-col items-center justify-center min-h-screen bg-cover bg-center py-8"
      style={{ backgroundImage: 'url(/newBg.jpg)' }}
    >
      <div className="text-center">
        <section className="mb-6 max-w-3xl">
          <h1 className="text-6xl font-bold text-white">Nutrition AI</h1>
          <h6 className="text-lg text-white">Your personal nutritionist</h6>
        </section>

        <section className="w-full max-w-3xl mb-6">
          <div className="bg-white bg-opacity-20 backdrop-blur-md border border-gray-300 rounded-lg p-6 h-96 overflow-y-auto flex flex-col">
            {messages.map((msg, index) => (
              <div
                key={index}
                className={`my-2 p-2 rounded-lg ${msg.type === 'user'
                  ? 'bg-red-600 bg-opacity-80 backdrop-blur-md text-white self-end'
                  : 'bg-gray-200 text-black self-start'
                  }`}
              >
                {msg.text}
              </div>
            ))}
          </div>
          <label className="block mt-2 text-left text-white">What is your goal?</label>
        </section>

        <section className="flex flex-col w-full max-w-3xl">
          <form onSubmit={handleSubmit} className="flex flex-col">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              className="p-2 border border-gray-300 rounded-lg mb-2"
              placeholder="Please provide your age, weight, height, gender, and activity level:"
              required
            />
            <button
              type="submit"
              className={`p-2 rounded-lg flex items-center justify-center ${loading ? 'bg-gray-500' : 'bg-red-600 hover:bg-red-700'} text-white`}
              disabled={loading}
            >
              {loading ? (
                <svg
                  className="animate-spin h-5 w-5 text-white"
                  xmlns="http://www.w3.org/2000/svg"
                  viewBox="0 0 24 24"
                >
                  <circle
                    className="opacity-25"
                    cx="12"
                    cy="12"
                    r="10"
                    fill="none"
                    stroke="currentColor"
                    strokeWidth="4"
                  />
                  <path
                    className="opacity-75"
                    fill="currentColor"
                    d="M4 12a8 8 0 0016 0H4z"
                  />
                </svg>
              ) : (
                "Create Nutrition Plan"
              )}
            </button>
          </form>
        </section>
      </div>
    </div>
  );
};

export default ChatPage;
