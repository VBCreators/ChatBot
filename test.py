import streamlit as st


st.session_state.setdefault("count", 0)

# if "count" not in st.session_state:
#     st.session_state.count = 0

col1, col2 = st.columns(2)

with col1:
    if st.button("Add 1"):
        st.session_state.count += 1

with col2:
    if st.button("Minus 1"):
        st.session_state.count -= 1

st.write("Count:", st.session_state.count)
