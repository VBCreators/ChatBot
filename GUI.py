# External libs
import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

# Internal imports
from config import BOT_NAME
from services.gui_streaming import stream_response_gui
import brain.engine as engine


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

    bot_name = st.text_input("Bot Name", value=BOT_NAME)
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
            role_class = HumanMessage
        else:
            role_class = AIMessage
        langchain_messages.append(role_class(content=msg["content"]))

    # Assistant response block
    with st.chat_message("assistant"):
        message_placeholder = st.empty()

        # CALL THE MODULAR STREAMING FUNCTION
        full_response = stream_response_gui(
            llm, langchain_messages, message_placeholder
        )

    st.session_state.messages.append({"role": "assistant", "content": full_response})
