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

        st.warning("Please enter a question first.")

    else:

        if role == "EMPLOYEE":

            if customer_context:

                final_prompt = f"""
You are an insurance Customer 360 AI assistant helping an
authorized insurance employee.

The employee may ask questions about the selected customer,
insurance concepts, policies, claims, payments, interactions,
risk, retention, or business processes.

A specific customer context is available below.

CUSTOMER CONTEXT:
{customer_context}

EMPLOYEE QUESTION:
{user_query}

Instructions:

1. Answer the employee's question directly and precisely.

2. When the question concerns the selected customer, use the
   CUSTOMER CONTEXT as the primary source of truth.

3. Never invent customer-specific facts.

4. If the customer context does not contain enough information
   to answer a customer-specific question, clearly say that the
   required customer data is unavailable.

5. You may use your general insurance knowledge to explain
   insurance concepts, terminology, processes, or implications
   when the question is not asking for a specific customer fact.

6. Clearly distinguish:
   - facts present in the customer data
   - reasonable interpretation
   - general insurance knowledge

7. For numerical or factual customer questions, rely on the
   supplied customer data rather than guessing.

8. Never make up policy numbers, claim amounts, dates, payments,
   customer details, risk scores, or interaction details.

9. Do not reveal information about other customers.

10. If the employee asks something unrelated to the selected
    customer, answer it using general knowledge when possible.

11. Keep the answer concise but provide enough explanation to
    make the answer useful to an insurance employee.

12. If the available information is insufficient, explicitly say
    what information is missing.

Answer the employee now.
"""

            else:

                final_prompt = f"""
You are an insurance Customer 360 AI assistant helping an
authorized insurance employee.

No specific customer has been selected for this question.

EMPLOYEE QUESTION:
{user_query}

Instructions:

1. Answer the employee's question directly and precisely.

2. You may use your general knowledge to answer questions about:
   - insurance concepts
   - insurance terminology
   - claims processes
   - policy concepts
   - customer service
   - retention
   - churn
   - risk concepts
   - general business processes
   - general analytical reasoning

3. Do NOT invent information about customers, policies, claims,
   payments, interactions, employees, or database records.

4. If the employee asks for a specific customer, policy, claim,
   payment, interaction, count, list, or database value that is
   not provided in the current context, clearly state that the
   required application data is unavailable.

5. Do not pretend that you queried Snowflake or the application
   database.

6. Do not fabricate numerical results.

7. Clearly distinguish general knowledge from application data.

8. If the question is ambiguous, explain the ambiguity and answer
   the most reasonable interpretation without inventing facts.

9. Keep the answer concise, professional, and useful.

Answer the employee now.
"""

        else:

            if customer_context:

                final_prompt = f"""
You are an insurance Customer 360 AI assistant.

CUSTOMER EVIDENCE:
{customer_context}

USER QUESTION:
{user_query}

Instructions:

- Answer using the supplied customer evidence when the question
  concerns the customer.
- Do not invent customer facts.
- You may use general insurance knowledge for explanations.
- Clearly distinguish customer facts from general knowledge.
- If required customer evidence is unavailable, say so.
- Never expose information belonging to another customer.
- Keep the answer concise and useful.
"""

            else:

                final_prompt = f"""
You are an insurance AI assistant.

USER QUESTION:
{user_query}

No customer-specific application context is currently available.

Instructions:

- Answer general insurance questions using your knowledge.
- Do not invent customer-specific information.
- Do not fabricate policies, claims, payments, interactions,
  dates, amounts, or database values.
- If the question requires application-specific data that is not
  available, clearly say that the required data is unavailable.
- Keep the answer concise and useful.
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