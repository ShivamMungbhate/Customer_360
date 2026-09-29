import streamlit as st
from utils.security import enforce_employee_boundary

enforce_employee_boundary()

st.title("💬 Interactions & Unstructured AI Parser")
st.write("Review call transcripts and AI-extracted structured insights (Sentiment, Intent, Churn Signal, Urgency).")
st.info("Transcript viewer and NLP transformation monitor placeholder.")