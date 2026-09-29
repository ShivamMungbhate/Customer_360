import streamlit as st
from services.ai_service import query_local_llm

st.title("🤖 Natural Language AI Assistant")

active_model = st.session_state.get("bg_llm_model", "llama3")
st.caption(f"Running on background model: **{active_model}** (configurable in Settings)")

role = st.session_state.get("role", "CUSTOMER")

if role == "CUSTOMER":
    st.write("👤 Ask questions about your active policies, coverage, or claims.")
    default_prompt = "What are the common causes for a policy renewal delay?"
else:
    st.write("🛡️ Ask complex business queries, risk metrics, or request summaries.")
    default_prompt = "Why might a customer with a pending claim and negative support interaction be flagged as high churn risk?"

user_query = st.text_area("Type your question here:", value=default_prompt)

if st.button("Generate AI Response", type="primary"):
    if user_query:
        with st.spinner(f"Querying model (`{active_model}` via Ollama)..."):
            ai_response = query_local_llm(user_query, model_name=active_model)
            st.markdown("### 💡 AI Response")
            st.markdown(ai_response)
    else:
        st.warning("Please enter a question first.")