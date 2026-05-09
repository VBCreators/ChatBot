import sys


def stream_response(llm, messages):
    """Handles the terminal output logic for streaming responses."""
    # Show initial loading state
    print("Fin-Buddy: Thinking...", end="\r", flush=True)

    response_started = False

    # Iterate through chunks provided by the LLM
    for chunk in llm.stream(messages):
        if not response_started:
            # \033[K is an ANSI escape code that clears the line from the cursor to the end
            sys.stdout.write("\033[K")
            print("Fin-Buddy: ", end="")
            response_started = True

        content = chunk.content
        print(content, end="", flush=True)

    # Print a new line once the stream is finished
    print()
