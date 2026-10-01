import streamlit as st
import pandas as pd

from utils.security import enforce_employee_boundary
from services.snowflake_service import (
    get_all_interactions,
    get_all_ai_insights,
)
enforce_employee_boundary()

st.title("💬 Interactions & AI Insights")

st.write(
    "Review customer conversations, call transcripts, "
    "and AI-extracted structured insights."
)

interactions_df = get_all_interactions()
insights_df = get_all_ai_insights()
total_interactions = len(interactions_df)
total_insights = len(insights_df)

transcript_count = 0

if not interactions_df.empty and "TRANSCRIPT" in interactions_df.columns:
    transcript_count = (
        interactions_df["TRANSCRIPT"]
        .fillna("")
        .astype(str)
        .str.strip()
        .ne("")
        .sum()
    )


unique_customers = 0

if not interactions_df.empty and "CUSTOMER_ID" in interactions_df.columns:
    unique_customers = interactions_df["CUSTOMER_ID"].nunique()


col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Interactions",
        total_interactions
    )

with col2:
    st.metric(
        "Customers",
        unique_customers
    )

with col3:
    st.metric(
        "Transcripts Available",
        transcript_count
    )

with col4:
    st.metric(
        "AI Insights",
        total_insights
    )


st.markdown("---")
st.subheader("🔎 Interaction Explorer")


search_col1, search_col2 = st.columns([1, 2])

with search_col1:

    customer_filter = st.text_input(
        "Customer ID",
        placeholder="Example: C001"
    )

with search_col2:

    interaction_type_filter = st.text_input(
        "Interaction Type",
        placeholder="Example: CALL, EMAIL, CHAT"
    )


filtered_interactions = interactions_df.copy()


if not filtered_interactions.empty:

    if customer_filter:

        if "CUSTOMER_ID" in filtered_interactions.columns:

            filtered_interactions = filtered_interactions[
                filtered_interactions["CUSTOMER_ID"]
                .astype(str)
                .str.upper()
                .str.contains(
                    customer_filter.strip().upper(),
                    na=False
                )
            ]


    if interaction_type_filter:

        if "INTERACTION_TYPE" in filtered_interactions.columns:

            filtered_interactions = filtered_interactions[
                filtered_interactions["INTERACTION_TYPE"]
                .astype(str)
                .str.upper()
                .str.contains(
                    interaction_type_filter.strip().upper(),
                    na=False
                )
            ]


st.caption(
    f"Showing {len(filtered_interactions)} interaction(s)"
)
if filtered_interactions.empty:

    st.info(
        "No interactions found for the selected filters."
    )

else:

    st.markdown("### 💬 Customer Conversations")

    for index, row in filtered_interactions.iterrows():

        customer_id = str(
            row.get("CUSTOMER_ID", "UNKNOWN")
        )

        interaction_type = str(
            row.get("INTERACTION_TYPE", "Interaction")
        )

        interaction_date = str(
            row.get("INTERACTION_DATE", "Date unavailable")
        )

        interaction_id = str(
            row.get("INTERACTION_ID", index)
        )

        transcript = row.get(
            "TRANSCRIPT",
            ""
        )

        if pd.isna(transcript):
            transcript = ""

        transcript = str(transcript).strip()


        with st.container(border=True):

            header_col1, header_col2, header_col3 = st.columns(
                [2, 2, 1]
            )

            with header_col1:

                st.markdown(
                    f"**Customer:** `{customer_id}`"
                )

            with header_col2:

                st.markdown(
                    f"**Type:** {interaction_type}"
                )

            with header_col3:

                st.caption(
                    f"ID: {interaction_id}"
                )


            st.caption(
                f"📅 {interaction_date}"
            )


            if transcript:

                with st.expander(
                    "📄 View Transcript",
                    expanded=False
                ):

                    st.write(transcript)

            else:

                st.warning(
                    "No transcript available for this interaction."
                )

            matching_insights = pd.DataFrame()

            if not insights_df.empty:

                matching_insights = insights_df.copy()

                if (
                    "INTERACTION_ID" in insights_df.columns
                    and "INTERACTION_ID" in interactions_df.columns
                ):

                    matching_insights = insights_df[
                        insights_df["INTERACTION_ID"].astype(str)
                        == str(interaction_id)
                    ]


                elif "CUSTOMER_ID" in insights_df.columns:

                    matching_insights = insights_df[
                        insights_df["CUSTOMER_ID"].astype(str)
                        == customer_id
                    ]

            if matching_insights.empty:

                st.caption(
                    "🤖 No AI insight available for this interaction."
                )

            else:

                insight = matching_insights.iloc[0]

                st.markdown("**🤖 AI Extracted Insights**")

                insight_col1, insight_col2, insight_col3, insight_col4 = (
                    st.columns(4)
                )


                with insight_col1:

                    st.metric(
                        "Sentiment",
                        insight.get(
                            "SENTIMENT",
                            "UNKNOWN"
                        )
                    )


                with insight_col2:

                    st.metric(
                        "Intent",
                        insight.get(
                            "INTENT",
                            "UNKNOWN"
                        )
                    )


                with insight_col3:

                    st.metric(
                        "Churn Signal",
                        insight.get(
                            "CHURN_SIGNAL",
                            "UNKNOWN"
                        )
                    )


                with insight_col4:

                    st.metric(
                        "Urgency",
                        insight.get(
                            "URGENCY",
                            "UNKNOWN"
                        )
                    )


                # Confidence

                if "CONFIDENCE" in matching_insights.columns:

                    confidence = insight.get(
                        "CONFIDENCE"
                    )

                    if pd.notna(confidence):

                        st.progress(
                            min(
                                max(float(confidence), 0),
                                1
                            ),
                            text=f"AI Confidence: {float(confidence):.0%}"
                        )


                # Topic

                if "TOPIC" in matching_insights.columns:

                    topic = insight.get("TOPIC")

                    if pd.notna(topic):

                        st.caption(
                            f"Topic: **{topic}**"
                        )


st.markdown("---")

st.subheader("🤖 AI Insights Overview")


if insights_df.empty:

    st.info(
        "No AI insights are currently available in Snowflake."
    )

else:

    if "SENTIMENT" in insights_df.columns:

        st.markdown("#### Sentiment Distribution")

        sentiment_counts = (
            insights_df["SENTIMENT"]
            .fillna("UNKNOWN")
            .astype(str)
            .value_counts()
            .reset_index()
        )

        sentiment_counts.columns = [
            "Sentiment",
            "Interactions"
        ]

        st.dataframe(
            sentiment_counts,
            use_container_width=True,
            hide_index=True
        )

    if "CHURN_SIGNAL" in insights_df.columns:

        st.markdown("#### Churn Signal Distribution")

        churn_counts = (
            insights_df["CHURN_SIGNAL"]
            .fillna("UNKNOWN")
            .astype(str)
            .value_counts()
            .reset_index()
        )

        churn_counts.columns = [
            "Churn Signal",
            "Customers / Interactions"
        ]

        st.dataframe(
            churn_counts,
            use_container_width=True,
            hide_index=True
        )

    with st.expander("📊 View AI Insight Records"):

        st.dataframe(
            insights_df,
            use_container_width=True,
            hide_index=True
        )
st.markdown("---")

st.subheader("🩺 Transcript & AI Data Quality")


if interactions_df.empty:

    st.info("No interaction data available to validate.")

else:

    quality_col1, quality_col2, quality_col3 = st.columns(3)

    missing_transcripts = 0

    if "TRANSCRIPT" in interactions_df.columns:

        missing_transcripts = (
            interactions_df["TRANSCRIPT"]
            .fillna("")
            .astype(str)
            .str.strip()
            .eq("")
            .sum()
        )


    with quality_col1:

        st.metric(
            "Missing Transcripts",
            missing_transcripts
        )

    interactions_without_insight = 0

    if (
        "INTERACTION_ID" in interactions_df.columns
        and "INTERACTION_ID" in insights_df.columns
    ):

        interaction_ids = set(
            interactions_df["INTERACTION_ID"]
            .astype(str)
        )

        insight_ids = set(
            insights_df["INTERACTION_ID"]
            .astype(str)
        )

        interactions_without_insight = len(
            interaction_ids - insight_ids
        )


    with quality_col2:

        st.metric(
            "Without AI Insight",
            interactions_without_insight
        )

    with quality_col3:

        st.metric(
            "AI Insight Records",
            len(insights_df)
        )


st.caption(
    "Data shown above is read directly from Snowflake. "
    "AI processing will be connected to the transcript pipeline separately."
)