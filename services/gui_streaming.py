def stream_response_gui(llm, messages, placeholder):

    # Stream LLM response directly into Streamlit chat UI.

    full_response = "Thinking..."
    placeholder.markdown(full_response + "▌")

    response_started = False

    for chunk in llm.stream(messages):
        if not response_started:
            # \033[K is an ANSI escape code that clears the line from the cursor to the end
            placeholder.markdown("\033[K")
            full_response = ""
            response_started = True

        if chunk.content:
            full_response += chunk.content
            placeholder.markdown(full_response + "▌")

    placeholder.markdown(full_response)
    return full_response
