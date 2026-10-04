import streamlit as st

from services.ai_service import (
    query_local_llm,
    generate_customer_ai_summary,
    explain_next_best_action,
)
from services.customer_service import fetch_customer_360
from utils.security import enforce_customer_boundary, enforce_employee_boundary

st.markdown("""
<style>

/* ---------- Global ---------- */

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

.stApp {
    background:
        radial-gradient(
            circle at 8% 5%,
            rgba(59, 130, 246, 0.14),
            transparent 32%
        ),
        radial-gradient(
            circle at 92% 8%,
            rgba(139, 92, 246, 0.13),
            transparent 30%
        ),
        linear-gradient(
            135deg,
            #070b14 0%,
            #0b1220 50%,
            #080d18 100%
        );

    color: #e5e7eb;
    font-family: 'Inter', sans-serif;
}

/* Main content width / spacing */
[data-testid="stMainBlockContainer"] {
    max-width: 1400px;
    padding-top: 2.4rem;
    padding-bottom: 4rem;
}

/* ---------- Header ---------- */

h1 {
    font-size: clamp(2rem, 4vw, 2.8rem) !important;
    font-weight: 800 !important;
    letter-spacing: -1.4px;
    line-height: 1.2 !important;

    background: linear-gradient(
        100deg,
        #ffffff 10%,
        #93c5fd 55%,
        #c4b5fd 90%
    );

    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;

    margin-bottom: 0.7rem !important;
}

h2 {
    color: #f8fafc !important;
    font-weight: 750 !important;
    letter-spacing: -0.5px;
}

h3 {
    color: #e2e8f0 !important;
    font-weight: 700 !important;
}

p {
    color: #b8c4d6;
    line-height: 1.65;
}

[data-testid="stCaptionContainer"] {
    color: #7f8da3;
}

/* ---------- Customer context expander ---------- */

[data-testid="stExpander"] {
    background:
        linear-gradient(
            145deg,
            rgba(20, 31, 52, 0.92),
            rgba(12, 20, 35, 0.92)
        );

    border: 1px solid rgba(96, 165, 250, 0.20);
    border-radius: 18px;
    box-shadow:
        0 12px 35px rgba(0, 0, 0, 0.16),
        inset 0 1px 0 rgba(255, 255, 255, 0.025);

    overflow: hidden;
    transition: all 0.25s ease;
}

[data-testid="stExpander"]:hover {
    border-color: rgba(96, 165, 250, 0.38);
    box-shadow:
        0 16px 42px rgba(0, 0, 0, 0.22),
        0 0 25px rgba(59, 130, 246, 0.05);
}

[data-testid="stExpander"] summary {
    color: #e2e8f0 !important;
    font-weight: 650 !important;
    font-size: 0.96rem;
    padding: 0.8rem 0.3rem;
}

/* ---------- Metric cards ---------- */

[data-testid="stMetric"] {
    background:
        linear-gradient(
            145deg,
            rgba(25, 39, 65, 0.95),
            rgba(14, 23, 40, 0.95)
        );

    border: 1px solid rgba(96, 165, 250, 0.18);
    border-radius: 15px;

    padding: 18px 18px;

    box-shadow:
        0 8px 25px rgba(0, 0, 0, 0.15),
        inset 0 1px 0 rgba(255, 255, 255, 0.025);

    transition:
        transform 0.2s ease,
        border-color 0.2s ease,
        box-shadow 0.2s ease;
}

[data-testid="stMetric"]:hover {
    transform: translateY(-3px);

    border-color: rgba(96, 165, 250, 0.48);

    box-shadow:
        0 12px 32px rgba(0, 0, 0, 0.22),
        0 0 20px rgba(59, 130, 246, 0.06);
}

[data-testid="stMetricLabel"] {
    color: #94a3b8 !important;
    font-size: 0.78rem !important;
    font-weight: 600 !important;
    text-transform: uppercase;
    letter-spacing: 0.45px;
}

[data-testid="stMetricValue"] {
    color: #f8fafc !important;
    font-size: 1.8rem !important;
    font-weight: 800 !important;
}

/* ---------- Customer ID info box ---------- */

[data-testid="stAlert"] {
    border-radius: 13px;
    border: 1px solid rgba(96, 165, 250, 0.22);
    background: rgba(30, 64, 175, 0.10);
    color: #dbeafe;
}

/* ---------- Text area ---------- */

.stTextArea textarea {
    background:
        linear-gradient(
            145deg,
            #111b2e,
            #0e1727
        ) !important;

    color: #f1f5f9 !important;

    border: 1px solid #334155 !important;
    border-radius: 15px !important;

    padding: 16px 17px !important;

    font-family: 'Inter', sans-serif !important;
    font-size: 0.96rem !important;
    line-height: 1.6 !important;

    box-shadow:
        inset 0 1px 2px rgba(0, 0, 0, 0.18);
    
    transition:
        border-color 0.2s ease,
        box-shadow 0.2s ease;
}

.stTextArea textarea:focus {
    border-color: #60a5fa !important;

    box-shadow:
        0 0 0 3px rgba(59, 130, 246, 0.12),
        0 8px 25px rgba(0, 0, 0, 0.12) !important;
}

.stTextArea textarea::placeholder {
    color: #64748b !important;
}

/* Text area label */
.stTextArea label {
    color: #cbd5e1 !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
}

/* ---------- Generate button ---------- */

.stButton > button {
    min-height: 48px;

    border-radius: 12px;

    border: 1px solid rgba(147, 197, 253, 0.28);

    background:
        linear-gradient(
            110deg,
            #2563eb 0%,
            #4f46e5 55%,
            #7c3aed 100%
        );

    color: #ffffff !important;

    font-family: 'Inter', sans-serif;
    font-size: 0.94rem;
    font-weight: 700;

    letter-spacing: 0.1px;

    box-shadow:
        0 7px 22px rgba(37, 99, 235, 0.20);

    transition:
        transform 0.2s ease,
        box-shadow 0.2s ease,
        filter 0.2s ease;
}

.stButton > button:hover {
    filter: brightness(1.08);

    transform: translateY(-2px);

    box-shadow:
        0 10px 28px rgba(59, 130, 246, 0.32);

    border-color: rgba(191, 219, 254, 0.55);
}

.stButton > button:active {
    transform: translateY(0) scale(0.985);
}

/* ---------- AI Response ---------- */

/*
    The response itself remains normal Streamlit markdown.
    This styling makes the area around the response cleaner
    without changing the AI output.
*/

h3 {
    margin-top: 1.8rem !important;
}

/* Response markdown */
[data-testid="stMarkdownContainer"] {
    color: #d5deeb;
}

[data-testid="stMarkdownContainer"] strong {
    color: #f8fafc;
}

[data-testid="stMarkdownContainer"] code {
    color: #93c5fd;
    background: rgba(30, 41, 59, 0.75);
    border: 1px solid rgba(96, 165, 250, 0.14);
    border-radius: 6px;
    padding: 2px 6px;
}

/* AI response lists */
[data-testid="stMarkdownContainer"] ul,
[data-testid="stMarkdownContainer"] ol {
    padding-left: 1.5rem;
}

[data-testid="stMarkdownContainer"] li {
    color: #cbd5e1;
    margin-bottom: 0.35rem;
}

/* AI response blockquotes */
[data-testid="stMarkdownContainer"] blockquote {
    border-left: 3px solid #6366f1;
    background: rgba(79, 70, 229, 0.08);
    border-radius: 0 10px 10px 0;
    padding: 10px 15px;
    color: #cbd5e1;
}

/* ---------- Spinner ---------- */

[data-testid="stSpinner"] {
    color: #93c5fd;
}

/* ---------- Horizontal spacing ---------- */

hr {
    border-color: rgba(100, 116, 139, 0.22) !important;
}

/* ---------- Responsive ---------- */

@media (max-width: 768px) {

    [data-testid="stMainBlockContainer"] {
        padding: 1.3rem 1rem 2.5rem;
    }

    h1 {
        font-size: 1.85rem !important;
        letter-spacing: -0.8px;
    }

    [data-testid="stMetric"] {
        padding: 14px;
    }

    [data-testid="stExpander"] {
        border-radius: 14px;
    }

    .stButton > button {
        min-height: 45px;
    }
}



@media (prefers-reduced-motion: reduce) {

    *,
    *::before,
    *::after {
        transition: none !important;
        animation: none !important;
    }
}

</style>
""", unsafe_allow_html=True)

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