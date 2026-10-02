import streamlit as st

from services.ai_service import (
    query_local_llm,
    generate_customer_ai_summary,
    explain_next_best_action,
)
from services.customer_service import fetch_customer_360
from utils.security import enforce_customer_boundary, enforce_employee_boundary


st.title("🤖 Natural Language AI Assistant")

role = str(
    st.session_state.get("role", "CUSTOMER")
).upper()

# Use the Snowflake Cortex model that is confirmed to work
# in this project/account.
active_model = st.session_state.get(
    "bg_llm_model",
    "llama3.1-8b",
)

if role == "CUSTOMER":
    enforce_customer_boundary()
else:
    enforce_employee_boundary()


customer_id = st.session_state.get("customer_id")

customer_context = None
customer_360 = None

if customer_id:
    customer_360 = fetch_customer_360(customer_id)

    if customer_360:
        summary = customer_360["summary"]

        customer_context = f"""
Customer ID: {customer_360["customer_id"]}
Customer Name: {customer_360["customer_name"]}

Customer Summary:
- Total policies: {summary["total_policies"]}
- Active policies: {summary["active_policies"]}
- Total claims: {summary["total_claims"]}
- Open claims: {summary["open_claims"]}
- Total payments: {summary["total_payments"]}
- Total interactions: {summary["total_interactions"]}
- AI insights available: {summary["total_ai_insights"]}
"""

if role == "CUSTOMER":

    st.write(
        "👤 Ask questions about your policies, coverage, claims, "
        "payments, and recent interactions."
    )

    if customer_id:
        st.info(
            f"AI context is restricted to your customer record: "
            f"`{customer_id}`"
        )

    default_prompt = (
        "Summarize my current insurance situation "
        "and tell me what I should pay attention to."
    )

else:

    st.write(
        "🛡️ Ask business questions about customers, risk signals, "
        "interactions, and recommended actions."
    )

    default_prompt = (
        "Why might a customer with a pending claim and "
        "negative support interaction be flagged as high churn risk?"
    )

if customer_360:

    with st.expander("📊 Customer Context Used by AI"):

        summary = customer_360["summary"]

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "Policies",
                summary["total_policies"],
            )

        with col2:
            st.metric(
                "Open Claims",
                summary["open_claims"],
            )

        with col3:
            st.metric(
                "Payments",
                summary["total_payments"],
            )

        with col4:
            st.metric(
                "Interactions",
                summary["total_interactions"],
            )

user_query = st.text_area(
    "Type your question here:",
    value=default_prompt,
    height=120,
)


if st.button(
    "Generate AI Response",
    type="primary",
    use_container_width=True,
):

    if not user_query.strip():

        st.warning(
            "Please enter a question first."
        )

    else:

        if customer_context:

            final_prompt = f"""
You are an insurance Customer 360 AI assistant.

Answer the user's question using ONLY the customer evidence
provided below.

CUSTOMER EVIDENCE:
{customer_context}

USER QUESTION:
{user_query}

Rules:
- Do not invent customer facts.
- If the available evidence does not answer the question,
  clearly say that the required data is unavailable.
- Separate observed facts from interpretation.
- Keep the response concise and useful.
- Do not expose private information belonging to another customer.
"""

        else:

            final_prompt = f"""
You are an insurance AI assistant.

Answer the following question using only information
available in the application context.

USER QUESTION:
{user_query}

Rules:
- Do not invent facts.
- If evidence is unavailable, say UNKNOWN or
  that the required data is unavailable.
- Keep the answer concise and evidence-based.
"""

        with st.spinner(
            f"Generating response using `{active_model}`..."
        ):

            ai_response = query_local_llm(
                final_prompt,
                model_name=active_model,
            )

        st.markdown("### 💡 AI Response")
        st.markdown(ai_response)

if customer_360:

    st.markdown("---")

    st.subheader("🧠 Customer 360 Summary")

    if st.button(
        "Generate Customer Summary",
        use_container_width=True,
    ):

        with st.spinner("Generating evidence-based summary..."):

            summary_response = generate_customer_ai_summary(
                customer_context,
                model_name=active_model,
            )

        st.markdown(summary_response)

if role == "EMPLOYEE" and customer_360:

    st.markdown("---")

    st.subheader("⚡ Explain a Next Best Action")

    recommended_action = st.text_input(
        "Recommended action",
        placeholder="Example: Schedule renewal retention call",
    )

    if st.button(
        "Explain Recommendation",
        use_container_width=True,
    ):

        if not recommended_action.strip():

            st.warning(
                "Enter a recommended action first."
            )

        else:

            with st.spinner(
                "Analyzing recommendation evidence..."
            ):

                explanation = explain_next_best_action(
                    customer_context=customer_context,
                    recommended_action=recommended_action,
                    model_name=active_model,
                )

            st.markdown("### 🔎 Recommendation Explanation")
            st.markdown(explanation)


if not customer_360 and role == "CUSTOMER":

    st.warning(
        "Customer context is currently unavailable. "
        "AI responses will not invent customer information."
    )
