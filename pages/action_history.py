import streamlit as st
from utils.security import enforce_employee_boundary

enforce_employee_boundary()

st.title("📋 Employee Action History & Execution Tracker")
st.info("Log of tasks created, assigned employee IDs, timestamps, and completion statuses.")