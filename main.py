# from brain.engine import chatbot_response
import app.streaming as streaming
import brain.engine as engine
from langchain_core.messages import HumanMessage, SystemMessage
from config import BOT_NAME


def main():

    # Initialize the engine components
    llm = engine.get_llm()
    system_prompt = engine.get_ai_personality()

    print(
        f"{BOT_NAME}: Hi! I am {BOT_NAME}, your AI Assistant. How can I help with you today?"
    )
    print(f"{BOT_NAME}: Type 'exit' to quit.")

    while True:
        user_input = input("\nYou: ")
        if user_input.lower() in ["exit", "quit", "bye"]:
            print(f"{BOT_NAME}: Goodbye!")
            break

        # Adding a reminder for response length
        user_input = user_input + " Please keep the response under 300 words."

        # Construct the context for the LLM
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_input),
        ]

        # Call the modular streaming function
        streaming.stream_response(llm, messages)


if __name__ == "__main__":
    main()
