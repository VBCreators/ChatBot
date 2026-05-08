import spacy


def chatbot_response(user_input):
    nlp = spacy.load("en_core_web_md")
    doc = nlp(user_input.lower())

    # Check for 'weather' as a concept, not just a string
    for token in doc:
        if token.lemma_ == "weather":
            return "I don't have a window, but it feels like 22°C in the cloud."

    # Check for greeting entities or patterns
    if any(token.text in ["hi", "hello", "hey"] for token in doc):
        return "Greetings, human!"

    return "I'm still learning. can you ask about weather instead?"


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
