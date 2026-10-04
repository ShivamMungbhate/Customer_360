
import streamlit as st
import pandas as pd

from utils.security import enforce_employee_boundary

from services.snowflake_service import (
    get_system_health,
    get_all_customers,
    get_all_interactions,
    get_all_ai_insights,
)


st.set_page_config(
    page_title="System Health Dashboard",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="expanded",
)


st.markdown(
    """
    <style>

    /* =========================
       GLOBAL
       ========================= */

    .stApp {
        background:
            radial-gradient(
                circle at 10% 10%,
                rgba(37, 99, 235, 0.10),
                transparent 30%
            ),
            radial-gradient(
                circle at 90% 20%,
                rgba(14, 165, 233, 0.08),
                transparent 30%
            ),
            #0b1120;
        color: #e5e7eb;
    }

    .main .block-container {
        max-width: 1450px;
        padding-top: 2rem;
        padding-bottom: 4rem;
        padding-left: 3rem;
        padding-right: 3rem;
    }

    /* =========================
       HEADINGS
       ========================= */

    h1 {
        font-size: 2.4rem !important;
        font-weight: 800 !important;
        color: #f8fafc !important;
        letter-spacing: -0.5px;
    }

    h2 {
        font-size: 1.55rem !important;
        font-weight: 750 !important;
        color: #f1f5f9 !important;
        margin-top: 1.5rem !important;
    }

    h3 {
        color: #e2e8f0 !important;
        font-weight: 700 !important;
    }

    p {
        color: #cbd5e1;
    }

    /* =========================
       METRIC CARDS
       ========================= */

    [data-testid="stMetric"] {
        background:
            linear-gradient(
                145deg,
                rgba(30, 41, 59, 0.95),
                rgba(15, 23, 42, 0.95)
            );

        border: 1px solid rgba(148, 163, 184, 0.16);
        border-radius: 16px;

        padding: 20px 22px;

        min-height: 125px;

        box-shadow:
            0 10px 30px rgba(0, 0, 0, 0.20);

        transition:
            transform 0.2s ease,
            border-color 0.2s ease,
            box-shadow 0.2s ease;
    }

    [data-testid="stMetric"]:hover {
        transform: translateY(-3px);

        border-color:
            rgba(59, 130, 246, 0.45);

        box-shadow:
            0 14px 35px rgba(0, 0, 0, 0.30);
    }

    [data-testid="stMetricLabel"] {
        color: #94a3b8 !important;
        font-size: 0.85rem !important;
        font-weight: 600 !important;
    }

    [data-testid="stMetricValue"] {
        color: #f8fafc !important;
        font-size: 1.65rem !important;
        font-weight: 800 !important;
    }

    [data-testid="stMetricDelta"] {
        font-size: 0.78rem !important;
    }

    /* =========================
       DATAFRAME / TABLE
       ========================= */

    [data-testid="stDataFrame"] {
        border-radius: 14px;
        overflow: hidden;

        border: 1px solid
            rgba(148, 163, 184, 0.15);

        box-shadow:
            0 8px 25px rgba(0, 0, 0, 0.18);
    }

    /* =========================
       CONTAINERS
       ========================= */

    [data-testid="stVerticalBlockBorderWrapper"] {
        background:
            rgba(15, 23, 42, 0.70);

        border:
            1px solid rgba(148, 163, 184, 0.14);

        border-radius: 16px;
    }

    /* =========================
       SELECTBOX
       ========================= */

    div[data-baseweb="select"] > div {
        background-color: #111827 !important;
        border: 1px solid #334155 !important;
        border-radius: 10px !important;
        color: #f8fafc !important;
    }

    div[data-baseweb="select"] span {
        color: #e5e7eb !important;
    }

    /* =========================
       BUTTONS
       ========================= */

    .stButton > button {
        border-radius: 10px;

        border: 1px solid
            rgba(59, 130, 246, 0.35);

        background:
            linear-gradient(
                135deg,
                #2563eb,
                #1d4ed8
            );

        color: white;

        font-weight: 650;

        padding: 0.55rem 1rem;

        transition:
            transform 0.2s ease,
            box-shadow 0.2s ease;
    }

    .stButton > button:hover {
        transform: translateY(-2px);

        box-shadow:
            0 8px 22px rgba(37, 99, 235, 0.30);
    }

    /* =========================
       ALERTS
       ========================= */

    [data-testid="stAlert"] {
        border-radius: 12px !important;
        border-width: 1px !important;
    }

    /* =========================
       DIVIDERS
       ========================= */

    hr {
        border: none;
        height: 1px;

        background:
            linear-gradient(
                90deg,
                transparent,
                rgba(148, 163, 184, 0.25),
                transparent
            );

        margin: 2rem 0;
    }

    /* =========================
       CAPTIONS
       ========================= */

    [data-testid="stCaptionContainer"] {
        color: #94a3b8 !important;
    }

    /* =========================
       BAR CHART AREA
       ========================= */

    [data-testid="stVegaLiteChart"] {
        background:
            rgba(15, 23, 42, 0.70);

        border:
            1px solid rgba(148, 163, 184, 0.12);

        border-radius: 16px;

        padding: 10px;

        box-shadow:
            0 8px 25px rgba(0, 0, 0, 0.18);
    }

    /* =========================
       SIDEBAR
       ========================= */

    section[data-testid="stSidebar"] {
        background:
            linear-gradient(
                180deg,
                #0f172a,
                #020617
            );

        border-right:
            1px solid rgba(148, 163, 184, 0.12);
    }

    section[data-testid="stSidebar"] * {
        color: #e2e8f0;
    }

    /* =========================
       RESPONSIVE
       ========================= */

    @media (max-width: 900px) {

        .main .block-container {
            padding-left: 1rem;
            padding-right: 1rem;
        }

        h1 {
            font-size: 1.8rem !important;
        }

        h2 {
            font-size: 1.3rem !important;
        }

        [data-testid="stMetric"] {
            min-height: 105px;
            padding: 15px;
        }
    }

    </style>
    """,
    unsafe_allow_html=True,
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


