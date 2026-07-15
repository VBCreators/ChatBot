import streamlit as st
from config import BOT_NAME
from services.chat_services.chat_functions import ai_response


def main_chat_ui():
    
    first_message = (
    f"{BOT_NAME}: Hi! I am {BOT_NAME}, your AI Assistant. How can I help you today?"
    )
    
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": first_message}]

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    prompt = st.chat_input("Type your message...")

    if prompt:
    
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)
            st.session_state.messages.append({"role": "user", "content": prompt})


        with st.chat_message("assistant"):
            message_placeholder = st.empty()

            full_response = ai_response(message_placeholder)

        #     full_response = stream_response_gui(
        #     llm, langchain_messages, message_placeholder
        # )

        st.session_state.messages.append({"role": "assistant", "content": full_response})
