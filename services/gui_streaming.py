def stream_response_gui(llm, messages, placeholder):

    # Stream LLM response directly into Streamlit chat UI.

    full_response = ""

    for chunk in llm.stream(messages):
        if chunk.content:
            full_response += chunk.content
            placeholder.markdown(full_response + "▌")

    placeholder.markdown(full_response)
    return full_response
