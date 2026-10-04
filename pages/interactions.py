
import streamlit as st
import pandas as pd

from utils.security import enforce_employee_boundary

from services.snowflake_service import (
    get_all_interactions,
    get_all_ai_insights,
    get_all_policy_feedback,
    upsert_customer_insight,
)

from services.ai_service import process_transcript_to_insights
enforce_employee_boundary()

st.markdown("""
<style>

    /* =====================================================
       ROOT / GLOBAL
       ===================================================== */

    html, body, [data-testid="stAppViewContainer"] {
        background:
            radial-gradient(
                circle at 85% 5%,
                rgba(37, 99, 235, 0.14),
                transparent 28%
            ),
            radial-gradient(
                circle at 10% 25%,
                rgba(20, 184, 166, 0.09),
                transparent 25%
            ),
            #07111f !important;
    }

    [data-testid="stAppViewContainer"] {
        color: #e5edf7 !important;
    }

    [data-testid="stHeader"] {
        background: transparent !important;
    }

    [data-testid="stToolbar"] {
        background: transparent !important;
    }


    /* =====================================================
       MAIN CONTENT
       ===================================================== */

    .block-container {
        max-width: 1450px !important;
        padding-top: 2rem !important;
        padding-bottom: 4rem !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
    }


    /* =====================================================
       HEADINGS
       ===================================================== */

    h1, h2, h3, h4, h5 {
        color: #f8fafc !important;
        letter-spacing: -0.02em !important;
    }

    h1 {
        font-size: 2.2rem !important;
        font-weight: 800 !important;

        background:
            linear-gradient(
                90deg,
                #ffffff 0%,
                #dbeafe 45%,
                #67e8f9 100%
            );

        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    h2 {
        font-size: 1.55rem !important;
        font-weight: 750 !important;
        margin-top: 1rem !important;
    }

    h3 {
        font-size: 1.25rem !important;
        font-weight: 700 !important;
    }

    h4 {
        font-size: 1.05rem !important;
    }

    p {
        color: #aebed0 !important;
    }

    label {
        color: #aebed0 !important;
    }

    [data-testid="stCaptionContainer"] {
        color: #8195aa !important;
    }


    /* =====================================================
       METRIC CARDS
       ===================================================== */

    [data-testid="stMetric"] {
        background:
            linear-gradient(
                145deg,
                rgba(15, 31, 52, 0.97),
                rgba(8, 22, 38, 0.97)
            ) !important;

        border: 1px solid
            rgba(71, 102, 138, 0.34) !important;

        border-radius: 16px !important;

        padding: 18px 20px !important;

        min-height: 105px !important;

        box-shadow:
            0 10px 30px rgba(0, 0, 0, 0.25),
            inset 0 1px 0 rgba(255, 255, 255, 0.035) !important;

        transition:
            transform 0.2s ease,
            border-color 0.2s ease,
            box-shadow 0.2s ease !important;
    }

    [data-testid="stMetric"]:hover {
        transform: translateY(-3px) !important;

        border-color:
            rgba(45, 212, 191, 0.60) !important;

        box-shadow:
            0 15px 35px rgba(0, 0, 0, 0.32),
            0 0 22px rgba(20, 184, 166, 0.10) !important;
    }

    [data-testid="stMetricLabel"] {
        color: #8fa4bb !important;
        font-size: 0.82rem !important;
        font-weight: 650 !important;
    }

    [data-testid="stMetricValue"] {
        color: #f8fafc !important;
        font-size: 1.65rem !important;
        font-weight: 800 !important;
    }


    /* =====================================================
       DIVIDERS
       ===================================================== */

    hr {
        border: 0 !important;
        height: 1px !important;

        background:
            linear-gradient(
                90deg,
                transparent,
                rgba(71, 102, 138, 0.55),
                transparent
            ) !important;

        margin: 30px 0 !important;
    }


    /* =====================================================
       TEXT INPUTS
       ===================================================== */

    div[data-baseweb="input"] {
        background:
            rgba(11, 27, 45, 0.95) !important;

        border: 1px solid
            rgba(71, 102, 138, 0.45) !important;

        border-radius: 10px !important;

        box-shadow: none !important;

        transition:
            border-color 0.2s ease,
            box-shadow 0.2s ease !important;
    }

    div[data-baseweb="input"]:focus-within {
        border-color:
            rgba(45, 212, 191, 0.75) !important;

        box-shadow:
            0 0 0 2px rgba(20, 184, 166, 0.10) !important;
    }

    div[data-baseweb="input"] input {
        color: #e5edf7 !important;
        background: transparent !important;
    }

    div[data-baseweb="input"] input::placeholder {
        color: #64748b !important;
    }


    /* =====================================================
       TEXT AREA
       ===================================================== */

    textarea {
        background:
            rgba(11, 27, 45, 0.95) !important;

        color: #e5edf7 !important;

        border: 1px solid
            rgba(71, 102, 138, 0.45) !important;

        border-radius: 10px !important;
    }

    textarea:focus {
        border-color:
            rgba(45, 212, 191, 0.75) !important;

        box-shadow:
            0 0 0 2px rgba(20, 184, 166, 0.10) !important;
    }


    /* =====================================================
       INTERACTION CARDS
       ===================================================== */

    [data-testid="stVerticalBlockBorderWrapper"] {
        background:
            linear-gradient(
                145deg,
                rgba(15, 31, 52, 0.96),
                rgba(8, 22, 38, 0.96)
            ) !important;

        border: 1px solid
            rgba(71, 102, 138, 0.32) !important;

        border-radius: 16px !important;

        box-shadow:
            0 10px 28px rgba(0, 0, 0, 0.22) !important;

        padding: 6px !important;

        margin-bottom: 16px !important;

        transition:
            border-color 0.2s ease,
            transform 0.2s ease,
            box-shadow 0.2s ease !important;
    }

    [data-testid="stVerticalBlockBorderWrapper"]:hover {
        border-color:
            rgba(45, 212, 191, 0.42) !important;

        transform: translateY(-1px) !important;

        box-shadow:
            0 15px 35px rgba(0, 0, 0, 0.30),
            0 0 22px rgba(20, 184, 166, 0.06) !important;
    }


    /* =====================================================
       BUTTONS
       ===================================================== */

    .stButton > button {
        width: 100% !important;

        min-height: 42px !important;

        background:
            linear-gradient(
                135deg,
                #0f766e 0%,
                #0891b2 100%
            ) !important;

        color: #ffffff !important;

        border: 1px solid
            rgba(103, 232, 249, 0.22) !important;

        border-radius: 9px !important;

        font-weight: 700 !important;

        box-shadow:
            0 7px 18px rgba(8, 145, 178, 0.18) !important;

        transition:
            transform 0.18s ease,
            box-shadow 0.18s ease,
            filter 0.18s ease !important;
    }

    .stButton > button:hover {
        color: #ffffff !important;

        filter: brightness(1.10) !important;

        transform: translateY(-1px) !important;

        box-shadow:
            0 11px 26px rgba(8, 145, 178, 0.28) !important;
    }

    .stButton > button:active {
        transform: translateY(0) !important;
    }


    /* =====================================================
       EXPANDERS
       ===================================================== */

    [data-testid="stExpander"] {
        background:
            rgba(10, 28, 47, 0.92) !important;

        border: 1px solid
            rgba(71, 102, 138, 0.35) !important;

        border-radius: 12px !important;

        overflow: hidden !important;

        margin-top: 10px !important;
    }

    [data-testid="stExpander"]:hover {
        border-color:
            rgba(45, 212, 191, 0.45) !important;
    }

    [data-testid="stExpander"] summary {
        color: #dce8f5 !important;
        font-weight: 650 !important;
    }


    /* =====================================================
       SELECTBOX
       ===================================================== */

    div[data-baseweb="select"] > div {
        background:
            rgba(11, 27, 45, 0.95) !important;

        border: 1px solid
            rgba(71, 102, 138, 0.45) !important;

        border-radius: 10px !important;
    }

    div[data-baseweb="select"] span {
        color: #dbeafe !important;
    }


    /* =====================================================
       PROGRESS BAR
       ===================================================== */

    [data-testid="stProgress"] {
        margin-top: 10px !important;
    }

    [data-testid="stProgress"] > div {
        background:
            rgba(51, 65, 85, 0.55) !important;

        border-radius: 999px !important;
    }

    [data-testid="stProgress"] [role="progressbar"] {
        background:
            linear-gradient(
                90deg,
                #0f766e,
                #06b6d4,
                #67e8f9
            ) !important;

        border-radius: 999px !important;
    }


    /* =====================================================
       ALERTS
       ===================================================== */

    [data-testid="stAlert"] {
        border-radius: 12px !important;

        border: 1px solid
            rgba(71, 102, 138, 0.32) !important;

        background:
            rgba(12, 29, 48, 0.94) !important;
    }

    [data-testid="stAlert"] p {
        color: #d8e5f2 !important;
    }


    /* =====================================================
       DATAFRAME
       ===================================================== */

    [data-testid="stDataFrame"] {
        border: 1px solid
            rgba(71, 102, 138, 0.32) !important;

        border-radius: 12px !important;

        overflow: hidden !important;

        box-shadow:
            0 8px 25px rgba(0, 0, 0, 0.20) !important;
    }


    /* =====================================================
       CODE / CUSTOMER IDS
       ===================================================== */

    code {
        color: #67e8f9 !important;

        background:
            rgba(8, 47, 73, 0.60) !important;

        border: 1px solid
            rgba(34, 211, 238, 0.15) !important;

        border-radius: 6px !important;

        padding: 2px 7px !important;
    }


    /* =====================================================
       SPINNER
       ===================================================== */

    [data-testid="stSpinner"] {
        color: #67e8f9 !important;
    }


    /* =====================================================
       SIDEBAR
       ===================================================== */

    [data-testid="stSidebar"] {
        background:
            linear-gradient(
                180deg,
                #081525 0%,
                #06101d 100%
            ) !important;

        border-right:
            1px solid rgba(71, 102, 138, 0.25) !important;
    }


    /* =====================================================
       SCROLLBAR
       ===================================================== */

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
        background: #36536f;
    }


    /* =====================================================
       MOBILE
       ===================================================== */

    @media (max-width: 900px) {

        .block-container {
            padding-left: 1rem !important;
            padding-right: 1rem !important;
        }

        h1 {
            font-size: 1.75rem !important;
        }

        [data-testid="stMetric"] {
            min-height: 90px !important;
            padding: 14px !important;
        }

    }

</style>
""", unsafe_allow_html=True)


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

                if transcript:
                    if st.button(
                        "🧠 Analyze with Cortex",
                        key=f"analyze_cortex_{interaction_id}",
                    ):
                        with st.spinner("Analyzing transcript with Cortex..."):
                            result = process_transcript_to_insights(
                                transcript
                            )

                        if result.get("status") == "SUCCESS":
                            saved = upsert_customer_insight(
                                customer_id=customer_id,
                                interaction_id=interaction_id,
                                sentiment=result.get(
                                    "sentiment",
                                    "UNKNOWN",
                                ),
                                intent=result.get(
                                    "intent",
                                    "UNKNOWN",
                                ),
                                topic=result.get(
                                    "topic",
                                    "UNKNOWN",
                                ),
                                churn_signal=result.get(
                                    "churn_signal",
                                    "UNKNOWN",
                                ),
                                urgency=result.get(
                                    "urgency",
                                    "UNKNOWN",
                                ),
                                confidence=result.get(
                                    "confidence"
                                ),
                            )

                            if saved:
                                st.success(
                                    "AI insight generated successfully."
                                )
                                st.rerun()
                        else:
                            st.warning(
                                "Cortex could not generate a valid insight: "
                                f"{result.get('evidence', 'Unknown error')}"
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

                if transcript:
                    if st.button(
                        "🔄 Re-analyze with Cortex",
                        key=f"reanalyze_cortex_{interaction_id}",
                    ):
                        with st.spinner("Re-analyzing transcript with Cortex..."):
                            result = process_transcript_to_insights(
                                transcript
                            )

                        if result.get("status") == "SUCCESS":
                            saved = upsert_customer_insight(
                                customer_id=customer_id,
                                interaction_id=interaction_id,
                                sentiment=result.get(
                                    "sentiment",
                                    "UNKNOWN",
                                ),
                                intent=result.get(
                                    "intent",
                                    "UNKNOWN",
                                ),
                                topic=result.get(
                                    "topic",
                                    "UNKNOWN",
                                ),
                                churn_signal=result.get(
                                    "churn_signal",
                                    "UNKNOWN",
                                ),
                                urgency=result.get(
                                    "urgency",
                                    "UNKNOWN",
                                ),
                                confidence=result.get(
                                    "confidence"
                                ),
                            )

                            if saved:
                                st.success(
                                    "AI insight updated successfully."
                                )
                                st.rerun()
                        else:
                            st.warning(
                                "Cortex could not generate a valid insight: "
                                f"{result.get('evidence', 'Unknown error')}"
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
