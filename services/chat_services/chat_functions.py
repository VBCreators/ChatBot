import streamlit as st
import brain.engine as engine
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from services.gui_streaming import stream_response_gui

def start_new_chat():
    st.success("new chat")



def ai_response(message_placeholder):
    
    # Initialize the engine components
    llm = engine.get_llm()
    system_prompt = engine.get_ai_personality()

    langchain_messages = [SystemMessage(content=system_prompt)]
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            role_class = HumanMessage
        else:
            role_class = AIMessage
        langchain_messages.append(role_class(content=msg["content"]))

    full_response = stream_response_gui(llm, langchain_messages, message_placeholder)

    return full_response