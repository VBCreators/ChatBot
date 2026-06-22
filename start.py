import streamlit as st
# from services.db_services.db_session import get_db_session
# from services.db_services.db_crud import get_all_sessions

from ui.user_login_ui import login_screen
from ui.chat_page import chat_page_ui
from ui.user_signup_ui import signup_screen


# session = get_db_session()
# value = get_all_sessions(session)

# for i, v in enumerate(value):
#     st.write(f"{i} time is {v.created_at} session id {v.session_id} with msg {v.messages}  -----")


def main():

    if "page" not in st.session_state:
        st.session_state.page = "user_login_page"

    if st.session_state.page == "user_login_page" :

        if "user_is_active" not in st.session_state:
            st.session_state.user_is_active = False

        if not st.session_state.user_is_active :
            login_result = login_screen()
            
            if login_result :
                st.session_state.user_is_active = True
                st.rerun()
                            
        else  :
            chat_page_ui()

    elif st.session_state.page == "user_signup_page" :
        signup_screen()

        

        



if __name__ == "__main__":
    main()

    

        
        

