import streamlit as st
import pandas as pd

from utils.security import enforce_customer_boundary

from services.snowflake_service import (
    get_customer_profile,
    get_customer_policies,
    get_customer_claims,
    get_customer_payments,
    get_customer_interactions,
    create_policy_feedback,
    get_policy_feedback,
)
st.set_page_config(
    page_title="Customer Dashboard",
    page_icon="👤",
    layout="wide",
    initial_sidebar_state="expanded",
)



st.markdown(
    """
    <style>

    /* ======================================================
       GLOBAL PAGE BACKGROUND
    ====================================================== */

    .stApp {
        background:
            linear-gradient(
                135deg,
                #0f172a 0%,
                #172554 45%,
                #1e3a8a 100%
            ) !important;
        color: #f8fafc;
    }

    /* Main Streamlit content area */
    .main {
        background: transparent !important;
    }

    .main .block-container {
        max-width: 1400px;
        padding-top: 2rem;
        padding-bottom: 3rem;
        background: transparent !important;
    }

    /* Remove white background from Streamlit wrappers */
    [data-testid="stAppViewContainer"] {
        background: transparent !important;
    }

    [data-testid="stMain"] {
        background: transparent !important;
    }

    [data-testid="stMainBlockContainer"] {
        background: transparent !important;
    }


    /* ======================================================
       HEADER
    ====================================================== */

    .customer-header {
        background:
            linear-gradient(
                135deg,
                #020617 0%,
                #172554 50%,
                #2563eb 100%
            );

        padding: 30px 35px;
        border-radius: 20px;
        color: white;
        margin-bottom: 25px;

        border: 1px solid rgba(255,255,255,0.10);

        box-shadow:
            0 15px 40px rgba(0,0,0,0.30);
    }

    .customer-header h1 {
        margin: 0;
        font-size: 32px;
        font-weight: 750;
        color: white !important;
    }

    .customer-header p {
        margin-top: 8px;
        margin-bottom: 0;
        color: #bfdbfe !important;
        font-size: 15px;
    }

    .customer-id-badge {
        display: inline-block;
        margin-top: 15px;
        padding: 7px 14px;
        border-radius: 999px;

        background: rgba(255,255,255,0.10);
        border: 1px solid rgba(255,255,255,0.18);

        color: #ffffff !important;
        font-size: 13px;
        font-weight: 600;
    }


    /* ======================================================
       NORMAL TEXT
    ====================================================== */

    .main p,
    .main span,
    .main label,
    .main div {
        color: inherit;
    }

    .main h1,
    .main h2,
    .main h3,
    .main h4,
    .main h5,
    .main h6 {
        color: #f8fafc !important;
    }

    .main [data-testid="stCaptionContainer"] {
        color: #cbd5e1 !important;
    }


    /* ======================================================
       METRIC CARDS
    ====================================================== */

    div[data-testid="metric-container"] {
        background:
            linear-gradient(
                145deg,
                rgba(30,41,59,0.96),
                rgba(15,23,42,0.96)
            ) !important;

        border: 1px solid rgba(148,163,184,0.20);

        border-radius: 16px;

        padding: 18px 20px;

        box-shadow:
            0 8px 25px rgba(0,0,0,0.25);

        transition:
            transform 0.2s ease,
            box-shadow 0.2s ease,
            border-color 0.2s ease;
    }

    div[data-testid="metric-container"]:hover {
        transform: translateY(-3px);

        border-color: rgba(96,165,250,0.50);

        box-shadow:
            0 14px 32px rgba(0,0,0,0.35);
    }

    div[data-testid="metric-container"]
    [data-testid="stMetricLabel"] {
        color: #94a3b8 !important;
        font-weight: 600;
        font-size: 13px;
    }

    div[data-testid="metric-container"]
    [data-testid="stMetricValue"] {
        color: #f8fafc !important;
        font-weight: 750;
    }

    div[data-testid="metric-container"]
    [data-testid="stMetricDelta"] {
        color: #93c5fd !important;
    }


    /* ======================================================
       POLICY / CLAIM / INTERACTION CARDS
    ====================================================== */

    div[data-testid="stVerticalBlockBorderWrapper"] {
        background:
            linear-gradient(
                145deg,
                rgba(30,41,59,0.96),
                rgba(15,23,42,0.96)
            ) !important;

        border: 1px solid rgba(148,163,184,0.20);

        border-radius: 18px;

        box-shadow:
            0 8px 25px rgba(0,0,0,0.25);

        transition:
            transform 0.2s ease,
            box-shadow 0.2s ease,
            border-color 0.2s ease;

        margin-bottom: 14px;
    }

    div[data-testid="stVerticalBlockBorderWrapper"]:hover {
        transform: translateY(-2px);

        border-color: rgba(96,165,250,0.45);

        box-shadow:
            0 14px 32px rgba(0,0,0,0.32);
    }


    /* ======================================================
       BUTTONS
    ====================================================== */

    .stButton > button {
        border-radius: 10px;

        border: 1px solid #475569;

        background: #1e293b;

        color: #e2e8f0 !important;

        font-weight: 650;

        min-height: 42px;

        transition: all 0.2s ease;
    }

    .stButton > button:hover {
        border-color: #60a5fa;

        color: #ffffff !important;

        background: #1e40af;

        box-shadow:
            0 6px 18px rgba(37,99,235,0.30);
    }

    .stButton > button[kind="primary"] {
        background:
            linear-gradient(
                135deg,
                #2563eb,
                #1d4ed8
            ) !important;

        color: white !important;

        border: none;
    }

    .stButton > button[kind="primary"]:hover {
        background:
            linear-gradient(
                135deg,
                #3b82f6,
                #2563eb
            ) !important;

        color: white !important;
    }


    /* ======================================================
       INPUTS
    ====================================================== */

    .stTextInput input,
    .stTextArea textarea {
        border-radius: 10px;

        border: 1px solid #475569 !important;

        background: #0f172a !important;

        color: #f8fafc !important;
    }

    .stTextInput input::placeholder,
    .stTextArea textarea::placeholder {
        color: #64748b !important;
    }

    .stTextInput input:focus,
    .stTextArea textarea:focus {
        border-color: #3b82f6 !important;

        box-shadow:
            0 0 0 2px rgba(59,130,246,0.20);
    }


    /* ======================================================
       SELECTBOX
    ====================================================== */

    .stSelectbox [data-baseweb="select"] > div {
        background: #0f172a !important;

        border-color: #475569 !important;

        color: #f8fafc !important;

        border-radius: 10px;
    }


    /* ======================================================
       SLIDER
    ====================================================== */

    .stSlider {
        color: #60a5fa !important;
    }


    /* ======================================================
       EXPANDERS
    ====================================================== */

    div[data-testid="stExpander"] {
        border: 1px solid rgba(148,163,184,0.22) !important;

        border-radius: 14px;

        background: #111827 !important;

        overflow: hidden;

        margin-top: 12px;
    }

    div[data-testid="stExpander"] summary {
        font-weight: 650;

        color: #e2e8f0 !important;
    }

    div[data-testid="stExpander"] summary:hover {
        color: #93c5fd !important;
    }


    /* ======================================================
       DATAFRAME
    ====================================================== */

    div[data-testid="stDataFrame"] {
        border-radius: 14px;

        overflow: hidden;

        border: 1px solid rgba(148,163,184,0.22);

        box-shadow:
            0 7px 20px rgba(0,0,0,0.25);
    }


    /* ======================================================
       ALERTS
    ====================================================== */

    div[data-testid="stAlert"] {
        border-radius: 12px;
    }


    /* ======================================================
       FEEDBACK
    ====================================================== */

    .feedback-title {
        color: #c4b5fd !important;

        font-size: 17px;

        font-weight: 750;

        margin-bottom: 8px;
    }


    /* ======================================================
       STATUS BADGES
    ====================================================== */

    .status-active {
        display: inline-block;

        background: #064e3b;

        color: #6ee7b7 !important;

        padding: 5px 11px;

        border-radius: 999px;

        font-size: 12px;

        font-weight: 700;
    }

    .status-warning {
        display: inline-block;

        background: #78350f;

        color: #fde68a !important;

        padding: 5px 11px;

        border-radius: 999px;

        font-size: 12px;

        font-weight: 700;
    }

    .status-danger {
        display: inline-block;

        background: #7f1d1d;

        color: #fecaca !important;

        padding: 5px 11px;

        border-radius: 999px;

        font-size: 12px;

        font-weight: 700;
    }


    /* ======================================================
       DIVIDERS
    ====================================================== */

    hr {
        border: none;

        border-top:
            1px solid rgba(148,163,184,0.18);

        margin: 28px 0;
    }


    /* ======================================================
       SIDEBAR
    ====================================================== */

    section[data-testid="stSidebar"] {
        background:
            linear-gradient(
                180deg,
                #020617 0%,
                #0f172a 45%,
                #172554 100%
            ) !important;
    }

    section[data-testid="stSidebar"] * {
        color: #e2e8f0;
    }


    /* ======================================================
       SCROLLBAR
    ====================================================== */

    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }

    ::-webkit-scrollbar-track {
        background: #020617;
    }

    ::-webkit-scrollbar-thumb {
        background: #334155;
        border-radius: 10px;
    }

    ::-webkit-scrollbar-thumb:hover {
        background: #475569;
    }


    /* ======================================================
       MOBILE
    ====================================================== */

    @media (max-width: 768px) {

        .main .block-container {
            padding-left: 1rem;
            padding-right: 1rem;
        }

        .customer-header {
            padding: 22px;
            border-radius: 15px;
        }

        .customer-header h1 {
            font-size: 25px;
        }

    }

    </style>
    """,
    unsafe_allow_html=True,
)

enforce_customer_boundary()


customer_id = st.session_state.get("customer_id")

if not customer_id or str(customer_id).startswith("CUST-"):
    customer_id = "C001"

customer_id = str(customer_id).strip().upper()

profile_df = get_customer_profile(customer_id)
policies_df = get_customer_policies(customer_id)
claims_df = get_customer_claims(customer_id)
payments_df = get_customer_payments(customer_id)
interactions_df = get_customer_interactions(customer_id)


if profile_df.empty:
    st.error(
        f"Customer record `{customer_id}` was not found in Snowflake."
    )
    st.stop()


profile = profile_df.iloc[0]


first_name = str(
    profile.get("FIRST_NAME", "")
).strip()

last_name = str(
    profile.get("LAST_NAME", "")
).strip()

display_name = f"{first_name} {last_name}".strip()

if not display_name:
    display_name = "Customer"

st.markdown(
    f"""
    <div class="customer-header">
        <h1>Welcome back, {display_name} 👋</h1>
        <p>Your insurance account overview and recent activity</p>
        <div class="customer-id-badge">
            Customer ID: {customer_id}
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

active_policies = 0

if not policies_df.empty and "STATUS" in policies_df.columns:
    active_policies = (
        policies_df["STATUS"]
        .astype(str)
        .str.upper()
        .eq("ACTIVE")
        .sum()
    )


open_claims = 0

if not claims_df.empty and "CLAIM_STATUS" in claims_df.columns:

    closed_statuses = [
        "CLOSED",
        "SETTLED",
        "REJECTED"
    ]

    open_claims = (
        ~claims_df["CLAIM_STATUS"]
        .astype(str)
        .str.upper()
        .isin(closed_statuses)
    ).sum()


payment_count = len(payments_df)

interaction_count = len(interactions_df)


col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Active Policies",
        active_policies
    )

with col2:
    st.metric(
        "Open Claims",
        open_claims
    )

with col3:
    st.metric(
        "Payments",
        payment_count
    )

with col4:
    st.metric(
        "Interactions",
        interaction_count
    )

st.markdown("---")

st.markdown("#### 🛡️ My Policies")


if policies_df.empty:

    st.info(
        "No policy records are available for your account."
    )

else:

    for _, policy in policies_df.iterrows():

        policy_id = str(
            policy.get("POLICY_ID", "N/A")
        )

        policy_type = str(
            policy.get("POLICY_TYPE", "Policy")
        )

        status = str(
            policy.get("STATUS", "UNKNOWN")
        )

        renewal_date = policy.get(
            "RENEWAL_DATE",
            "Not available"
        )

        premium = policy.get(
            "PREMIUM",
            None
        )

        coverage = policy.get(
            "COVERAGE_AMOUNT",
            None
        )

        with st.container(border=True):

            col1, col2 = st.columns([2, 1])

            with col1:

                st.markdown(
                    f"##### 🛡️ {policy_type}"
                )

                st.caption(
                    f"Policy ID: `{policy_id}`"
                )

                if status.upper() == "ACTIVE":

                    st.markdown(
                        '<span class="status-active">'
                        '● ACTIVE'
                        '</span>',
                        unsafe_allow_html=True
                    )

                elif status.upper() in [
                    "PENDING",
                    "RENEWAL"
                ]:

                    st.markdown(
                        '<span class="status-warning">'
                        '● '
                        + status.upper()
                        + '</span>',
                        unsafe_allow_html=True
                    )

                else:

                    st.markdown(
                        '<span class="status-danger">'
                        '● '
                        + status.upper()
                        + '</span>',
                        unsafe_allow_html=True
                    )

                st.caption(
                    f"Renewal: {renewal_date}"
                )

            with col2:

                if pd.notna(premium):

                    st.metric(
                        "Premium",
                        f"₹{float(premium):,.0f}"
                    )

                if pd.notna(coverage):

                    st.caption(
                        f"Coverage: ₹{float(coverage):,.0f}"
                    )


            st.markdown("---")

            st.markdown(
                '<div class="feedback-title">'
                '⭐ Policy Feedback'
                '</div>',
                unsafe_allow_html=True
            )

            with st.expander(
                f"Give feedback for {policy_type}"
            ):

                st.caption(
                    f"Your feedback is for policy `{policy_id}`."
                )

                rating = st.slider(
                    "How would you rate this policy?",
                    min_value=1,
                    max_value=5,
                    value=5,
                    step=1,
                    key=f"rating_{policy_id}",
                )

                rating_labels = {
                    1: "⭐ Very Poor",
                    2: "⭐⭐ Poor",
                    3: "⭐⭐⭐ Average",
                    4: "⭐⭐⭐⭐ Good",
                    5: "⭐⭐⭐⭐⭐ Excellent",
                }

                st.caption(
                    rating_labels.get(rating, "")
                )


                category = st.selectbox(
                    "Feedback Category",
                    [
                        "Coverage",
                        "Premium",
                        "Claims Experience",
                        "Customer Service",
                        "Policy Benefits",
                        "Renewal",
                        "Other",
                    ],
                    key=f"category_{policy_id}",
                )


                comments = st.text_area(
                    "Comments",
                    placeholder=(
                        "Tell us about your experience "
                        "with this policy..."
                    ),
                    max_chars=5000,
                    key=f"comments_{policy_id}",
                )


                recommendation = st.radio(
                    "Would you recommend this policy?",
                    ["YES", "NO"],
                    horizontal=True,
                    key=f"recommendation_{policy_id}",
                )


                submit_feedback = st.button(
                    "Submit Feedback",
                    type="primary",
                    use_container_width=True,
                    key=f"submit_feedback_{policy_id}",
                )


                if submit_feedback:

                    if not comments.strip():

                        st.warning(
                            "Please enter a comment before submitting your feedback."
                        )

                    else:

                        success = create_policy_feedback(
                            customer_id=customer_id,
                            policy_id=policy_id,
                            rating=rating,
                            category=category,
                            comments=comments.strip(),
                            recommendation=recommendation,
                        )


                        if success:

                            st.success(
                                "Thank you! Your feedback has been submitted successfully. ⭐"
                            )

                            st.rerun()

            previous_feedback = get_policy_feedback(
                customer_id,
                policy_id
            )


            if (
                previous_feedback is not None
                and not previous_feedback.empty
            ):

                with st.expander(
                    "📋 View your previous feedback"
                ):

                    feedback_columns = [
                        column
                        for column in [
                            "RATING",
                            "CATEGORY",
                            "COMMENTS",
                            "RECOMMENDATION",
                            "CREATED_AT",
                        ]
                        if column in previous_feedback.columns
                    ]


                    if feedback_columns:

                        st.dataframe(
                            previous_feedback[
                                feedback_columns
                            ],
                            use_container_width=True,
                            hide_index=True,
                        )

                    else:

                        st.dataframe(
                            previous_feedback,
                            use_container_width=True,
                            hide_index=True,
                        )



st.markdown("---")

st.markdown("#### 📑 My Claims")


if claims_df.empty:

    st.info(
        "No claim records are available for your account."
    )

else:

    for _, claim in claims_df.iterrows():

        claim_id = str(
            claim.get("CLAIM_ID", "N/A")
        )

        claim_type = str(
            claim.get("CLAIM_TYPE", "Claim")
        )

        claim_status = str(
            claim.get("CLAIM_STATUS", "UNKNOWN")
        )

        claim_amount = claim.get(
            "CLAIM_AMOUNT",
            None
        )

        claim_date = claim.get(
            "CLAIM_DATE",
            "Not available"
        )


        with st.container(border=True):

            col1, col2, col3 = st.columns(
                [1, 2, 1]
            )

            with col1:

                st.markdown(
                    f"**`{claim_id}`**"
                )

                st.caption(
                    str(claim_date)
                )

            with col2:

                st.markdown(
                    f"**{claim_type}**"
                )

                if pd.notna(claim_amount):

                    st.caption(
                        f"Claim amount: ₹{float(claim_amount):,.0f}"
                    )

            with col3:

                if claim_status.upper() in [
                    "CLOSED",
                    "SETTLED"
                ]:

                    st.markdown(
                        '<span class="status-active">'
                        '● '
                        + claim_status.upper()
                        + '</span>',
                        unsafe_allow_html=True
                    )

                elif claim_status.upper() in [
                    "REJECTED",
                    "DENIED"
                ]:

                    st.markdown(
                        '<span class="status-danger">'
                        '● '
                        + claim_status.upper()
                        + '</span>',
                        unsafe_allow_html=True
                    )

                else:

                    st.markdown(
                        '<span class="status-warning">'
                        '● '
                        + claim_status.upper()
                        + '</span>',
                        unsafe_allow_html=True
                    )



st.markdown("---")

st.markdown("#### 💳 My Payments")


if payments_df.empty:

    st.info(
        "No payment records are available."
    )

else:

    payment_columns = [
        column
        for column in [
            "PAYMENT_ID",
            "POLICY_ID",
            "AMOUNT",
            "PAYMENT_DATE",
            "PAYMENT_STATUS"
        ]
        if column in payments_df.columns
    ]


    if payment_columns:

        st.dataframe(
            payments_df[payment_columns],
            use_container_width=True,
            hide_index=True
        )

    else:

        st.dataframe(
            payments_df,
            use_container_width=True,
            hide_index=True
        )

st.markdown("---")

st.markdown("#### 💬 Recent Interactions")


if interactions_df.empty:

    st.info(
        "No interaction records are available."
    )

else:

    recent_interactions = interactions_df.head(5)


    for _, interaction in recent_interactions.iterrows():

        interaction_type = str(
            interaction.get(
                "INTERACTION_TYPE",
                "Interaction"
            )
        )

        interaction_date = interaction.get(
            "INTERACTION_DATE",
            "Not available"
        )

        transcript = interaction.get(
            "TRANSCRIPT",
            ""
        )


        with st.container(border=True):

            st.markdown(
                f"**💬 {interaction_type}**"
            )

            st.caption(
                str(interaction_date)
            )

            if (
                pd.notna(transcript)
                and str(transcript).strip()
            ):

                st.write(
                    str(transcript)
                )

