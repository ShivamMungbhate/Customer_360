import streamlit as st
import pandas as pd

from utils.security import enforce_employee_boundary

from services.snowflake_service import (
    get_system_health,
    get_all_customers,
    get_all_interactions,
    get_all_ai_insights,
    get_customer_policies,
    get_customer_claims,
    get_customer_payments,
)
enforce_employee_boundary()


st.title("⚙️ System & Data Quality Health Dashboard")

st.caption(
    "Live monitoring of Snowflake data, customer interactions, "
    "AI readiness and operational data quality."
)


system_health = get_system_health()

customers_df = get_all_customers()
interactions_df = get_all_interactions()
ai_insights_df = get_all_ai_insights()



def safe_count(dataframe):
    if dataframe is None:
        return 0

    return len(dataframe)


def get_count(table_name):
    return int(system_health.get(table_name, 0))


def safe_datetime(df, column):
    if df.empty or column not in df.columns:
        return pd.Series(dtype="datetime64[ns]")

    return pd.to_datetime(
        df[column],
        errors="coerce"
    )
st.markdown("## 🖥️ Core System Status")


# Snowflake connectivity
database_status = "Healthy"

if not system_health:
    database_status = "Unavailable"


# Customer data
customer_count = get_count("CUSTOMERS")

# Interaction data
interaction_count = get_count("INTERACTIONS")

# AI pipeline
ai_count = get_count("AI_INSIGHTS")


col_s1, col_s2, col_s3 = st.columns(3)

col_s1.metric(
    "Database Connection",
    database_status,
    "🟢 Connected" if database_status == "Healthy" else "🔴 Unavailable"
)

col_s2.metric(
    "Customer Data",
    f"{customer_count:,} records",
    "Live Snowflake"
)

col_s3.metric(
    "Interaction Data",
    f"{interaction_count:,} records",
    "Live Snowflake"
)


col_s4, col_s5, col_s6 = st.columns(3)

col_s4.metric(
    "Transcription Pipeline",
    "Data Monitoring",
    "Pipeline not yet enabled"
)

col_s5.metric(
    "AI Insight Pipeline",
    (
        "Available"
        if ai_count > 0
        else "Not Available"
    ),
    f"{ai_count:,} insights"
)

col_s6.metric(
    "NBA Engine",
    f"{get_count('NEXT_BEST_ACTIONS'):,} records",
    "Stored recommendations"
)
st.markdown("---")
st.markdown("## 🗄️ Snowflake Table Health")


table_rows = [
    {
        "Table": "CUSTOMERS",
        "Rows": get_count("CUSTOMERS"),
        "Status": "🟢 Available" if get_count("CUSTOMERS") > 0 else "⚠️ Empty",
    },
    {
        "Table": "POLICIES",
        "Rows": get_count("POLICIES"),
        "Status": "🟢 Available" if get_count("POLICIES") > 0 else "⚠️ Empty",
    },
    {
        "Table": "CLAIMS",
        "Rows": get_count("CLAIMS"),
        "Status": "🟢 Available" if get_count("CLAIMS") > 0 else "⚠️ Empty",
    },
    {
        "Table": "PAYMENTS",
        "Rows": get_count("PAYMENTS"),
        "Status": "🟢 Available" if get_count("PAYMENTS") > 0 else "⚠️ Empty",
    },
    {
        "Table": "INTERACTIONS",
        "Rows": get_count("INTERACTIONS"),
        "Status": "🟢 Available" if get_count("INTERACTIONS") > 0 else "⚠️ Empty",
    },
    {
        "Table": "AI_INSIGHTS",
        "Rows": get_count("AI_INSIGHTS"),
        "Status": (
            "🟢 Available"
            if get_count("AI_INSIGHTS") > 0
            else "⚪ Not Available"
        ),
    },
    {
        "Table": "NEXT_BEST_ACTIONS",
        "Rows": get_count("NEXT_BEST_ACTIONS"),
        "Status": (
            "🟢 Available"
            if get_count("NEXT_BEST_ACTIONS") > 0
            else "⚪ Not Available"
        ),
    },
    {
        "Table": "ACTION_HISTORY",
        "Rows": get_count("ACTION_HISTORY"),
        "Status": (
            "🟢 Available"
            if get_count("ACTION_HISTORY") > 0
            else "⚠️ Empty"
        ),
    },
    {
        "Table": "USERS",
        "Rows": get_count("USERS"),
        "Status": (
            "🟢 Available"
            if get_count("USERS") > 0
            else "⚠️ Empty"
        ),
    },
]


table_health_df = pd.DataFrame(table_rows)

st.dataframe(
    table_health_df,
    use_container_width=True,
    hide_index=True,
)

st.markdown("---")
st.markdown("## 🔍 Data Quality Summary")

missing_transcripts = 0
available_transcripts = 0

if (
    not interactions_df.empty
    and "TRANSCRIPT" in interactions_df.columns
):

    transcript_values = (
        interactions_df["TRANSCRIPT"]
        .fillna("")
        .astype(str)
        .str.strip()
    )

    missing_transcripts = int(
        (transcript_values == "").sum()
    )

    available_transcripts = int(
        (transcript_values != "").sum()
    )


missing_customer_ids = 0

if (
    not interactions_df.empty
    and "CUSTOMER_ID" in interactions_df.columns
):

    missing_customer_ids = int(
        interactions_df["CUSTOMER_ID"]
        .isna()
        .sum()
    )

ai_insights_available = len(
    ai_insights_df
)


col1, col2, col3, col4 = st.columns(4)

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

col4.metric(
    "❓ Missing Interaction IDs",
    missing_customer_ids
)

st.markdown("---")
st.markdown("## 📝 Transcript Quality")


if missing_transcripts > 0:

    st.warning(
        f"{missing_transcripts} interaction records "
        "do not currently contain a transcript."
    )

    missing_df = interactions_df.copy()

    if "TRANSCRIPT" in missing_df.columns:

        transcript_values = (
            missing_df["TRANSCRIPT"]
            .fillna("")
            .astype(str)
            .str.strip()
        )

        missing_df = missing_df[
            transcript_values == ""
        ].copy()

    display_columns = [
        column
        for column in [
            "INTERACTION_ID",
            "CUSTOMER_ID",
            "INTERACTION_TYPE",
            "INTERACTION_DATE",
            "TRANSCRIPT",
        ]
        if column in missing_df.columns
    ]

    if display_columns:

        st.dataframe(
            missing_df[display_columns],
            use_container_width=True,
            hide_index=True,
        )

else:

    st.success(
        "✅ No missing transcripts detected in the current interaction dataset."
    )

st.markdown("---")
st.markdown("## 💬 Interaction Data Inspection")


if interactions_df.empty:

    st.info(
        "No interaction records are currently available."
    )

else:

    interaction_types = []

    if "INTERACTION_TYPE" in interactions_df.columns:

        interaction_types = sorted(
            interactions_df["INTERACTION_TYPE"]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        )

    selected_type = st.selectbox(
        "Filter by interaction type",
        ["All"] + interaction_types,
    )

    filtered_interactions = interactions_df.copy()

    if (
        selected_type != "All"
        and "INTERACTION_TYPE" in filtered_interactions.columns
    ):

        filtered_interactions = filtered_interactions[
            filtered_interactions["INTERACTION_TYPE"]
            .astype(str)
            == selected_type
        ]

    st.write(
        f"Showing **{len(filtered_interactions):,}** interaction records."
    )

    display_columns = [
        column
        for column in [
            "INTERACTION_ID",
            "CUSTOMER_ID",
            "INTERACTION_TYPE",
            "INTERACTION_DATE",
            "TRANSCRIPT",
        ]
        if column in filtered_interactions.columns
    ]

    st.dataframe(
        filtered_interactions[display_columns],
        use_container_width=True,
        hide_index=True,
    )

st.markdown("---")
st.markdown("## 🤖 AI Pipeline Status")


if ai_insights_df.empty:

    st.info(
        "AI_INSIGHTS is currently unavailable. "
        "Transcript-to-AI insight processing has not yet been "
        "enabled in the active Snowflake pipeline."
    )

    ai_status_df = pd.DataFrame(
        [
            {
                "Pipeline": "Transcript Processing",
                "Status": "Not Enabled",
                "Evidence": f"{available_transcripts:,} transcripts available",
            },
            {
                "Pipeline": "AI Insight Generation",
                "Status": "Not Available",
                "Evidence": "AI_INSIGHTS has no available records",
            },
            {
                "Pipeline": "Next Best Action",
                "Status": (
                    "Available"
                    if get_count("NEXT_BEST_ACTIONS") > 0
                    else "No Stored Records"
                ),
                "Evidence": (
                    f"{get_count('NEXT_BEST_ACTIONS'):,} NBA records"
                ),
            },
        ]
    )

else:

    ai_status_df = pd.DataFrame(
        [
            {
                "Pipeline": "Transcript Processing",
                "Status": "Data Available",
                "Evidence": f"{available_transcripts:,} transcripts",
            },
            {
                "Pipeline": "AI Insight Generation",
                "Status": "Available",
                "Evidence": f"{ai_insights_available:,} AI insights",
            },
            {
                "Pipeline": "Next Best Action",
                "Status": (
                    "Available"
                    if get_count("NEXT_BEST_ACTIONS") > 0
                    else "No Stored Records"
                ),
                "Evidence": (
                    f"{get_count('NEXT_BEST_ACTIONS'):,} NBA records"
                ),
            },
        ]
    )


st.dataframe(
    ai_status_df,
    use_container_width=True,
    hide_index=True,
)

st.markdown("---")
st.markdown("## 📋 Action Execution Health")


action_count = get_count(
    "ACTION_HISTORY"
)

if action_count > 0:

    st.success(
        f"✅ {action_count:,} action history records are available."
    )

else:

    st.info(
        "No action history records are currently available."
    )


st.markdown("---")
st.markdown("## 📊 Database Snapshot")


snapshot_df = pd.DataFrame(
    [
        {
            "Dataset": table,
            "Row Count": count,
        }
        for table, count in system_health.items()
    ]
)

st.bar_chart(
    snapshot_df.set_index("Dataset")
)


st.markdown("---")
st.markdown("## 🔎 Customer Data Inspection")


if customers_df.empty:

    st.warning(
        "No customer records are available for inspection."
    )

else:

    customer_options = (
        customers_df["CUSTOMER_ID"]
        .dropna()
        .astype(str)
        .sort_values()
        .tolist()
        if "CUSTOMER_ID" in customers_df.columns
        else []
    )

    if customer_options:

        selected_customer = st.selectbox(
            "Select Customer",
            customer_options,
        )

        selected_customer_df = customers_df[
            customers_df["CUSTOMER_ID"]
            .astype(str)
            == selected_customer
        ]

        if not selected_customer_df.empty:

            st.dataframe(
                selected_customer_df,
                use_container_width=True,
                hide_index=True,
            )

            if st.button(
                "🔍 Open Customer 360",
                use_container_width=True,
            ):

                st.session_state[
                    "selected_customer_id"
                ] = selected_customer

                st.switch_page(
                    "pages/customer_360.py"
                )

st.markdown("---")
st.markdown("## ✅ System Summary")


summary_items = []

if customer_count > 0:
    summary_items.append(
        "🟢 Customer data is available."
    )
else:
    summary_items.append(
        "🔴 Customer data is unavailable."
    )


if interaction_count > 0:
    summary_items.append(
        "🟢 Interaction data is available."
    )
else:
    summary_items.append(
        "⚠️ No interaction records are available."
    )


if missing_transcripts > 0:
    summary_items.append(
        f"⚠️ {missing_transcripts} interactions "
        "have missing transcripts."
    )
else:
    summary_items.append(
        "🟢 No missing transcripts detected."
    )


if ai_count > 0:
    summary_items.append(
        "🟢 AI insight records are available."
    )
else:
    summary_items.append(
        "⚪ AI_INSIGHTS is not yet active."
    )


if get_count("ACTION_HISTORY") > 0:
    summary_items.append(
        "🟢 Action execution history is available."
    )
else:
    summary_items.append(
        "⚪ No action history records found."
    )


for item in summary_items:
    st.write(item)


st.caption(
    "All displayed database counts and quality indicators are "
    "derived from the current Snowflake environment. "
    "Unavailable pipelines are explicitly shown as unavailable "
    "rather than represented with simulated health metrics."
)