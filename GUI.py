import streamlit as st
import time
import brain.engine as engine
from config import BOT_NAME
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

# Initialize the engine components
llm = engine.get_llm()
system_prompt = engine.get_ai_personality()

# --- Sidebar Chat Interface ---
with st.sidebar:
    st.header("Configuration")
    st.write("Set up your chatbot's personality and response style.")

    # Model Settings
    model_option = st.selectbox(
        "Choose a Model", ("gpt-4o", "gpt-3.5-turbo", "Llama-3-Local")
    )

    bot_name = st.text_input("Bot Name", value="Zina")
    company_name = st.text_input("Company Name", value="VB Creators")
    scope = st.text_input("Scope (Domain)", value="Personal Finance")
    reply_size_limit = st.slider(
        "Reply Size Limit (words)", min_value=50, max_value=500, value=300
    )


# --- Page Config ---
st.set_page_config(page_title="AI Chatbot", layout="wide")


# --- Main Chat Interface ---
st.title("💬 Personal AI Assistant")

first_message = (
    f"{BOT_NAME}: Hi! I am {BOT_NAME}, your AI Assistant. How can I help you today?"
)

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": first_message}]

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
prompt = st.chat_input("Type your message...")
if prompt:
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Prepare messages for LangChain
    # We include the System Message + History + Current Prompt
    langchain_messages = [SystemMessage(content=system_prompt)]
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            langchain_messages.append(HumanMessage(content=msg["content"]))
        else:
            langchain_messages.append(AIMessage(content=msg["content"]))

    # Display assistant response with REAL streaming
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        # Using llm.stream to get real-time chunks from Google Generative AI
        for chunk in llm.stream(langchain_messages):
            full_response += chunk.content
            # Add a cursor to simulate typing
            message_placeholder.markdown(full_response + "▌")

        message_placeholder.markdown(full_response)

    # # Display assistant response in chat message container
    # with st.chat_message("assistant"):
    #     message_placeholder = st.empty()
    #     full_response = ""

    #     # --- Logic for Bot Response ---
    #     # (Replace this block with your actual LLM API call)
    #     assistant_response = f"You are using {model_option}. You said: {prompt}"

    #     # Simulate a streaming response
    #     for chunk in assistant_response.split():
    #         full_response += chunk + " "
    #         time.sleep(0.05)
    #         # Add a blinking cursor to simulate typing
    #         message_placeholder.markdown(full_response + "▌")

    #     message_placeholder.markdown(full_response)

    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": full_response})
