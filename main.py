# from brain.engine import chatbot_response
import app.streaming as streaming
import brain.engine as engine
from langchain_core.messages import HumanMessage, SystemMessage


def main():

    # Initialize the engine components
    llm = engine.get_llm()
    system_prompt = engine.get_ai_personality()

    print("Zina: Hi! I am Zina. Your AI Assistant. How can I help with you today?")
    print("Zina: Type 'exit' to quit.")

    while True:
        user_input = input("\nYou: ")
        if user_input.lower() in ["exit", "quit", "bye"]:
            print("Zina: Goodbye!")
            break

        # Construct the context for the LLM
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_input),
        ]

        # Call the modular streaming function
        streaming.stream_response(llm, messages)


if __name__ == "__main__":
    main()
