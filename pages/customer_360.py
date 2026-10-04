
import streamlit as st
import pandas as pd

from services.snowflake_service import (
    get_customer_profile,
    get_customer_policies,
    get_customer_claims,
    get_customer_interactions,
    get_ai_insights,
)

from services.ai_service import generate_customer_ai_summary

st.set_page_config(
    page_title="Customer 360 View",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>

    @import url(
        'https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap'
    );

    /* =====================================================
       GLOBAL APP
       ===================================================== */

    .stApp {
        background:
            radial-gradient(
                circle at 5% 0%,
                rgba(37, 99, 235, 0.14),
                transparent 30%
            ),
            radial-gradient(
                circle at 95% 5%,
                rgba(124, 58, 237, 0.12),
                transparent 28%
            ),
            linear-gradient(
                135deg,
                #070b14 0%,
                #0b1220 48%,
                #080d18 100%
            );

        color: #e5e7eb;
        font-family: 'Inter', sans-serif;
    }


    /* =====================================================
       MAIN CONTAINER
       ===================================================== */

    [data-testid="stMainBlockContainer"] {
        max-width: 1500px;
        padding-top: 2.2rem;
        padding-bottom: 4rem;
    }


    /* =====================================================
       HEADINGS
       ===================================================== */

    h1 {
        font-size: clamp(2rem, 4vw, 2.8rem) !important;
        font-weight: 800 !important;
        letter-spacing: -1.4px;
        line-height: 1.2 !important;

        background:
            linear-gradient(
                100deg,
                #ffffff 5%,
                #93c5fd 52%,
                #c4b5fd 95%
            );

        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;

        margin-bottom: 0.35rem !important;
    }

    h2 {
        color: #f8fafc !important;
        font-weight: 750 !important;
        letter-spacing: -0.7px;
        margin-top: 2rem !important;
    }

    h3 {
        color: #e2e8f0 !important;
        font-weight: 700 !important;
        letter-spacing: -0.4px;
    }

    h4,
    h5,
    h6 {
        color: #dbeafe !important;
        font-weight: 650 !important;
    }

    p {
        color: #aebbd0;
        line-height: 1.65;
    }

    [data-testid="stCaptionContainer"] {
        color: #7f8da3 !important;
    }


    /* =====================================================
       METRIC CARDS
       ===================================================== */

    [data-testid="stMetric"] {
        position: relative;

        background:
            linear-gradient(
                145deg,
                rgba(23, 36, 61, 0.96),
                rgba(12, 21, 37, 0.96)
            );

        border: 1px solid rgba(96, 165, 250, 0.18);
        border-radius: 17px;

        padding: 18px 18px;

        min-height: 108px;

        box-shadow:
            0 10px 30px rgba(0, 0, 0, 0.18),
            inset 0 1px 0 rgba(255, 255, 255, 0.025);

        overflow: hidden;

        transition:
            transform 0.22s ease,
            border-color 0.22s ease,
            box-shadow 0.22s ease;
    }

    [data-testid="stMetric"]::before {
        content: "";

        position: absolute;

        top: 0;
        left: 0;
        right: 0;

        height: 2px;

        background:
            linear-gradient(
                90deg,
                #2563eb,
                #6366f1,
                #8b5cf6
            );

        opacity: 0.7;
    }

    [data-testid="stMetric"]:hover {
        transform: translateY(-4px);

        border-color: rgba(96, 165, 250, 0.45);

        box-shadow:
            0 15px 38px rgba(0, 0, 0, 0.25),
            0 0 24px rgba(59, 130, 246, 0.08);
    }

    [data-testid="stMetricLabel"] {
        color: #94a3b8 !important;
        font-size: 0.74rem !important;
        font-weight: 600 !important;
        text-transform: uppercase;
        letter-spacing: 0.45px;
    }

    [data-testid="stMetricValue"] {
        color: #f8fafc !important;
        font-size: 1.55rem !important;
        font-weight: 800 !important;
    }

    [data-testid="stMetricDelta"] {
        font-size: 0.78rem !important;
    }


    /* =====================================================
       SEARCH INPUT
       ===================================================== */

    [data-testid="stTextInput"] input {
        background:
            rgba(15, 23, 42, 0.88) !important;

        color: #f8fafc !important;

        border: 1px solid
            rgba(96, 165, 250, 0.24) !important;

        border-radius: 12px !important;

        min-height: 46px;

        padding: 0 15px !important;

        transition:
            border-color 0.2s ease,
            box-shadow 0.2s ease;
    }

    [data-testid="stTextInput"] input:focus {
        border-color:
            rgba(96, 165, 250, 0.7) !important;

        box-shadow:
            0 0 0 3px
            rgba(59, 130, 246, 0.12) !important;
    }

    [data-testid="stTextInput"] label {
        color: #cbd5e1 !important;
        font-weight: 600 !important;
    }

    [data-testid="stTextInput"] input::placeholder {
        color: #64748b !important;
    }


    /* =====================================================
       BUTTONS
       ===================================================== */

    .stButton > button {
        background:
            linear-gradient(
                110deg,
                #2563eb 0%,
                #4f46e5 55%,
                #7c3aed 100%
            );

        color: #ffffff !important;

        border: 1px solid
            rgba(147, 197, 253, 0.25);

        border-radius: 11px;

        min-height: 43px;

        font-weight: 650;

        box-shadow:
            0 6px 18px
            rgba(37, 99, 235, 0.18);

        transition:
            transform 0.2s ease,
            box-shadow 0.2s ease,
            filter 0.2s ease;
    }

    .stButton > button:hover {
        filter: brightness(1.08);

        transform: translateY(-2px);

        box-shadow:
            0 9px 25px
            rgba(59, 130, 246, 0.28);

        border-color:
            rgba(191, 219, 254, 0.5);
    }

    .stButton > button:active {
        transform: translateY(0);
    }


    /* =====================================================
       ALERTS
       ===================================================== */

    [data-testid="stAlert"] {
        border-radius: 13px;

        border: 1px solid
            rgba(96, 165, 250, 0.20);

        background:
            linear-gradient(
                135deg,
                rgba(30, 64, 175, 0.10),
                rgba(30, 41, 59, 0.28)
            );

        color: #dbeafe;
    }


    /* =====================================================
       DATAFRAMES
       ===================================================== */

    [data-testid="stDataFrame"] {
        border: 1px solid
            rgba(71, 85, 105, 0.45);

        border-radius: 15px;

        overflow: hidden;

        background:
            rgba(10, 17, 30, 0.78);

        box-shadow:
            0 10px 28px
            rgba(0, 0, 0, 0.15);
    }


    /* =====================================================
       EXPANDERS
       ===================================================== */

    [data-testid="stExpander"] {
        background:
            linear-gradient(
                145deg,
                rgba(17, 29, 49, 0.92),
                rgba(10, 18, 32, 0.92)
            );

        border: 1px solid
            rgba(71, 85, 105, 0.42);

        border-radius: 15px;

        overflow: hidden;

        margin-bottom: 10px;

        box-shadow:
            0 8px 24px
            rgba(0, 0, 0, 0.12);
    }

    [data-testid="stExpander"] summary {
        color: #e2e8f0 !important;
        font-weight: 650 !important;
    }

    [data-testid="stExpander"] summary:hover {
        color: #93c5fd !important;
    }


    /* =====================================================
       DIVIDERS
       ===================================================== */

    hr {
        border: none !important;

        height: 1px !important;

        background:
            linear-gradient(
                90deg,
                transparent,
                rgba(96, 165, 250, 0.25),
                rgba(139, 92, 246, 0.25),
                transparent
            ) !important;

        margin: 2rem 0 !important;
    }


    /* =====================================================
       COLUMNS
       ===================================================== */

    [data-testid="stHorizontalBlock"] {
        gap: 1rem;
    }


    /* =====================================================
       SPINNER
       ===================================================== */

    [data-testid="stSpinner"] {
        color: #93c5fd !important;
    }


    /* =====================================================
       CODE
       ===================================================== */

    code {
        color: #93c5fd !important;

        background:
            rgba(30, 41, 59, 0.7);

        border: 1px solid
            rgba(96, 165, 250, 0.12);

        border-radius: 5px;

        padding: 2px 6px;
    }


    /* =====================================================
       SCROLLBAR
       ===================================================== */

    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }

    ::-webkit-scrollbar-track {
        background: #080d18;
    }

    ::-webkit-scrollbar-thumb {
        background: #334155;
        border-radius: 10px;
    }

    ::-webkit-scrollbar-thumb:hover {
        background: #475569;
    }


    /* =====================================================
       MOBILE
       ===================================================== */

    @media (max-width: 768px) {

        [data-testid="stMainBlockContainer"] {
            padding:
                1.2rem
                1rem
                2.5rem;
        }

        h1 {
            font-size: 1.85rem !important;
            letter-spacing: -0.8px;
        }

        h2 {
            font-size: 1.35rem !important;
        }

        h3 {
            font-size: 1.15rem !important;
        }

        [data-testid="stMetric"] {
            min-height: 95px;
            padding: 14px;
            border-radius: 14px;
        }

        [data-testid="stMetricValue"] {
            font-size: 1.35rem !important;
        }

        [data-testid="stDataFrame"] {
            border-radius: 11px;
        }
    }


    /* =====================================================
       ACCESSIBILITY
       ===================================================== */

    @media (prefers-reduced-motion: reduce) {

        *,
        *::before,
        *::after {
            transition: none !important;
            animation: none !important;
        }
    }

    </style>
    """,
    unsafe_allow_html=True,
)

st.title("🔍 Customer 360 View")

st.caption(
    "Live customer intelligence from Snowflake — "
    "profile, policies, claims, interactions and AI insights."
)

search_col1, search_col2 = st.columns([4, 1])

with search_col1:
    customer_id_input = st.text_input(
        "Search Customer ID",
        placeholder="Example: C001",
        key="customer_search_input",
    )

with search_col2:
    st.markdown("<br>", unsafe_allow_html=True)

    search_clicked = st.button(
        "🔎 Search Customer",
        type="primary",
        use_container_width=True,
    )


if search_clicked:

    entered_customer_id = (
        str(customer_id_input)
        .strip()
        .upper()
    )

    if not entered_customer_id:
        st.warning(
            "Please enter a Customer ID."
        )
        st.stop()

    st.session_state[
        "selected_customer_id"
    ] = entered_customer_id


customer_id = st.session_state.get(
    "selected_customer_id",
    "",
)

if customer_id:

    profile_df = get_customer_profile(
        customer_id
    )

    if profile_df.empty:
        st.error(
            f"No customer record found in Snowflake "
            f"for `{customer_id}`."
        )
        st.stop()

    customer = profile_df.iloc[0]

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

    st.success(
        f"Customer found: {customer_name}"
    )

    st.markdown("---")


    st.subheader("👤 Customer Profile")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Customer ID",
            customer.get(
                "CUSTOMER_ID",
                customer_id,
            ),
        )

    with col2:
        st.metric(
            "Name",
            customer_name,
        )

    with col3:
        st.metric(
            "City",
            customer.get(
                "CITY",
                "N/A",
            ),
        )

    with col4:
        st.metric(
            "State",
            customer.get(
                "STATE",
                "N/A",
            ),
        )


    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Occupation",
            customer.get(
                "OCCUPATION",
                "N/A",
            ),
        )

    with col2:

        income = customer.get(
            "ANNUAL_INCOME"
        )

        if pd.notna(income):
            st.metric(
                "Annual Income",
                f"₹{float(income):,.0f}",
            )
        else:
            st.metric(
                "Annual Income",
                "N/A",
            )

    with col3:
        st.metric(
            "Age",
            customer.get(
                "AGE",
                "N/A",
            ),
        )

    st.markdown("---")
    st.subheader("🛡️ Policies")

    policies_df = get_customer_policies(
        customer_id
    )

    if policies_df.empty:

        st.info(
            "No policy records found."
        )

    else:

        if "STATUS" in policies_df.columns:

            active_count = (
                policies_df["STATUS"]
                .astype(str)
                .str.upper()
                .eq("ACTIVE")
                .sum()
            )

            st.caption(
                f"Total policies: {len(policies_df)} | "
                f"Active policies: {active_count}"
            )

        st.dataframe(
            policies_df,
            use_container_width=True,
            hide_index=True,
        )

    st.markdown("---")
    st.subheader("📑 Claims")

    claims_df = get_customer_claims(
        customer_id
    )

    if claims_df.empty:

        st.info(
            "No claim records found."
        )

    else:

        if "CLAIM_STATUS" in claims_df.columns:

            open_claims = (
                ~claims_df["CLAIM_STATUS"]
                .astype(str)
                .str.upper()
                .isin(
                    [
                        "CLOSED",
                        "SETTLED",
                        "REJECTED",
                    ]
                )
            ).sum()

            st.caption(
                f"Total claims: {len(claims_df)} | "
                f"Open claims: {open_claims}"
            )

        st.dataframe(
            claims_df,
            use_container_width=True,
            hide_index=True,
        )


    st.markdown("---")
    st.subheader(
        "💬 Interactions & Call Transcripts"
    )

    interactions_df = (
        get_customer_interactions(
            customer_id
        )
    )

    if interactions_df.empty:

        st.info(
            "No interaction records found."
        )

    else:

        st.caption(
            f"Total interactions: "
            f"{len(interactions_df)}"
        )

        for index, row in interactions_df.iterrows():

            interaction_type = str(
                row.get(
                    "INTERACTION_TYPE",
                    "Interaction",
                )
            )

            interaction_date = str(
                row.get(
                    "INTERACTION_DATE",
                    "Date unavailable",
                )
            )

            transcript = row.get(
                "TRANSCRIPT",
                "No transcript recorded.",
            )

            if pd.isna(transcript):
                transcript = (
                    "No transcript recorded."
                )

            with st.expander(
                f"💬 {interaction_type} "
                f"— {interaction_date}"
            ):

                st.markdown(
                    "**Transcript**"
                )

                st.write(
                    str(transcript)
                )

                extra_fields = []

                for field in [
                    "CHANNEL",
                    "AGENT_ID",
                    "INTERACTION_ID",
                ]:

                    if field in interactions_df.columns:

                        value = row.get(field)

                        if pd.notna(value):

                            extra_fields.append(
                                f"**"
                                f"{field.replace('_', ' ').title()}"
                                f":** {value}"
                            )

                if extra_fields:

                    st.markdown(
                        "  \n".join(
                            extra_fields
                        )
                    )


    st.markdown("---")
    st.subheader("🤖 AI Insights")

    insights_df = get_ai_insights(
        customer_id
    )

    if insights_df.empty:

        st.info(
            "No AI insights are available "
            "for this customer yet."
        )

    else:

        st.caption(
            f"AI insight records: "
            f"{len(insights_df)}"
        )

        insight = insights_df.iloc[0]

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "Sentiment",
                insight.get(
                    "SENTIMENT",
                    "UNKNOWN",
                ),
            )

        with col2:
            st.metric(
                "Intent",
                insight.get(
                    "INTENT",
                    "UNKNOWN",
                ),
            )

        with col3:
            st.metric(
                "Churn Signal",
                insight.get(
                    "CHURN_SIGNAL",
                    "UNKNOWN",
                ),
            )

        with col4:
            st.metric(
                "Urgency",
                insight.get(
                    "URGENCY",
                    "UNKNOWN",
                ),
            )


        st.markdown(
            "#### Insight Details"
        )

        insight_display = {}

        for field in [
            "SENTIMENT",
            "INTENT",
            "TOPIC",
            "CHURN_SIGNAL",
            "URGENCY",
            "CONFIDENCE",
            "GENERATED_AT",
        ]:

            if field in insights_df.columns:

                value = insight.get(
                    field
                )

                if pd.notna(value):

                    insight_display[
                        field
                        .replace("_", " ")
                        .title()
                    ] = value


        if insight_display:

            st.dataframe(
                pd.DataFrame(
                    list(
                        insight_display.items()
                    ),
                    columns=[
                        "Field",
                        "Value",
                    ],
                ),
                use_container_width=True,
                hide_index=True,
            )


        st.markdown(
            "#### Raw AI Insight Record"
        )

        st.dataframe(
            insights_df,
            use_container_width=True,
            hide_index=True,
        )


    st.markdown("---")
    st.subheader(
        "🧠 AI Customer Summary"
    )

    if insights_df.empty:

        st.info(
            "Generate at least one Cortex AI "
            "insight for this customer before "
            "creating an AI summary."
        )

    else:

        if st.button(
            "✨ Generate AI Summary",
            type="secondary",
            key=(
                f"generate_ai_summary_"
                f"{customer_id}"
            ),
        ):

            with st.spinner(
                "Generating customer summary with Cortex..."
            ):

                try:

                    customer_context_parts = [
                        (
                            f"Customer ID: "
                            f"{customer.get('CUSTOMER_ID', customer_id)}"
                        ),
                        (
                            f"Name: "
                            f"{customer_name}"
                        ),
                        (
                            f"Age: "
                            f"{customer.get('AGE', 'UNKNOWN')}"
                        ),
                        (
                            f"City: "
                            f"{customer.get('CITY', 'UNKNOWN')}"
                        ),
                        (
                            f"State: "
                            f"{customer.get('STATE', 'UNKNOWN')}"
                        ),
                        (
                            f"Occupation: "
                            f"{customer.get('OCCUPATION', 'UNKNOWN')}"
                        ),
                        (
                            f"Annual income: "
                            f"{customer.get('ANNUAL_INCOME', 'UNKNOWN')}"
                        ),
                        (
                            f"Policies: "
                            f"{len(policies_df)}"
                        ),
                        (
                            f"Claims: "
                            f"{len(claims_df)}"
                        ),
                        (
                            f"Interactions: "
                            f"{len(interactions_df)}"
                        ),
                    ]


                    if not policies_df.empty:

                        customer_context_parts.append(
                            "POLICIES:\n"
                            + policies_df.to_string(
                                index=False,
                                max_rows=10,
                            )
                        )


                    if not claims_df.empty:

                        customer_context_parts.append(
                            "CLAIMS:\n"
                            + claims_df.to_string(
                                index=False,
                                max_rows=10,
                            )
                        )


                    if not interactions_df.empty:

                        customer_context_parts.append(
                            "INTERACTIONS:\n"
                            + interactions_df.to_string(
                                index=False,
                                max_rows=10,
                            )
                        )


                    if not insights_df.empty:

                        customer_context_parts.append(
                            "CORTEX AI INSIGHTS:\n"
                            + insights_df.to_string(
                                index=False,
                                max_rows=10,
                            )
                        )


                    customer_context = (
                        "\n\n".join(
                            customer_context_parts
                        )
                    )


                    summary = (
                        generate_customer_ai_summary(
                            customer_context=(
                                customer_context
                            ),
                        )
                    )


                    if (
                        summary
                        and not summary.startswith("⚠️")
                    ):

                        st.success(
                            "AI customer summary generated."
                        )

                        st.write(
                            summary
                        )

                    elif summary:

                        st.error(
                            summary
                        )

                    else:

                        st.warning(
                            "Cortex did not return "
                            "a customer summary."
                        )


                except Exception as e:

                    st.error(
                        "Could not generate "
                        "AI customer summary: "
                        f"{type(e).__name__}: {e}"
                    )

    st.markdown("---")

    st.subheader(
        "📊 Customer 360 Summary"
    )

    summary_col1, summary_col2, summary_col3, summary_col4 = (
        st.columns(4)
    )

    with summary_col1:

        st.metric(
            "Policies",
            len(policies_df),
        )

    with summary_col2:

        st.metric(
            "Claims",
            len(claims_df),
        )

    with summary_col3:

        st.metric(
            "Interactions",
            len(interactions_df),
        )

    with summary_col4:

        st.metric(
            "AI Insights",
            len(insights_df),
        )

