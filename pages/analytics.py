'''import streamlit as st
import pandas as pd
from utils.security import enforce_employee_boundary

enforce_employee_boundary()

st.title("📈 Enterprise Analytics & Risk Intelligence")
st.write("Analyze high-risk customer growth trends, churn indicators, claim spikes, and platform data hygiene metrics.")

# 1. Data Hygiene & Anomalies Section (Moved here from System Health)
st.markdown("### 📊 Data Hygiene & Anomalies")

col1, col2, col3 = st.columns(3)
col1.metric("Missing Transcripts", "14", "-2 this week", delta_color="inverse")
col2.metric("Conflicting Signals", "3", "Requires Review", delta_color="off")
col3.metric("Human Review Required", "4", "Low confidence", delta_color="off")

col4, col5, _ = st.columns(3)
col4.metric("Unprocessed Calls", "7", "Pending queue", delta_color="off")
col5.metric("Failed Transcriptions", "1", "Audio error", delta_color="inverse")

st.markdown("---")

# 2. Visual Graphs & Trends
st.markdown("### 📉 High-Risk Customers & Churn Trend Analysis")

# Mock trend data for high risk cases over recent weeks
trend_data = pd.DataFrame({
    "Week": ["Week 1", "Week 2", "Week 3", "Week 4", "Week 5", "Week 6 (Current)"],
    "High Risk Cases": [42, 55, 68, 61, 79, 86],
    "Resolved Interventions": [30, 40, 52, 50, 65, 74]
})

st.line_chart(trend_data.set_index("Week"))
st.caption("Figure: Weekly progression of flagged high-risk customer accounts vs. successfully resolved RM interventions.")

st.markdown("---")

# 3. Claims & Renewal Risk Distribution
col_a, col_b = st.columns(2)

with col_a:
    st.markdown("##### ⚠️ Churn Triggers Breakdown")
    trigger_data = pd.DataFrame({
        "Trigger Factor": ["Premium Increase", "Pending Claim Delay", "Competitor Mention", "Poor Support Call"],
        "Percentage": [45, 25, 20, 10]
    })
    st.bar_chart(trigger_data.set_index("Trigger Factor"))

with col_b:
    st.markdown("##### 📑 Claims Status Distribution")
    claims_dist = pd.DataFrame({
        "Status": ["Approved", "In Progress", "Under Investigation", "Rejected"],
        "Count": [450, 120, 35, 15]
    })
    st.bar_chart(claims_dist.set_index("Status"))'''


import streamlit as st
import pandas as pd

from utils.security import enforce_employee_boundary

from services.snowflake_service import (
    get_all_customers,
    get_all_interactions,
    get_all_ai_insights,
    get_customer_profile,
    get_customer_policies,
    get_customer_claims,
    get_customer_payments,
    get_customer_interactions,
)
enforce_employee_boundary()

st.title("📈 Enterprise Analytics & Risk Intelligence")
st.caption(
    "Live operational analytics from Snowflake — customer risk, "
    "claims, renewals, payments, interactions and data quality."
)


customers_df = get_all_customers()
interactions_df = get_all_interactions()
ai_insights_df = get_all_ai_insights()

@st.cache_data(ttl=60)
def load_operational_data():
    """
    Load policies, claims and payments directly from Snowflake.

    Uses the existing customer-level service functions so this page
    remains compatible with the current snowflake_service.py.
    """

    if customers_df.empty or "CUSTOMER_ID" not in customers_df.columns:
        return pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

    all_policies = []
    all_claims = []
    all_payments = []

    for customer_id in customers_df["CUSTOMER_ID"].dropna().astype(str).unique():

        policies = get_customer_policies(customer_id)
        if not policies.empty:
            all_policies.append(policies)

        claims = get_customer_claims(customer_id)
        if not claims.empty:
            all_claims.append(claims)

        payments = get_customer_payments(customer_id)
        if not payments.empty:
            all_payments.append(payments)

    policies_df = (
        pd.concat(all_policies, ignore_index=True)
        if all_policies
        else pd.DataFrame()
    )

    claims_df = (
        pd.concat(all_claims, ignore_index=True)
        if all_claims
        else pd.DataFrame()
    )

    payments_df = (
        pd.concat(all_payments, ignore_index=True)
        if all_payments
        else pd.DataFrame()
    )

    return policies_df, claims_df, payments_df


policies_df, claims_df, payments_df = load_operational_data()

def normalize_status(value):
    if pd.isna(value):
        return ""

    return str(value).strip().upper()


def count_status(df, column, statuses):
    if df.empty or column not in df.columns:
        return 0

    values = df[column].astype(str).str.strip().str.upper()

    return int(values.isin(statuses).sum())


def safe_datetime(df, column):
    if df.empty or column not in df.columns:
        return pd.Series(dtype="datetime64[ns]")

    return pd.to_datetime(
        df[column],
        errors="coerce"
    )

st.markdown("## 🏢 Enterprise Overview")

total_customers = (
    len(customers_df)
    if not customers_df.empty
    else 0
)

total_policies = (
    len(policies_df)
    if not policies_df.empty
    else 0
)

total_claims = (
    len(claims_df)
    if not claims_df.empty
    else 0
)

total_interactions = (
    len(interactions_df)
    if not interactions_df.empty
    else 0
)

total_payments = (
    len(payments_df)
    if not payments_df.empty
    else 0
)


col1, col2, col3, col4, col5 = st.columns(5)

col1.metric(
    "👥 Customers",
    f"{total_customers:,}"
)

col2.metric(
    "📄 Policies",
    f"{total_policies:,}"
)

col3.metric(
    "🧾 Claims",
    f"{total_claims:,}"
)

col4.metric(
    "💬 Interactions",
    f"{total_interactions:,}"
)

col5.metric(
    "💳 Payments",
    f"{total_payments:,}"
)


st.markdown("## ⚠️ Operational Risk Indicators")

renewals_30d = 0

if not policies_df.empty and "RENEWAL_DATE" in policies_df.columns:

    renewal_dates = safe_datetime(
        policies_df,
        "RENEWAL_DATE"
    )

    today = pd.Timestamp.today().normalize()

    days_to_renewal = (
        renewal_dates - today
    ).dt.days

    renewals_30d = int(
        (
            (days_to_renewal >= 0)
            & (days_to_renewal <= 30)
        ).sum()
    )

open_claims = count_status(
    claims_df,
    "CLAIM_STATUS",
    {
        "OPEN",
        "PENDING",
        "IN_PROGRESS",
        "UNDER_INVESTIGATION"
    }
)


payment_risk = count_status(
    payments_df,
    "PAYMENT_STATUS",
    {
        "OVERDUE",
        "LATE",
        "FAILED",
        "PENDING"
    }
)
repeated_interaction_customers = 0

if (
    not interactions_df.empty
    and "CUSTOMER_ID" in interactions_df.columns
):

    interaction_counts = (
        interactions_df
        .groupby("CUSTOMER_ID")
        .size()
    )

    repeated_interaction_customers = int(
        (interaction_counts >= 3).sum()
    )


col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "🔄 Renewals ≤ 30 Days",
    renewals_30d
)

col2.metric(
    "🧾 Open / Pending Claims",
    open_claims
)

col3.metric(
    "💰 Payment Risk",
    payment_risk
)

col4.metric(
    "🔁 Repeated Interaction Customers",
    repeated_interaction_customers
)

st.markdown("## 🧹 Data Quality & AI Readiness")

missing_transcripts = 0
available_transcripts = 0

if not interactions_df.empty and "TRANSCRIPT" in interactions_df.columns:

    transcript_series = (
        interactions_df["TRANSCRIPT"]
        .fillna("")
        .astype(str)
        .str.strip()
    )

    missing_transcripts = int(
        (transcript_series == "").sum()
    )

    available_transcripts = int(
        (transcript_series != "").sum()
    )

ai_insights_available = (
    len(ai_insights_df)
    if not ai_insights_df.empty
    else 0
)


col1, col2, col3 = st.columns(3)

col1.metric(
    "📝 Transcripts Available",
    available_transcripts
)

col2.metric(
    "⚠️ Missing Transcripts",
    missing_transcripts
)

col3.metric(
    "🤖 AI Insights",
    ai_insights_available
)

st.markdown("## 📄 Policy Portfolio")

if (
    not policies_df.empty
    and "POLICY_TYPE" in policies_df.columns
):

    policy_distribution = (
        policies_df["POLICY_TYPE"]
        .fillna("UNKNOWN")
        .astype(str)
        .str.strip()
        .replace("", "UNKNOWN")
        .value_counts()
        .rename_axis("Policy Type")
        .reset_index(name="Count")
    )

    st.bar_chart(
        policy_distribution.set_index("Policy Type")
    )

else:

    st.info(
        "No policy data is currently available."
    )

st.markdown("## 🧾 Claims Distribution")

if (
    not claims_df.empty
    and "CLAIM_STATUS" in claims_df.columns
):

    claim_distribution = (
        claims_df["CLAIM_STATUS"]
        .fillna("UNKNOWN")
        .astype(str)
        .str.strip()
        .replace("", "UNKNOWN")
        .str.upper()
        .value_counts()
        .rename_axis("Claim Status")
        .reset_index(name="Count")
    )

    st.bar_chart(
        claim_distribution.set_index("Claim Status")
    )

else:

    st.info(
        "No claim data is currently available."
    )

st.markdown("## 💳 Payment Status")

if (
    not payments_df.empty
    and "PAYMENT_STATUS" in payments_df.columns
):

    payment_distribution = (
        payments_df["PAYMENT_STATUS"]
        .fillna("UNKNOWN")
        .astype(str)
        .str.strip()
        .replace("", "UNKNOWN")
        .str.upper()
        .value_counts()
        .rename_axis("Payment Status")
        .reset_index(name="Count")
    )

    st.bar_chart(
        payment_distribution.set_index("Payment Status")
    )

else:

    st.info(
        "No payment data is currently available."
    )

st.markdown("## 💬 Customer Interaction Analytics")

if (
    not interactions_df.empty
    and "INTERACTION_TYPE" in interactions_df.columns
):

    interaction_distribution = (
        interactions_df["INTERACTION_TYPE"]
        .fillna("UNKNOWN")
        .astype(str)
        .str.strip()
        .replace("", "UNKNOWN")
        .str.upper()
        .value_counts()
        .rename_axis("Interaction Type")
        .reset_index(name="Count")
    )

    st.bar_chart(
        interaction_distribution.set_index("Interaction Type")
    )

else:

    st.info(
        "No interaction data is currently available."
    )


st.markdown("## 🤖 AI Risk Intelligence")

if ai_insights_df.empty:

    st.info(
        "AI_INSIGHTS is not available yet. "
        "AI risk analytics will appear here once transcript "
        "processing and insight generation are enabled."
    )

else:

    insight_col1, insight_col2, insight_col3 = st.columns(3)


    if "SENTIMENT" in ai_insights_df.columns:

        sentiment_counts = (
            ai_insights_df["SENTIMENT"]
            .fillna("UNKNOWN")
            .astype(str)
            .str.strip()
            .str.upper()
            .value_counts()
        )

        negative_count = int(
            sentiment_counts.get("NEGATIVE", 0)
        )

        positive_count = int(
            sentiment_counts.get("POSITIVE", 0)
        )

    else:

        negative_count = 0
        positive_count = 0



    if "CHURN_SIGNAL" in ai_insights_df.columns:

        churn_values = (
            ai_insights_df["CHURN_SIGNAL"]
            .fillna("")
            .astype(str)
            .str.strip()
            .str.upper()
        )

        high_churn = int(
            (churn_values == "HIGH").sum()
        )

    else:

        high_churn = 0


    insight_col1.metric(
        "🔴 Negative Sentiment",
        negative_count
    )

    insight_col2.metric(
        "🟢 Positive Sentiment",
        positive_count
    )

    insight_col3.metric(
        "🚨 High Churn Signals",
        high_churn
    )


    if "SENTIMENT" in ai_insights_df.columns:

        sentiment_distribution = (
            ai_insights_df["SENTIMENT"]
            .fillna("UNKNOWN")
            .astype(str)
            .str.strip()
            .str.upper()
            .value_counts()
            .rename_axis("Sentiment")
            .reset_index(name="Count")
        )

        st.bar_chart(
            sentiment_distribution.set_index("Sentiment")
        )


    if "CHURN_SIGNAL" in ai_insights_df.columns:

        churn_distribution = (
            ai_insights_df["CHURN_SIGNAL"]
            .fillna("UNKNOWN")
            .astype(str)
            .str.strip()
            .str.upper()
            .value_counts()
            .rename_axis("Churn Signal")
            .reset_index(name="Count")
        )

        st.bar_chart(
            churn_distribution.set_index("Churn Signal")
        )

st.markdown("## 🚨 Customers Requiring Attention")

risk_customers = []

if not customers_df.empty and "CUSTOMER_ID" in customers_df.columns:

    for customer_id in customers_df["CUSTOMER_ID"].dropna().astype(str).unique():

        policies = get_customer_policies(customer_id)
        claims = get_customer_claims(customer_id)
        payments = get_customer_payments(customer_id)
        interactions = get_customer_interactions(customer_id)

        risk_reasons = []

        if (
            not policies.empty
            and "RENEWAL_DATE" in policies.columns
        ):

            renewal_dates = safe_datetime(
                policies,
                "RENEWAL_DATE"
            )

            today = pd.Timestamp.today().normalize()

            renewal_days = (
                renewal_dates - today
            ).dt.days

            if (
                (
                    (renewal_days >= 0)
                    & (renewal_days <= 30)
                ).any()
            ):
                risk_reasons.append(
                    "Renewal within 30 days"
                )
        if count_status(
            claims,
            "CLAIM_STATUS",
            {
                "OPEN",
                "PENDING",
                "IN_PROGRESS",
                "UNDER_INVESTIGATION"
            }
        ) > 0:

            risk_reasons.append(
                "Open/pending claim"
            )

        if count_status(
            payments,
            "PAYMENT_STATUS",
            {
                "OVERDUE",
                "LATE",
                "FAILED"
            }
        ) > 0:

            risk_reasons.append(
                "Payment risk"
            )

        if len(interactions) >= 3:

            risk_reasons.append(
                "Repeated support interactions"
            )


        if risk_reasons:

            customer_name = customer_id

            if not customers_df.empty:

                match = customers_df[
                    customers_df["CUSTOMER_ID"].astype(str)
                    == customer_id
                ]

                if not match.empty:

                    first_name = match.iloc[0].get(
                        "FIRST_NAME",
                        ""
                    )

                    last_name = match.iloc[0].get(
                        "LAST_NAME",
                        ""
                    )

                    customer_name = (
                        f"{first_name} {last_name}"
                    ).strip()

                    if not customer_name:

                        customer_name = customer_id


            risk_customers.append(
                {
                    "Customer ID": customer_id,
                    "Customer": customer_name,
                    "Risk Triggers": ", ".join(
                        risk_reasons
                    ),
                    "Risk Count": len(
                        risk_reasons
                    ),
                }
            )


if risk_customers:

    risk_df = pd.DataFrame(
        risk_customers
    ).sort_values(
        "Risk Count",
        ascending=False
    )

    st.dataframe(
        risk_df[
            [
                "Customer ID",
                "Customer",
                "Risk Triggers",
                "Risk Count",
            ]
        ],
        use_container_width=True,
        hide_index=True,
    )

else:

    st.success(
        "No customers currently match the configured operational risk rules."
    )
st.markdown("## 🗄️ Data Availability")

availability_df = pd.DataFrame(
    {
        "Dataset": [
            "Customers",
            "Policies",
            "Claims",
            "Payments",
            "Interactions",
            "AI Insights",
        ],
        "Rows Available": [
            len(customers_df),
            len(policies_df),
            len(claims_df),
            len(payments_df),
            len(interactions_df),
            len(ai_insights_df),
        ],
    }
)

st.dataframe(
    availability_df,
    use_container_width=True,
    hide_index=True,
)

st.markdown("---")

st.caption(
    "Analytics are calculated from live Snowflake data. "
    "AI-specific metrics remain unavailable until AI_INSIGHTS "
    "and transcript processing are enabled."
)
