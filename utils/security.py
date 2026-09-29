import streamlit as st

def enforce_employee_boundary():
    if st.session_state.get("role") != "EMPLOYEE":
        st.error("Access Denied: Employee privileges required.")
        st.stop()

def enforce_customer_boundary():
    if st.session_state.get("role") != "CUSTOMER":
        st.error("Access Denied: Customer portal restriction.")
        st.stop()