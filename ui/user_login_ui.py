import streamlit as st
from services.auth_services.user_login_mgmt import check_user_login
from ui.user_signup_ui import signup_screen


def login_screen():
    st.title("Please Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type = "password")

  
    if st.button("Log in"):
       
        if check_user_login(username, password):
            return True
        else:
            st.error("Invalid username or password")
    
    if st.button("Sign up"):
        st.session_state.page = "user_signup_page"
        st.rerun()
    
    return False