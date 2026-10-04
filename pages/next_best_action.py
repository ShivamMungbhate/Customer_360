
import streamlit as st
import pandas as pd

from utils.security import enforce_employee_boundary
from services.ai_service import explain_next_best_action

from services.snowflake_service import (
    get_all_customers,
    get_customer_policies,
    get_customer_claims,
    get_customer_payments,
    get_customer_interactions,
    get_ai_insights,
)
enforce_employee_boundary()


st.markdown("""
<style>

/* =========================================================
   GLOBAL PAGE
   ========================================================= */

.stApp {
    background:
        radial-gradient(
            circle at 88% 4%,
            rgba(99, 102, 241, 0.14),
            transparent 27%
        ),
        radial-gradient(
            circle at 8% 22%,
            rgba(14, 165, 233, 0.08),
            transparent 25%
        ),
        radial-gradient(
            circle at 55% 90%,
            rgba(168, 85, 247, 0.05),
            transparent 25%
        ),
        #07111f;

    color: #e5edf7;
}

.block-container {
    max-width: 1450px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}


/* =========================================================
   HEADINGS
   ========================================================= */

h1,
h2,
h3,
h4 {
    color: #f8fafc !important;
    letter-spacing: -0.02em;
}

h1 {
    font-size: 2.15rem !important;
    font-weight: 750 !important;
}

h2,
h3 {
    font-weight: 700 !important;
}

p,
label,
.stCaption {
    color: #aebed0 !important;
}


/* =========================================================
   TITLE / HERO
   ========================================================= */

.stApp h1 {
    background:
        linear-gradient(
            90deg,
            #f8fafc 0%,
            #dbeafe 42%,
            #a5b4fc 72%,
            #c4b5fd 100%
        );

    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}


/* =========================================================
   METRIC CARDS
   ========================================================= */

[data-testid="stMetric"] {
    background:
        linear-gradient(
            145deg,
            rgba(18, 31, 55, 0.96),
            rgba(10, 22, 40, 0.94)
        );

    border: 1px solid rgba(99, 102, 241, 0.24);

    border-radius: 16px;

    padding: 18px 20px;

    min-height: 105px;

    box-shadow:
        0 10px 30px rgba(0, 0, 0, 0.22),
        inset 0 1px 0 rgba(255, 255, 255, 0.035);

    transition:
        transform 0.18s ease,
        border-color 0.18s ease,
        box-shadow 0.18s ease;
}

[data-testid="stMetric"]:hover {
    transform: translateY(-3px);

    border-color:
        rgba(129, 140, 248, 0.60);

    box-shadow:
        0 15px 35px rgba(0, 0, 0, 0.30),
        0 0 22px rgba(99, 102, 241, 0.08);
}

[data-testid="stMetricLabel"] {
    color: #8fa4bb !important;

    font-size: 0.82rem !important;

    font-weight: 600 !important;
}

[data-testid="stMetricValue"] {
    color: #f8fafc !important;

    font-size: 1.65rem !important;

    font-weight: 750 !important;
}


/* =========================================================
   DIVIDERS
   ========================================================= */

hr {
    border: none !important;

    height: 1px !important;

    background:
        linear-gradient(
            90deg,
            transparent,
            rgba(99, 102, 241, 0.45),
            rgba(71, 102, 138, 0.45),
            transparent
        ) !important;

    margin: 28px 0 !important;
}


/* =========================================================
   INPUTS / SEARCH
   ========================================================= */

div[data-baseweb="input"] {
    background:
        rgba(11, 27, 45, 0.94) !important;

    border: 1px solid
        rgba(71, 102, 138, 0.42) !important;

    border-radius: 10px !important;

    transition:
        border-color 0.18s ease,
        box-shadow 0.18s ease;
}

div[data-baseweb="input"]:focus-within {
    border-color:
        rgba(129, 140, 248, 0.80) !important;

    box-shadow:
        0 0 0 2px
        rgba(99, 102, 241, 0.12) !important;
}

div[data-baseweb="input"] input {
    color: #e5edf7 !important;
}

div[data-baseweb="input"] input::placeholder {
    color: #64748b !important;
}


/* =========================================================
   SELECTBOX
   ========================================================= */

div[data-baseweb="select"] > div {
    background:
        rgba(11, 27, 45, 0.94) !important;

    border-color:
        rgba(71, 102, 138, 0.42) !important;

    border-radius: 10px !important;
}

div[data-baseweb="select"] span {
    color: #dbeafe !important;
}


/* =========================================================
   RECOMMENDATION CARDS
   ========================================================= */

div[data-testid="stVerticalBlockBorderWrapper"] {
    background:
        linear-gradient(
            145deg,
            rgba(17, 30, 52, 0.96),
            rgba(8, 21, 37, 0.96)
        );

    border: 1px solid
        rgba(71, 102, 138, 0.30) !important;

    border-radius: 17px !important;

    box-shadow:
        0 10px 30px rgba(0, 0, 0, 0.22);

    padding: 5px;

    margin-bottom: 15px;

    transition:
        transform 0.18s ease,
        border-color 0.18s ease,
        box-shadow 0.18s ease;
}

div[data-testid="stVerticalBlockBorderWrapper"]:hover {
    transform: translateY(-2px);

    border-color:
        rgba(129, 140, 248, 0.45) !important;

    box-shadow:
        0 15px 38px rgba(0, 0, 0, 0.30),
        0 0 22px rgba(99, 102, 241, 0.06);
}


/* =========================================================
   RECOMMENDATION HEADINGS
   ========================================================= */

.stMarkdown h3 {
    color: #f8fafc !important;
}

.stMarkdown h4 {
    color: #c7d2fe !important;
}


/* =========================================================
   CODE / CUSTOMER IDs
   ========================================================= */

code {
    color: #a5b4fc !important;

    background:
        rgba(49, 46, 129, 0.25) !important;

    border: 1px solid
        rgba(129, 140, 248, 0.18);

    border-radius: 6px;

    padding: 2px 7px;
}


/* =========================================================
   BUTTONS
   ========================================================= */

.stButton > button {
    background:
        linear-gradient(
            135deg,
            #4f46e5,
            #6366f1
        ) !important;

    color: #ffffff !important;

    border: 1px solid
        rgba(165, 180, 252, 0.22) !important;

    border-radius: 9px !important;

    font-weight: 650 !important;

    min-height: 42px;

    box-shadow:
        0 7px 20px
        rgba(79, 70, 229, 0.18);

    transition:
        transform 0.18s ease,
        box-shadow 0.18s ease,
        filter 0.18s ease;
}

.stButton > button:hover {
    filter: brightness(1.10);

    transform: translateY(-1px);

    box-shadow:
        0 11px 27px
        rgba(79, 70, 229, 0.30);
}

.stButton > button:active {
    transform: translateY(0);
}


/* =========================================================
   SECONDARY ACTION BUTTON FEEL
   ========================================================= */

button[kind="secondary"] {
    background:
        rgba(30, 41, 59, 0.90) !important;

    border:
        1px solid rgba(99, 102, 241, 0.35) !important;
}

button[kind="secondary"]:hover {
    background:
        rgba(49, 46, 129, 0.45) !important;
}


/* =========================================================
   EXPANDERS
   ========================================================= */

[data-testid="stExpander"] {
    background:
        rgba(10, 28, 47, 0.90) !important;

    border: 1px solid
        rgba(71, 102, 138, 0.32) !important;

    border-radius: 13px !important;

    overflow: hidden;
}

[data-testid="stExpander"]:hover {
    border-color:
        rgba(129, 140, 248, 0.42) !important;
}

[data-testid="stExpander"] summary {
    color: #dce8f5 !important;

    font-weight: 650 !important;
}


/* =========================================================
   TABS
   ========================================================= */

button[data-baseweb="tab"] {
    color: #8fa4bb !important;

    font-weight: 600 !important;
}

button[data-baseweb="tab"]:hover {
    color: #c7d2fe !important;
}

button[data-baseweb="tab"][aria-selected="true"] {
    color: #a5b4fc !important;
}

div[data-baseweb="tab-highlight"] {
    background:
        linear-gradient(
            90deg,
            #4f46e5,
            #8b5cf6
        ) !important;
}


/* =========================================================
   ALERTS
   ========================================================= */

div[data-testid="stAlert"] {
    border-radius: 12px !important;

    border: 1px solid
        rgba(71, 102, 138, 0.30) !important;

    background:
        rgba(12, 29, 48, 0.92) !important;
}

div[data-testid="stAlert"] p {
    color: #d8e5f2 !important;
}


/* =========================================================
   SUCCESS / AI STATE
   ========================================================= */

div[data-testid="stAlert"][kind="success"] {
    border-color:
        rgba(45, 212, 191, 0.30) !important;
}


/* =========================================================
   DATAFRAMES
   ========================================================= */

[data-testid="stDataFrame"] {
    border: 1px solid
        rgba(71, 102, 138, 0.30);

    border-radius: 12px;

    overflow: hidden;

    box-shadow:
        0 8px 25px rgba(0, 0, 0, 0.18);
}


/* =========================================================
   AI EXPLAINABILITY AREA
   ========================================================= */

[data-testid="stExpander"] p {
    color: #aebed0 !important;
}

.stCaption {
    color: #8195aa !important;
}


/* =========================================================
   SPINNER
   ========================================================= */

[data-testid="stSpinner"] {
    color: #a5b4fc !important;
}


/* =========================================================
   SCROLLBAR
   ========================================================= */

::-webkit-scrollbar {
    width: 8px;
    height: 8px;
}

::-webkit-scrollbar-track {
    background: #07111f;
}

::-webkit-scrollbar-thumb {
    background: #263b52;

    border-radius: 999px;
}

::-webkit-scrollbar-thumb:hover {
    background: #465b78;
}


/* =========================================================
   RESPONSIVE
   ========================================================= */

@media (max-width: 900px) {

    .block-container {
        padding-left: 1rem;
        padding-right: 1rem;
    }

    h1 {
        font-size: 1.75rem !important;
    }

}

</style>
""", unsafe_allow_html=True)
st.title("⚡ Next Best Action")
st.caption(
    "Live customer recommendations using Snowflake data and Cortex AI insights."
)


customers_df = get_all_customers()

if customers_df.empty:
    st.warning("No customer data is currently available.")
    st.stop()

if "CUSTOMER_ID" not in customers_df.columns:
    st.error("CUSTOMERS table is missing CUSTOMER_ID.")
    st.stop()

st.subheader("🔎 Customer Selection")

search_text = st.text_input(
    "Search by Customer ID, first name, last name, city or state",
    placeholder="Example: CUST-1001 or Rahul"
)


filtered_customers = customers_df.copy()


if search_text.strip():

    search_text = search_text.strip().lower()

    searchable_columns = [
        "CUSTOMER_ID",
        "FIRST_NAME",
        "LAST_NAME",
        "CITY",
        "STATE",
    ]

    existing_columns = [
        col
        for col in searchable_columns
        if col in filtered_customers.columns
    ]

    mask = pd.Series(
        False,
        index=filtered_customers.index
    )

    for column in existing_columns:

        mask = mask | (
            filtered_customers[column]
            .astype(str)
            .str.lower()
            .str.contains(
                search_text,
                na=False
            )
        )

    filtered_customers = filtered_customers[mask]


if filtered_customers.empty:

    st.warning(
        "No customers matched your search."
    )

    st.stop()



customer_options = []

customer_lookup = {}


for _, row in filtered_customers.iterrows():

    customer_id = str(
        row.get("CUSTOMER_ID", "")
    ).strip()

    if not customer_id:
        continue

    first_name = str(
        row.get("FIRST_NAME", "")
    ).strip()

    last_name = str(
        row.get("LAST_NAME", "")
    ).strip()

    full_name = (
        f"{first_name} {last_name}"
    ).strip()

    if not full_name:
        full_name = "Customer"

    label = (
        f"{customer_id} — {full_name}"
    )

    customer_options.append(label)
    customer_lookup[label] = customer_id


if not customer_options:

    st.warning("No valid customers found.")
    st.stop()


selected_customer_label = st.selectbox(
    "Select customer",
    customer_options
)


customer_id = customer_lookup[
    selected_customer_label
]

customer_rows = customers_df[
    customers_df["CUSTOMER_ID"]
    .astype(str)
    .str.upper()
    .eq(customer_id.upper())
]


if customer_rows.empty:

    st.error(
        f"Customer {customer_id} could not be loaded."
    )

    st.stop()


customer = customer_rows.iloc[0]


first_name = str(
    customer.get("FIRST_NAME", "")
).strip()

last_name = str(
    customer.get("LAST_NAME", "")
).strip()

customer_name = (
    f"{first_name} {last_name}"
).strip()

if not customer_name:
    customer_name = customer_id

with st.spinner("Loading customer data..."):

    policies_df = get_customer_policies(
        customer_id
    )

    claims_df = get_customer_claims(
        customer_id
    )

    payments_df = get_customer_payments(
        customer_id
    )

    interactions_df = get_customer_interactions(
        customer_id
    )

ai_insights_df = get_ai_insights(customer_id)


customer_context_parts = [
    f"Customer ID: {customer_id}",
    f"Customer name: {customer_name}",
    f"Policies: {len(policies_df)}",
    f"Claims: {len(claims_df)}",
    f"Payments: {len(payments_df)}",
    f"Interactions: {len(interactions_df)}",
]

if not policies_df.empty:
    customer_context_parts.append(
        "POLICIES:\n" + policies_df.to_string(index=False, max_rows=10)
    )

if not claims_df.empty:
    customer_context_parts.append(
        "CLAIMS:\n" + claims_df.to_string(index=False, max_rows=10)
    )

if not payments_df.empty:
    customer_context_parts.append(
        "PAYMENTS:\n" + payments_df.to_string(index=False, max_rows=10)
    )

if not interactions_df.empty:
    customer_context_parts.append(
        "INTERACTIONS:\n"
        + interactions_df.to_string(index=False, max_rows=10)
    )

if not ai_insights_df.empty:
    customer_context_parts.append(
        "CORTEX AI INSIGHTS:\n"
        + ai_insights_df.to_string(index=False, max_rows=10)
    )

customer_context = "\n\n".join(customer_context_parts)

st.markdown("---")

st.subheader(
    f"👤 {customer_name}"
)

st.caption(
    f"Customer ID: {customer_id}"
)


col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "Policies",
        len(policies_df)
    )


with col2:

    st.metric(
        "Claims",
        len(claims_df)
    )


with col3:

    st.metric(
        "Payments",
        len(payments_df)
    )


with col4:

    st.metric(
        "Interactions",
        len(interactions_df)
    )
with st.expander("👤 Customer Profile"):

    profile_data = {}

    for column in [
        "CUSTOMER_ID",
        "FIRST_NAME",
        "LAST_NAME",
        "AGE",
        "CITY",
        "STATE",
        "OCCUPATION",
        "ANNUAL_INCOME",
    ]:

        if column in customer.index:

            profile_data[column] = customer[column]

    if profile_data:

        profile_df = pd.DataFrame(
            list(profile_data.items()),
            columns=[
                "Field",
                "Value"
            ]
        )

        st.dataframe(
            profile_df,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info(
            "No additional profile fields available."
        )

recommendations = []

if (
    not policies_df.empty
    and "RENEWAL_DATE" in policies_df.columns
):

    today = pd.Timestamp.now().normalize()

    for _, policy in policies_df.iterrows():

        renewal_date = pd.to_datetime(
            policy.get("RENEWAL_DATE"),
            errors="coerce"
        )

        if pd.isna(renewal_date):
            continue

        days_to_renewal = (
            renewal_date.normalize()
            - today
        ).days

        status = str(
            policy.get("STATUS", "")
        ).strip().upper()

        if (
            status == "ACTIVE"
            and 0 <= days_to_renewal <= 30
        ):

            policy_id = str(
                policy.get(
                    "POLICY_ID",
                    "N/A"
                )
            )

            recommendations.append({

                "ACTION_TYPE": "RETENTION",

                "ACTION": "Renewal follow-up",

                "PRIORITY": "HIGH",

                "REASON": (
                    f"Policy {policy_id} "
                    f"renews in "
                    f"{days_to_renewal} day(s)."
                ),

                "EVIDENCE": (
                    f"Renewal date: "
                    f"{renewal_date.date()}"
                ),

            })

if not claims_df.empty:

    claim_status_column = None

    for column in [
        "CLAIM_STATUS",
        "STATUS",
    ]:

        if column in claims_df.columns:

            claim_status_column = column
            break


    if claim_status_column:

        open_statuses = {
            "OPEN",
            "PENDING",
            "IN PROGRESS",
            "PROCESSING",
            "UNDER REVIEW",
        }

        open_claims = claims_df[
            claims_df[
                claim_status_column
            ]
            .astype(str)
            .str.upper()
            .isin(open_statuses)
        ]


        if not open_claims.empty:

            recommendations.append({

                "ACTION_TYPE": "CLAIMS",

                "ACTION": "Claims follow-up",

                "PRIORITY": "MEDIUM",

                "REASON": (
                    f"{len(open_claims)} "
                    "claim(s) currently "
                    "require attention."
                ),

                "EVIDENCE": (
                    f"Open/pending claims: "
                    f"{len(open_claims)}"
                ),

            })

if not payments_df.empty:

    payment_status_column = None

    for column in [
        "PAYMENT_STATUS",
        "STATUS",
    ]:

        if column in payments_df.columns:

            payment_status_column = column
            break


    if payment_status_column:

        payment_attention_statuses = {
            "OVERDUE",
            "LATE",
            "FAILED",
            "PENDING",
        }

        attention_payments = payments_df[
            payments_df[
                payment_status_column
            ]
            .astype(str)
            .str.upper()
            .isin(
                payment_attention_statuses
            )
        ]


        if not attention_payments.empty:

            recommendations.append({

                "ACTION_TYPE": "PAYMENT",

                "ACTION": "Payment follow-up",

                "PRIORITY": "HIGH",

                "REASON": (
                    f"{len(attention_payments)} "
                    "payment record(s) "
                    "require attention."
                ),

                "EVIDENCE": (
                    "Payment status indicates "
                    "overdue, late, failed, "
                    "or pending payment."
                ),

            })


if len(interactions_df) >= 3:

    recommendations.append({

        "ACTION_TYPE": "SERVICE",

        "ACTION": (
            "Proactive customer service "
            "follow-up"
        ),

        "PRIORITY": "MEDIUM",

        "REASON": (
            f"Customer has "
            f"{len(interactions_df)} "
            "recorded interactions."
        ),

        "EVIDENCE": (
            "Interaction history"
        ),

    })

if (
    not interactions_df.empty
    and "INTERACTION_DATE"
    in interactions_df.columns
):

    interaction_dates = pd.to_datetime(
        interactions_df[
            "INTERACTION_DATE"
        ],
        errors="coerce"
    )

    valid_dates = (
        interaction_dates
        .dropna()
    )


    if not valid_dates.empty:

        latest_interaction = (
            valid_dates.max()
        )

        days_since = (
            pd.Timestamp.now().normalize()
            - latest_interaction.normalize()
        ).days


        if 0 <= days_since <= 7:

            recommendations.append({

                "ACTION_TYPE": "SERVICE",

                "ACTION": (
                    "Review recent "
                    "customer interaction"
                ),

                "PRIORITY": "LOW",

                "REASON": (
                    "Customer had a recent "
                    "interaction."
                ),

                "EVIDENCE": (
                    f"Latest interaction: "
                    f"{latest_interaction.date()}"
                ),

            })



if not ai_insights_df.empty:
    insight = ai_insights_df.iloc[0]

    sentiment = str(insight.get("SENTIMENT", "")).strip().upper()
    intent = str(insight.get("INTENT", "")).strip().upper()
    topic = str(insight.get("TOPIC", "")).strip()
    churn_signal = str(insight.get("CHURN_SIGNAL", "")).strip().upper()
    urgency = str(insight.get("URGENCY", "")).strip().upper()

    confidence_value = insight.get("CONFIDENCE")
    try:
        confidence_text = f"{float(confidence_value):.0%}"
    except (TypeError, ValueError):
        confidence_text = "N/A"

    retention_signal = (
        churn_signal == "HIGH"
        and (
            sentiment == "NEGATIVE"
            or "RETENTION" in intent
            or "CANCEL" in intent
            or "CANCELLATION" in topic.upper()
        )
    )

    if retention_signal:
        recommendations.append({
            "ACTION_TYPE": "RETENTION",
            "ACTION": "AI-guided retention outreach",
            "PRIORITY": "HIGH",
            "REASON": (
                "Cortex detected a high churn signal with "
                f"{sentiment.lower()} sentiment and intent/topic "
                f"related to {intent.lower() or topic.lower()}."
            ),
            "EVIDENCE": (
                f"Sentiment: {sentiment.title()}; "
                f"Churn: {churn_signal.title()}; "
                f"Urgency: {urgency.title()}; "
                f"Confidence: {confidence_text}; "
                f"Topic: {topic or 'N/A'}"
            ),
        })

    elif urgency == "HIGH":
        recommendations.append({
            "ACTION_TYPE": "SERVICE",
            "ACTION": "Priority customer follow-up",
            "PRIORITY": "HIGH",
            "REASON": (
                "Cortex marked the customer's interaction as high urgency."
            ),
            "EVIDENCE": (
                f"Urgency: {urgency.title()}; "
                f"Sentiment: {sentiment.title()}; "
                f"Churn: {churn_signal.title()}; "
                f"Confidence: {confidence_text}"
            ),
        })

    elif churn_signal == "MEDIUM" and sentiment == "NEGATIVE":
        recommendations.append({
            "ACTION_TYPE": "SERVICE",
            "ACTION": "Proactive customer follow-up",
            "PRIORITY": "MEDIUM",
            "REASON": (
                "Cortex detected negative sentiment with a medium "
                "churn signal."
            ),
            "EVIDENCE": (
                f"Sentiment: {sentiment.title()}; "
                f"Churn: {churn_signal.title()}; "
                f"Urgency: {urgency.title()}; "
                f"Confidence: {confidence_text}"
            ),
        })

    elif "RENEW" in intent or "RENEW" in topic.upper():
        recommendations.append({
            "ACTION_TYPE": "RETENTION",
            "ACTION": "AI-guided renewal follow-up",
            "PRIORITY": "MEDIUM",
            "REASON": (
                "Cortex identified a renewal-related customer intent/topic."
            ),
            "EVIDENCE": (
                f"Intent: {intent.title()}; "
                f"Topic: {topic or 'N/A'}; "
                f"Confidence: {confidence_text}"
            ),
        })

unique_recommendations = []

seen = set()


for recommendation in recommendations:

    key = (
        recommendation["ACTION_TYPE"],
        recommendation["ACTION"]
    )

    if key not in seen:

        seen.add(key)

        unique_recommendations.append(
            recommendation
        )


recommendations = (
    unique_recommendations
)

priority_order = {
    "HIGH": 1,
    "MEDIUM": 2,
    "LOW": 3,
}


recommendations = sorted(
    recommendations,
    key=lambda item: priority_order.get(
        item["PRIORITY"],
        99
    )
)


st.markdown("---")

st.subheader("⚡ Recommended Actions")


if not recommendations:

    st.success(
        "No rule-based action is currently "
        "required from the available data."
    )

else:

    st.caption(
        f"{len(recommendations)} "
        "recommendation(s) generated "
        "from live customer data."
    )


    for index, recommendation in enumerate(
        recommendations,
        start=1
    ):

        with st.container(border=True):

            col1, col2 = st.columns(
                [5, 1]
            )


            with col1:

                st.markdown(
                    f"### {index}. "
                    f"{recommendation['ACTION']}"
                )

                st.write(
                    recommendation["REASON"]
                )

                st.caption(
                    f"Type: "
                    f"{recommendation['ACTION_TYPE']}"
                )

                st.caption(
                    f"Evidence: "
                    f"{recommendation['EVIDENCE']}"
                )


            with col2:

                st.metric(
                    "Priority",
                    recommendation[
                        "PRIORITY"
                    ]
                )

            if st.button(
                "➕ Select for Action History",
                key=f"select_nba_{customer_id}_{index}",
                use_container_width=True,
            ):
                st.session_state["selected_nba"] = {
                    "customer_id": str(customer_id).strip().upper(),
                    "action": recommendation["ACTION"],
                    "reason": recommendation["REASON"],
                    "priority": recommendation["PRIORITY"],
                }
                st.success(
                    "Recommendation selected. Open Action History "
                    "and click Create Action."
                )

            st.markdown("#### 💡 Why this action?")

            if st.button(
                "Explain with Cortex",
                key=f"explain_nba_{customer_id}_{index}",
            ):
                with st.spinner("Explaining recommendation with Cortex..."):
                    explanation = explain_next_best_action(
                        customer_context=customer_context,
                        recommended_action=recommendation["ACTION"],
                    )

                if explanation and not explanation.startswith("⚠️"):
                    st.info(explanation)
                elif explanation:
                    st.error(explanation)
                else:
                    st.warning(
                        "Cortex did not return an explanation."
                    )

st.markdown("---")

st.subheader(
    "📚 Supporting Customer Data"
)


tab1, tab2, tab3, tab4 = st.tabs(
    [
        "🛡️ Policies",
        "📑 Claims",
        "💳 Payments",
        "💬 Interactions",
    ]
)


with tab1:

    if policies_df.empty:

        st.info(
            "No policy records found."
        )

    else:

        st.dataframe(
            policies_df,
            use_container_width=True,
            hide_index=True
        )


with tab2:

    if claims_df.empty:

        st.info(
            "No claim records found."
        )

    else:

        st.dataframe(
            claims_df,
            use_container_width=True,
            hide_index=True
        )


with tab3:

    if payments_df.empty:

        st.info(
            "No payment records found."
        )

    else:

        st.dataframe(
            payments_df,
            use_container_width=True,
            hide_index=True
        )


with tab4:

    if interactions_df.empty:

        st.info(
            "No interaction records found."
        )

    else:

        st.dataframe(
            interactions_df,
            use_container_width=True,
            hide_index=True
        )

st.markdown("---")

st.subheader("🤖 AI Insights & Explainability")

if ai_insights_df.empty:
    st.info("No AI insights are available for this customer yet.")
else:
    st.success(
        f"{len(ai_insights_df)} AI insight(s) loaded from Cortex."
    )

    display_columns = [
        "SENTIMENT",
        "INTENT",
        "TOPIC",
        "CHURN_SIGNAL",
        "URGENCY",
        "CONFIDENCE",
    ]

    available_columns = [
        column
        for column in display_columns
        if column in ai_insights_df.columns
    ]

    if available_columns:
        st.dataframe(
            ai_insights_df[available_columns],
            use_container_width=True,
            hide_index=True,
        )


