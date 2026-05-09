import os

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI


def chatbot_response(user_input):

    # 1. Load the variables from the .env file into the system environment
    load_dotenv()

    # 2. Access the variable (LangChain often looks for GOOGLE_API_KEY automatically)
    api_key = os.getenv("GOOGLE_API_KEY")

    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", google_api_key=api_key)

    response = llm.invoke(user_input)
    return response.content


def main():
    print("Chatbot: Hello! Type 'exit' to quit.")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit", "bye"]:
            print("Chatbot: Goodbye!")
            break
        response = chatbot_response(user_input)
        print(f"Chatbot: {response}")


if __name__ == "__main__":
    main()
