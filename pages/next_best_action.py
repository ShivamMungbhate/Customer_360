import streamlit as st
from utils.security import enforce_employee_boundary

enforce_employee_boundary()

st.title("⚡ Next Best Action (NBA) Engine")
st.write("AI-driven and rule-based recommendations for customer retention, claims support, and payment follow-ups.")
st.info("NBA recommendations table and action trigger buttons placeholder.")