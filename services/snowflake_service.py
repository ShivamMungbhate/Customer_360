import streamlit as st
from utils.security import enforce_employee_boundary

enforce_employee_boundary()

st.title("⚙️ System & Data Quality Health Dashboard")
col1, col2, col3 = st.columns(3)
col1.metric("Total Customers", "1,500")
col2.metric("Missing Transcripts", "14")
col3.metric("Conflicting Signals", "3")