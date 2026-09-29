import streamlit as st
from utils.security import enforce_employee_boundary

enforce_employee_boundary()

st.title("🔍 Customer 360 & Explainable Insights")

customer_id_input = st.text_input("Enter Customer ID for Deep Dive", "CUST-1001")

if customer_id_input:
    col_a, col_b = st.columns([2, 1])
    
    with col_a:
        st.subheader("Customer Profile & Overview")
        st.write(f"Viewing profile details for **{customer_id_input}**")
        
        st.markdown("### 📑 Policies & Claims Summary")
        st.info("Policies, Claims, and Payment records table placeholder.")
        
    with col_b:
        st.subheader("🧠 AI Insights & Explainability")
        st.warning("⚠️ High Churn Risk Detected")
        st.markdown("""
        **Why is this customer high risk?**
        * Policy renewal is within 15 days
        * Latest interaction shows negative sentiment
        * Customer complained about premium increase
        """)