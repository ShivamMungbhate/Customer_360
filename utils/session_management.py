import streamlit as st

def init_session_state():
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False
    if "role" not in st.session_state:
        st.session_state["role"] = None
    if "user_email" not in st.session_state:
        st.session_state["user_email"] = None