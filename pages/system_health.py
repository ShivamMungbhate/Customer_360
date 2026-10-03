

import streamlit as st
import pandas as pd

from utils.security import enforce_employee_boundary

from services.snowflake_service import (
    get_system_health,
    get_all_customers,
    get_all_interactions,
    get_all_ai_insights,
)

enforce_employee_boundary()

st.title("⚙️ System & Data Quality Health Dashboard")

st.caption(
    "Live monitoring of Snowflake data, customer interactions, "
    "AI insights and operational data quality."
)

system_health = get_system_health()
customers_df = get_all_customers()
interactions_df = get_all_interactions()
ai_insights_df = get_all_ai_insights()


def get_count(table_name):
    try:
        return int(system_health.get(table_name, 0))
    except Exception:
        return 0


def safe_len(df):
    if df is None:
        return 0
    return len(df)


customer_count = get_count("CUSTOMERS")
interaction_count = get_count("INTERACTIONS")
ai_table_count = get_count("AI_INSIGHTS")
nba_count = get_count("NEXT_BEST_ACTIONS")
action_count = get_count("ACTION_HISTORY")

ai_insights_available = safe_len(ai_insights_df)

missing_transcripts = 0
available_transcripts = 0

if (
    interactions_df is not None
    and not interactions_df.empty
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
    interactions_df is not None
    and not interactions_df.empty
    and "CUSTOMER_ID" in interactions_df.columns
):

    missing_customer_ids = int(
        interactions_df["CUSTOMER_ID"].isna().sum()
    )


st.markdown("## 🖥️ Core System Status")

database_status = (
    "Healthy"
    if system_health
    else "Unavailable"
)

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Database Connection",
        database_status,
        "🟢 Connected"
        if database_status == "Healthy"
        else "🔴 Unavailable"
    )

with col2:
    st.metric(
        "Customer Data",
        f"{customer_count:,} records",
        "Live Snowflake"
    )

with col3:
    st.metric(
        "Interaction Data",
        f"{interaction_count:,} records",
        "Live Snowflake"
    )


col4, col5, col6 = st.columns(3)

with col4:
    st.metric(
        "Transcripts",
        f"{available_transcripts:,}",
        f"{missing_transcripts:,} missing"
    )

with col5:

    if ai_insights_available > 0:

        st.metric(
            "AI Insight Pipeline",
            "WORKING",
            f"{ai_insights_available:,} insights"
        )

    elif ai_table_count > 0:

        st.metric(
            "AI Insight Pipeline",
            "DATA AVAILABLE",
            f"{ai_table_count:,} records"
        )

    else:

        st.metric(
            "AI Insight Pipeline",
            "NO INSIGHTS",
            "0 stored records"
        )

with col6:
    st.metric(
        "NBA Engine",
        f"{nba_count:,} records",
        "Stored recommendations"
    )


st.markdown("---")

st.markdown("## 🤖 AI Insights")

if ai_insights_df is None:

    st.error(
        "The AI_INSIGHTS query returned no dataframe."
    )

elif ai_insights_df.empty:

    st.warning(
        "AI_INSIGHTS currently contains no stored insight records."
    )

    st.info(
        "The dashboard is connected to the AI_INSIGHTS table, "
        "but no generated insights have been stored yet."
    )

else:

    st.success(
        f"🟢 AI Insights are working. "
        f"{len(ai_insights_df):,} insight record(s) are available."
    )

    st.markdown("### Stored AI Insights")

    st.dataframe(
        ai_insights_df,
        use_container_width=True,
        hide_index=True
    )

    st.markdown("### AI Insight Columns")

    insight_columns = pd.DataFrame(
        {
            "Column": ai_insights_df.columns.tolist(),
            "Non-Null Values": [
                int(ai_insights_df[column].notna().sum())
                for column in ai_insights_df.columns
            ],
        }
    )

    st.dataframe(
        insight_columns,
        use_container_width=True,
        hide_index=True
    )


st.markdown("---")

st.markdown("## 🗄️ Snowflake Table Health")

table_rows = [
    {
        "Table": "CUSTOMERS",
        "Rows": customer_count,
        "Status": (
            "🟢 Available"
            if customer_count > 0
            else "⚠️ Empty"
        ),
    },
    {
        "Table": "POLICIES",
        "Rows": get_count("POLICIES"),
        "Status": (
            "🟢 Available"
            if get_count("POLICIES") > 0
            else "⚠️ Empty"
        ),
    },
    {
        "Table": "CLAIMS",
        "Rows": get_count("CLAIMS"),
        "Status": (
            "🟢 Available"
            if get_count("CLAIMS") > 0
            else "⚠️ Empty"
        ),
    },
    {
        "Table": "PAYMENTS",
        "Rows": get_count("PAYMENTS"),
        "Status": (
            "🟢 Available"
            if get_count("PAYMENTS") > 0
            else "⚠️ Empty"
        ),
    },
    {
        "Table": "INTERACTIONS",
        "Rows": interaction_count,
        "Status": (
            "🟢 Available"
            if interaction_count > 0
            else "⚠️ Empty"
        ),
    },
    {
        "Table": "AI_INSIGHTS",
        "Rows": ai_table_count,
        "Status": (
            "🟢 Available"
            if ai_table_count > 0
            else "⚪ No Records"
        ),
    },
    {
        "Table": "NEXT_BEST_ACTIONS",
        "Rows": nba_count,
        "Status": (
            "🟢 Available"
            if nba_count > 0
            else "⚪ No Records"
        ),
    },
    {
        "Table": "ACTION_HISTORY",
        "Rows": action_count,
        "Status": (
            "🟢 Available"
            if action_count > 0
            else "⚪ Empty"
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
    hide_index=True
)


st.markdown("---")

st.markdown("## 🔍 Data Quality Summary")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "📝 Transcripts Available",
        available_transcripts
    )

with col2:
    st.metric(
        "⚠️ Missing Transcripts",
        missing_transcripts
    )

with col3:
    st.metric(
        "🤖 AI Insights",
        ai_insights_available
    )

with col4:
    st.metric(
        "❓ Missing Customer IDs",
        missing_customer_ids
    )


st.markdown("---")

st.markdown("## 📝 Transcript Quality")

if missing_transcripts > 0:

    st.warning(
        f"{missing_transcripts} interaction record(s) "
        "do not currently contain a transcript."
    )

    missing_df = interactions_df.copy()

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
            hide_index=True
        )

else:

    st.success(
        "✅ No missing transcripts detected."
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
        ["All"] + interaction_types
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
        f"Showing **{len(filtered_interactions):,}** "
        "interaction records."
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
        hide_index=True
    )


st.markdown("---")

st.markdown("## 🤖 AI Pipeline Status")

ai_pipeline_rows = [
    {
        "Pipeline": "Snowflake Connection",
        "Status": (
            "🟢 Healthy"
            if system_health
            else "🔴 Unavailable"
        ),
        "Evidence": "Snowflake system health query",
    },
    {
        "Pipeline": "Transcript Data",
        "Status": (
            "🟢 Available"
            if available_transcripts > 0
            else "⚪ No Data"
        ),
        "Evidence": (
            f"{available_transcripts:,} transcripts"
        ),
    },
    {
        "Pipeline": "AI Insight Storage",
        "Status": (
            "🟢 Working"
            if ai_insights_available > 0
            else "⚪ No Stored Insights"
        ),
        "Evidence": (
            f"{ai_insights_available:,} records returned "
            "from AI_INSIGHTS"
        ),
    },
    {
        "Pipeline": "Next Best Action",
        "Status": (
            "🟢 Available"
            if nba_count > 0
            else "⚪ No Stored Records"
        ),
        "Evidence": (
            f"{nba_count:,} NBA records"
        ),
    },
]

ai_status_df = pd.DataFrame(ai_pipeline_rows)

st.dataframe(
    ai_status_df,
    use_container_width=True,
    hide_index=True
)


st.markdown("---")

st.markdown("## 📋 Action Execution Health")

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

if not snapshot_df.empty:

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

    if "CUSTOMER_ID" in customers_df.columns:

        customer_options = (
            customers_df["CUSTOMER_ID"]
            .dropna()
            .astype(str)
            .sort_values()
            .tolist()
        )

    else:

        customer_options = []

    if customer_options:

        selected_customer = st.selectbox(
            "Select Customer",
            customer_options
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
                hide_index=True
            )

            if st.button(
                "🔍 Open Customer 360",
                use_container_width=True
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

if ai_insights_available > 0:
    summary_items.append(
        f"🟢 AI Insights are working with "
        f"{ai_insights_available:,} stored insight records."
    )
else:
    summary_items.append(
        "⚪ No AI insight records are currently stored."
    )

if action_count > 0:
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
    "derived from the current Snowflake environment."
)