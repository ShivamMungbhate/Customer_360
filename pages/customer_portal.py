import streamlit as st
from utils.security import enforce_customer_boundary
from services.ai_service import query_local_llm

enforce_customer_boundary()


user_email = st.session_state.get("user_email", "customer@insurance.com")
customer_name = "Rahul" if "customer" in user_email else user_email.split("@")[0].capitalize()

st.markdown(f"### Welcome back, {customer_name} 👋")
st.markdown("---")


st.markdown("#### 🛡️ My Policies &nbsp;&nbsp;&nbsp; `2 Active`")

col_p1, col_p2 = st.columns(2)

with col_p1:
    with st.container(border=True):
        st.markdown("##### Health Insurance")
        st.markdown("Status: **Active**")
        st.caption("Renewal: 12 Dec 2026")

with col_p2:
    with st.container(border=True):
        st.markdown("##### Car Insurance")
        st.markdown("Status: **Active**")
        st.caption("Renewal: 05 Feb 2027")

st.markdown("---")


st.markdown("#### 📑 My Claims")

with st.container(border=True):
    col_c1, col_c2, col_c3 = st.columns([1, 2, 1])
    with col_c1:
        st.markdown("**`CLM1023`**")
    with col_c2:
        st.markdown("Vehicle Damage")
    with col_c3:
        st.markdown("🟡 **In Progress**")

st.markdown("---")


st.markdown("#### 🤖 Ask AI")
default_question = "What is the status of my claim?"
user_query = st.text_input("Type your question below:", value=default_question)

active_model = st.session_state.get("bg_llm_model", "llama3")

if st.button("Ask", type="primary"):
    if user_query:
        with st.spinner(f"Querying local model (`{active_model}`)..."):
            
            prompt = f"The customer is asking: '{user_query}'. Context: The customer has active Health and Car insurances, and 1 active claim CLM1023 for Vehicle Damage which is currently In Progress. Provide a concise, helpful answer."
            response = query_local_llm(prompt, model_name=active_model)
            
            st.markdown("### 💡 AI Assistant Response")
            st.success(response)
    else:
        st.warning("Please enter a question first.")