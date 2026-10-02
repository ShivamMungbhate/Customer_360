
import streamlit as st
import pandas as pd

from utils.security import enforce_employee_boundary

from services.snowflake_service import (
    get_all_interactions,
    get_all_ai_insights,
    get_all_policy_feedback,
)
enforce_employee_boundary()

st.title("💬 Interactions & AI Insights")

st.write(
    "Review customer conversations, call transcripts, "
    "customer policy feedback, and AI-extracted structured insights."
)


interactions_df = get_all_interactions()
insights_df = get_all_ai_insights()
feedback_df = get_all_policy_feedback()

total_interactions = len(interactions_df)
total_insights = len(insights_df)
total_feedback = len(feedback_df)

transcript_count = 0

if (
    not interactions_df.empty
    and "TRANSCRIPT" in interactions_df.columns
):

    transcript_count = (
        interactions_df["TRANSCRIPT"]
        .fillna("")
        .astype(str)
        .str.strip()
        .ne("")
        .sum()
    )


unique_customers = 0

if (
    not interactions_df.empty
    and "CUSTOMER_ID" in interactions_df.columns
):

    unique_customers = (
        interactions_df["CUSTOMER_ID"]
        .dropna()
        .astype(str)
        .nunique()
    )


col1, col2, col3, col4, col5 = st.columns(5)

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

with col5:

    st.metric(
        "Policy Feedback",
        total_feedback
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
            row.get(
                "CUSTOMER_ID",
                "UNKNOWN"
            )
        )

        interaction_type = str(
            row.get(
                "INTERACTION_TYPE",
                "Interaction"
            )
        )

        interaction_date = str(
            row.get(
                "INTERACTION_DATE",
                "Date unavailable"
            )
        )

        interaction_id = str(
            row.get(
                "INTERACTION_ID",
                index
            )
        )

        transcript = row.get(
            "TRANSCRIPT",
            ""
        )


        if pd.isna(transcript):

            transcript = ""


        transcript = str(
            transcript
        ).strip()

        with st.container(border=True):

            header_col1, header_col2, header_col3 = (
                st.columns([2, 2, 1])
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

                    st.write(
                        transcript
                    )

            else:

                st.warning(
                    "No transcript available for this interaction."
                )

            matching_insights = pd.DataFrame()


            if not insights_df.empty:

                if (
                    "INTERACTION_ID" in insights_df.columns
                    and "INTERACTION_ID" in interactions_df.columns
                ):

                    matching_insights = insights_df[
                        insights_df["INTERACTION_ID"]
                        .astype(str)
                        == str(interaction_id)
                    ]

                elif "CUSTOMER_ID" in insights_df.columns:

                    matching_insights = insights_df[
                        insights_df["CUSTOMER_ID"]
                        .astype(str)
                        .str.upper()
                        == customer_id.upper()
                    ]

            if matching_insights.empty:

                st.caption(
                    "🤖 No AI insight available for this interaction."
                )

            else:

                insight = matching_insights.iloc[0]

                st.markdown(
                    "**🤖 AI Extracted Insights**"
                )


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

                if "CONFIDENCE" in matching_insights.columns:

                    confidence = insight.get(
                        "CONFIDENCE"
                    )

                    if pd.notna(confidence):

                        try:

                            confidence_value = float(
                                confidence
                            )
                            if confidence_value > 1:

                                confidence_value = (
                                    confidence_value / 100
                                )


                            confidence_value = min(
                                max(
                                    confidence_value,
                                    0
                                ),
                                1
                            )


                            st.progress(
                                confidence_value,
                                text=(
                                    f"AI Confidence: "
                                    f"{confidence_value:.0%}"
                                )
                            )

                        except (
                            ValueError,
                            TypeError
                        ):

                            pass

                if "TOPIC" in matching_insights.columns:

                    topic = insight.get(
                        "TOPIC"
                    )

                    if pd.notna(topic):

                        st.caption(
                            f"Topic: **{topic}**"
                        )


st.markdown("---")

st.subheader("⭐ Customer Policy Feedback")

st.write(
    "Feedback submitted by customers for their insurance policies. "
    "This information is displayed for employee reference and "
    "is not used for AI analysis."
)


feedback_filter_col1, feedback_filter_col2 = st.columns(
    [1, 2]
)


with feedback_filter_col1:

    feedback_customer_filter = st.text_input(
        "Customer ID",
        placeholder="Example: C001",
        key="feedback_customer_filter"
    )


with feedback_filter_col2:

    feedback_policy_filter = st.text_input(
        "Policy ID",
        placeholder="Example: POL-1001",
        key="feedback_policy_filter"
    )


filtered_feedback = feedback_df.copy()


if not filtered_feedback.empty:

    if feedback_customer_filter:

        if "CUSTOMER_ID" in filtered_feedback.columns:

            filtered_feedback = filtered_feedback[
                filtered_feedback["CUSTOMER_ID"]
                .astype(str)
                .str.upper()
                .str.contains(
                    feedback_customer_filter.strip().upper(),
                    na=False
                )
            ]

    if feedback_policy_filter:

        if "POLICY_ID" in filtered_feedback.columns:

            filtered_feedback = filtered_feedback[
                filtered_feedback["POLICY_ID"]
                .astype(str)
                .str.upper()
                .str.contains(
                    feedback_policy_filter.strip().upper(),
                    na=False
                )
            ]


st.caption(
    f"Showing {len(filtered_feedback)} feedback record(s)"
)

if filtered_feedback.empty:

    st.info(
        "No policy feedback found for the selected filters."
    )

else:

    for feedback_index, feedback in (
        filtered_feedback.iterrows()
    ):

        customer_id = str(
            feedback.get(
                "CUSTOMER_ID",
                "UNKNOWN"
            )
        )

        policy_id = str(
            feedback.get(
                "POLICY_ID",
                "UNKNOWN"
            )
        )

        feedback_id = str(
            feedback.get(
                "FEEDBACK_ID",
                feedback_index
            )
        )

        rating = feedback.get(
            "RATING",
            None
        )

        category = str(
            feedback.get(
                "CATEGORY",
                "Other"
            )
        )

        comments = feedback.get(
            "COMMENTS",
            ""
        )

        recommendation = str(
            feedback.get(
                "RECOMMENDATION",
                "UNKNOWN"
            )
        )

        created_at = feedback.get(
            "CREATED_AT",
            "Date unavailable"
        )


        if pd.isna(comments):

            comments = ""

        else:

            comments = str(
                comments
            ).strip()


        with st.container(border=True):

            feedback_header_col1, feedback_header_col2, feedback_header_col3 = (
                st.columns([2, 2, 1])
            )


            with feedback_header_col1:

                st.markdown(
                    f"**Customer:** `{customer_id}`"
                )

                st.caption(
                    f"Policy: `{policy_id}`"
                )


            with feedback_header_col2:

                if pd.notna(rating):

                    try:

                        rating_int = int(
                            rating
                        )

                        rating_int = min(
                            max(
                                rating_int,
                                1
                            ),
                            5
                        )

                        stars = (
                            "⭐" * rating_int
                        )

                        st.markdown(
                            f"**Rating:** "
                            f"{stars} "
                            f"({rating_int}/5)"
                        )

                    except (
                        ValueError,
                        TypeError
                    ):

                        st.markdown(
                            "**Rating:** Not available"
                        )

                else:

                    st.markdown(
                        "**Rating:** Not available"
                    )


                st.caption(
                    f"Category: **{category}**"
                )


            with feedback_header_col3:

                st.caption(
                    f"Feedback ID: {feedback_id}"
                )

                st.caption(
                    f"Submitted: {created_at}"
                )

            if comments:

                st.markdown(
                    "💬 **Customer Feedback**"
                )

                st.write(
                    comments
                )

            else:

                st.caption(
                    "No written comment provided."
                )

            if recommendation.upper() == "YES":

                st.success(
                    "Customer would recommend this policy."
                )

            elif recommendation.upper() == "NO":

                st.warning(
                    "Customer would not recommend this policy."
                )

            else:

                st.caption(
                    f"Recommendation: {recommendation}"
                )


            st.caption(
                "ℹ️ This policy feedback is displayed for "
                "employee reference only and is not used "
                "for AI analysis."
            )


st.markdown("---")

st.subheader("🤖 AI Insights Overview")


if insights_df.empty:

    st.info(
        "No AI insights are currently available in Snowflake."
    )

else:

    if "SENTIMENT" in insights_df.columns:

        st.markdown(
            "#### Sentiment Distribution"
        )

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

        st.markdown(
            "#### Churn Signal Distribution"
        )

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


    with st.expander(
        "📊 View AI Insight Records"
    ):

        st.dataframe(
            insights_df,
            use_container_width=True,
            hide_index=True
        )

st.markdown("---")

st.subheader(
    "🩺 Transcript & AI Data Quality"
)


if interactions_df.empty:

    st.info(
        "No interaction data available to validate."
    )

else:

    quality_col1, quality_col2, quality_col3 = (
        st.columns(3)
    )

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

st.markdown("---")

st.caption(
    "Interaction and policy feedback data is read directly "
    "from Snowflake. Customer policy feedback is displayed "
    "for employee reference and is kept separate from "
    "the AI insight analysis pipeline."
)