import streamlit as st

from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from config import BOT_NAME, APP_TITLE
from services.db_services.db_session import get_db_session

from services.db_services.db_crud import (
    create_new_session,
    get_all_sessions,
    get_session_by_id,
    add_message,
    update_session_title,
    delete_session,
)

from services.chat_services.chat_session_mgmt import (
    init_session_state,
    load_chat_into_state,
    start_new_chat,
)

from brain.engine import get_llm, get_ai_personality
from services.gui_streaming import stream_response_gui


st.set_page_config(
    page_title=APP_TITLE,
    layout="wide",
)


# INITIALIZATION
db = get_db_session()
llm = get_llm()
system_prompt = get_ai_personality()
init_session_state()


# CREATE FIRST CHAT IF DATABASE EMPTY
all_sessions = get_all_sessions(db)

if len(all_sessions) == 0:
    first_chat = create_new_session(db, title="New Chat")

    st.session_state.current_session_id = first_chat.session_id


# LOAD CURRENT CHAT IF NOT LOADED
if st.session_state.current_session_id and len(st.session_state.messages) == 0:
    load_chat_into_state(db, st.session_state.current_session_id)


# SIDEBAR


with st.sidebar:
    st.title("💬 Chat History")

    # NEW CHAT BUTTON
    if st.button("➕ New Chat"):
        new_chat = start_new_chat(db)
        st.session_state.current_session_id = new_chat.session_id
        st.rerun()
    st.divider()

    sessions = get_all_sessions(db)

    for session in sessions:
        col1, col2 = st.columns([5, 1])

        # OPEN CHAT

        with col1:
            if st.button(session.title, key=f"open_{session.session_id}"):
                load_chat_into_state(db, session.session_id)

                st.rerun()

        # DELETE CHAT

        with col2:
            if st.button("🗑️", key=f"delete_{session.session_id}"):
                delete_session(db, session.session_id)

                # if currently open chat deleted

                if st.session_state.current_session_id == session.session_id:
                    st.session_state.current_session_id = None

                    st.session_state.messages = []

                st.rerun()

# ==========================================
# MAIN CHAT AREA
# ==========================================

st.title("🤖 AI Assistant")

# ==========================================
# DISPLAY EXISTING CHAT HISTORY
# ==========================================

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ==========================================
# USER INPUT
# ==========================================

prompt = st.chat_input("Type your message...")

if prompt:
    # ======================================
    # SHOW USER MESSAGE
    # ======================================

    with st.chat_message("user"):
        st.markdown(prompt)

    # ======================================
    # ADD TO STREAMLIT MEMORY
    # ======================================

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt,
        }
    )

    # ======================================
    # SAVE USER MESSAGE TO DATABASE
    # ======================================

    add_message(
        db,
        st.session_state.current_session_id,
        "user",
        prompt,
    )

    # ======================================
    # BUILD LANGCHAIN HISTORY
    # ======================================

    langchain_messages = [SystemMessage(content=system_prompt)]

    for msg in st.session_state.messages:
        if msg["role"] == "user":
            langchain_messages.append(HumanMessage(content=msg["content"]))

        else:
            langchain_messages.append(AIMessage(content=msg["content"]))

    # ======================================
    # GENERATE AI RESPONSE
    # ======================================

    with st.chat_message("assistant"):
        placeholder = st.empty()

        full_response = stream_response_gui(
            llm,
            langchain_messages,
            placeholder,
        )

    # ======================================
    # STORE AI RESPONSE IN MEMORY
    # ======================================

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": full_response,
        }
    )

    # ======================================
    # SAVE AI RESPONSE TO DATABASE
    # ======================================

    add_message(
        db,
        st.session_state.current_session_id,
        "assistant",
        full_response,
    )

    # ======================================
    # AUTO GENERATE CHAT TITLE
    # FIRST USER MESSAGE BECOMES TITLE
    # ======================================

    current_chat = get_session_by_id(
        db,
        st.session_state.current_session_id,
    )

    if current_chat.title == "New Chat":
        update_session_title(
            db,
            current_chat.session_id,
            prompt[:40],
        )

    st.rerun()

# ==========================================
# CLEANUP
# ==========================================

db.close()
