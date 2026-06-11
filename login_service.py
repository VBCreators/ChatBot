import streamlit as st
from services.db_services.db_session import get_db_session
from services.db_services.db_crud import get_all_sessions

USERS = {
    "bhargav" : "bhargav123",
    "vrushu" : "vrushu123"
}

def login_screen():
    st.title("Please Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type = "password")

    if st.button("Log in"):
        if USERS.get(username) == password:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.rerun()
        else:
            st.error("Invalid username or password")

session = get_db_session()
value = get_all_sessions(session)

for i, v in enumerate(value):
    st.write(f"{i} time is {v.created_at} session id {v.session_id} with msg {v.messages}  -----")


def main_app():
     st.title(f"welcome {st.session_state.username}")
     if st.button("log out"):
         st.session_state.logged_in = False
         st.rerun()

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if st.session_state.logged_in:
    main_app()
else:
    login_screen()


