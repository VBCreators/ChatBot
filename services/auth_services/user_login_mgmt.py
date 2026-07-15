import streamlit as st


def check_user_login(username : str, password: str):
    
    USERS = {
        "bhargav" : "bhargav123",
        "vrushu" : "vrushu123"
    }

    if USERS.get(username) == password :
        return True
    else :
        return False 


