import streamlit as st

from services.auth_services.user_signup_mgmt import check_user_signup, check_password_match

def signup_screen():

    st.title("Signup Page")
        
    user_name = st.text_input("Enter User name")
    user_password = st.text_input("Enter Password", type="password")
    re_user_password = st.text_input("Retype Password", type="password")

    if st.button("Submit"):
       
        if not check_password_match(user_password, re_user_password) :
            st.error("Passwrord and Re-Typed PAssword dont match")
        
        else :
            
            if not check_user_signup(user_name, user_password) :
                st.error("Login Failed")
            
            else :
                st.success("Login Success")

            


    
    if st.button("Cancel"):
        st.session_state.page = "user_login_page"
        st.rerun()


    