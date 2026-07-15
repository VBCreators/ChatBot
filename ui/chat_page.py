import streamlit as st
from services.chat_services.chat_functions import start_new_chat
from ui.actual_chat_module_ui import main_chat_ui



def sidebar():
    with st.sidebar:
        if st.button("Log out"):
            st.session_state.user_is_active = False
            st.rerun()

        st.title("💬 Chat History")

        if st.button("➕ New Chat"):
            start_new_chat()

        st.divider()
        
      


def main_page_body():

    st.set_page_config(page_title="AI Chatbot", layout="wide")
    st.title("💬 Zina AI Assistant")
    
    main_chat_ui()
    

  

def chat_page_ui():
    sidebar()    
    main_page_body()