import streamlit as st





def sidebar():
    with st.sidebar:
        st.title("💬 Chat History")

        if st.button("Log out"):
            st.session_state.user_is_active = False
            st.rerun()


def main_page_body():
    st.header("header part")
    if st.button("trigger message"):
        st.success("msg triggered")
        


def chat_ui():
    st.title("Login success")
    sidebar()    
    main_page_body()