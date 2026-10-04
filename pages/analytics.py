
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

from utils.security import enforce_employee_boundary

from services.snowflake_service import (
    get_all_customers,
    get_all_interactions,
    get_all_ai_insights,
    get_customer_policies,
    get_customer_claims,
    get_customer_payments,
    get_customer_interactions,
)


enforce_employee_boundary()


st.set_page_config(
    page_title="Enterprise Analytics",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)


st.markdown(
    """
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');


/* =========================================================
   GLOBAL APP
   ========================================================= */

.stApp {
    background:
        radial-gradient(
            circle at 5% 0%,
            rgba(37, 99, 235, 0.14),
            transparent 32%
        ),
        radial-gradient(
            circle at 95% 5%,
            rgba(124, 58, 237, 0.12),
            transparent 30%
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


[data-testid="stMainBlockContainer"] {
    max-width: 1500px;
    padding-top: 2.3rem;
    padding-bottom: 4rem;
}


/* =========================================================
   HEADINGS
   ========================================================= */

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

    margin-bottom: 0.4rem !important;
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
}

p {
    color: #aebbd0;
    line-height: 1.65;
}

[data-testid="stCaptionContainer"] {
    color: #7f8da3;
}


/* =========================================================
   METRIC CARDS
   ========================================================= */

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

    padding: 19px 18px;

    min-height: 108px;

    box-shadow:
        0 10px 30px rgba(0, 0, 0, 0.16),
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

    opacity: 0.65;
}


[data-testid="stMetric"]:hover {
    transform: translateY(-4px);

    border-color: rgba(96, 165, 250, 0.45);

    box-shadow:
        0 15px 38px rgba(0, 0, 0, 0.22),
        0 0 24px rgba(59, 130, 246, 0.06);
}


[data-testid="stMetricLabel"] {
    color: #94a3b8 !important;
    font-size: 0.76rem !important;
    font-weight: 600 !important;
    text-transform: uppercase;
    letter-spacing: 0.45px;
}


[data-testid="stMetricValue"] {
    color: #f8fafc !important;
    font-size: 1.75rem !important;
    font-weight: 800 !important;
}


[data-testid="stMetricDelta"] {
    font-size: 0.78rem !important;
}


/* =========================================================
   PLOTLY CHART CONTAINER
   ========================================================= */

[data-testid="stPlotlyChart"] {
    background:
        linear-gradient(
            145deg,
            rgba(16, 27, 47, 0.82),
            rgba(10, 18, 32, 0.82)
        );

    border: 1px solid rgba(71, 85, 105, 0.35);

    border-radius: 18px;

    padding: 8px;

    box-shadow:
        0 12px 32px rgba(0, 0, 0, 0.16);
}


/* =========================================================
   DATAFRAME
   ========================================================= */

[data-testid="stDataFrame"] {
    border: 1px solid rgba(71, 85, 105, 0.48);

    border-radius: 15px;

    overflow: hidden;

    background: rgba(10, 17, 30, 0.75);

    box-shadow:
        0 10px 28px rgba(0, 0, 0, 0.13);
}


/* =========================================================
   ALERTS
   ========================================================= */

[data-testid="stAlert"] {
    border-radius: 13px;

    border: 1px solid rgba(96, 165, 250, 0.20);

    background:
        linear-gradient(
            135deg,
            rgba(30, 64, 175, 0.10),
            rgba(30, 41, 59, 0.28)
        );

    color: #dbeafe;
}


/* =========================================================
   SEPARATORS
   ========================================================= */

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


/* =========================================================
   COLUMNS
   ========================================================= */

[data-testid="stHorizontalBlock"] {
    gap: 1rem;
}


/* =========================================================
   BUTTONS
   ========================================================= */

.stButton > button {
    background:
        linear-gradient(
            110deg,
            #2563eb 0%,
            #4f46e5 55%,
            #7c3aed 100%
        );

    color: #ffffff !important;

    border: 1px solid rgba(147, 197, 253, 0.25);

    border-radius: 11px;

    min-height: 43px;

    font-weight: 650;

    box-shadow:
        0 6px 18px rgba(37, 99, 235, 0.18);

    transition:
        transform 0.2s ease,
        box-shadow 0.2s ease,
        filter 0.2s ease;
}


.stButton > button:hover {
    filter: brightness(1.08);

    transform: translateY(-2px);

    box-shadow:
        0 9px 25px rgba(59, 130, 246, 0.28);

    border-color: rgba(191, 219, 254, 0.5);
}


/* =========================================================
   SCROLLBAR
   ========================================================= */

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


/* =========================================================
   MOBILE
   ========================================================= */

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

    [data-testid="stMetric"] {
        min-height: 95px;
        padding: 14px;
        border-radius: 14px;
    }

    [data-testid="stMetricValue"] {
        font-size: 1.45rem !important;
    }

    [data-testid="stDataFrame"] {
        border-radius: 11px;
    }
}


/* =========================================================
   ACCESSIBILITY
   ========================================================= */

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

st.title("📈 Enterprise Analytics & Risk Intelligence")

st.caption(
    "Live operational analytics from Snowflake — customer risk, "
    "claims, renewals, payments, interactions and data quality."
)

customers_df = get_all_customers()
interactions_df = get_all_interactions()
ai_insights_df = get_all_ai_insights()


@st.cache_data(ttl=60)
def load_operational_data(customer_ids):

    if not customer_ids:
        return (
            pd.DataFrame(),
            pd.DataFrame(),
            pd.DataFrame(),
        )

    all_policies = []
    all_claims = []
    all_payments = []

    for customer_id in customer_ids:

        policies = get_customer_policies(customer_id)

        if policies is not None and not policies.empty:
            all_policies.append(policies)

        claims = get_customer_claims(customer_id)

        if claims is not None and not claims.empty:
            all_claims.append(claims)

        payments = get_customer_payments(customer_id)

        if payments is not None and not payments.empty:
            all_payments.append(payments)

    policies_df = (
        pd.concat(
            all_policies,
            ignore_index=True
        )
        if all_policies
        else pd.DataFrame()
    )

    claims_df = (
        pd.concat(
            all_claims,
            ignore_index=True
        )
        if all_claims
        else pd.DataFrame()
    )

    payments_df = (
        pd.concat(
            all_payments,
            ignore_index=True
        )
        if all_payments
        else pd.DataFrame()
    )

    return (
        policies_df,
        claims_df,
        payments_df,
    )


customer_ids = []

if (
    not customers_df.empty
    and "CUSTOMER_ID" in customers_df.columns
):

    customer_ids = (
        customers_df["CUSTOMER_ID"]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )


policies_df, claims_df, payments_df = load_operational_data(
    tuple(customer_ids)
)


def count_status(df, column, statuses):

    if (
        df is None
        or df.empty
        or column not in df.columns
    ):
        return 0

    values = (
        df[column]
        .fillna("")
        .astype(str)
        .str.strip()
        .str.upper()
    )

    return int(
        values.isin(statuses).sum()
    )


def safe_datetime(df, column):

    if (
        df is None
        or df.empty
        or column not in df.columns
    ):
        return pd.Series(
            dtype="datetime64[ns]"
        )

    return pd.to_datetime(
        df[column],
        errors="coerce"
    )

PLOT_BG = "rgba(10,18,32,0.20)"
GRID_COLOR = "rgba(148,163,184,0.10)"
TEXT_COLOR = "#94a3b8"
TITLE_COLOR = "#e2e8f0"


def apply_chart_theme(fig, height=360):

    fig.update_layout(
        height=height,

        paper_bgcolor="rgba(0,0,0,0)",

        plot_bgcolor=PLOT_BG,

        font=dict(
            family="Inter, sans-serif",
            color=TEXT_COLOR,
            size=12,
        ),

        margin=dict(
            l=25,
            r=25,
            t=25,
            b=30,
        ),

        hoverlabel=dict(
            bgcolor="#111827",
            bordercolor="#334155",
            font=dict(
                color="#f8fafc",
                family="Inter",
            ),
        ),

        showlegend=False,

        xaxis=dict(
            color=TEXT_COLOR,
            gridcolor="rgba(0,0,0,0)",
            zeroline=False,
        ),

        yaxis=dict(
            color=TEXT_COLOR,
            gridcolor=GRID_COLOR,
            zeroline=False,
        ),
    )

    return fig


def show_plotly(fig):

    st.plotly_chart(
        fig,
        use_container_width=True,
        config={
            "displayModeBar": False,
            "responsive": True,
        },
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
    f"{total_customers:,}",
)

col2.metric(
    "📄 Policies",
    f"{total_policies:,}",
)

col3.metric(
    "🧾 Claims",
    f"{total_claims:,}",
)

col4.metric(
    "💬 Interactions",
    f"{total_interactions:,}",
)

col5.metric(
    "💳 Payments",
    f"{total_payments:,}",
)


st.markdown("## ⚠️ Operational Risk Indicators")


renewals_30d = 0


if (
    not policies_df.empty
    and "RENEWAL_DATE" in policies_df.columns
):

    renewal_dates = safe_datetime(
        policies_df,
        "RENEWAL_DATE",
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
        "UNDER_INVESTIGATION",
    },
)


payment_risk = count_status(
    payments_df,
    "PAYMENT_STATUS",
    {
        "OVERDUE",
        "LATE",
        "FAILED",
        "PENDING",
    },
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
    renewals_30d,
)

col2.metric(
    "🧾 Open / Pending Claims",
    open_claims,
)

col3.metric(
    "💰 Payment Risk",
    payment_risk,
)

col4.metric(
    "🔁 Repeated Interaction Customers",
    repeated_interaction_customers,
)


st.markdown("## 🧹 Data Quality & AI Readiness")


missing_transcripts = 0
available_transcripts = 0


if (
    not interactions_df.empty
    and "TRANSCRIPT" in interactions_df.columns
):

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
    available_transcripts,
)

col2.metric(
    "⚠️ Missing Transcripts",
    missing_transcripts,
)

col3.metric(
    "🤖 AI Insights",
    ai_insights_available,
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

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=policy_distribution["Policy Type"],
            y=policy_distribution["Count"],

            marker=dict(
                color=[
                    "#3b82f6",
                    "#6366f1",
                    "#8b5cf6",
                    "#06b6d4",
                    "#14b8a6",
                ],
                line=dict(width=0),
            ),

            hovertemplate=(
                "<b>%{x}</b><br>"
                "Policies: %{y}<extra></extra>"
            ),
        )
    )

    fig.update_layout(
        bargap=0.35,
    )

    fig = apply_chart_theme(
        fig,
        height=370,
    )

    show_plotly(fig)

else:

    st.info(
        "No policy data is currently available."
    )


col_left, col_right = st.columns(2)

with col_left:

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

        claim_colors = {
            "APPROVED": "#22c55e",
            "IN_PROGRESS": "#3b82f6",
            "PENDING": "#f59e0b",
            "UNDER_INVESTIGATION": "#f97316",
            "REJECTED": "#ef4444",
            "OPEN": "#06b6d4",
            "UNKNOWN": "#64748b",
        }

        colors = [
            claim_colors.get(
                status,
                "#6366f1"
            )
            for status
            in claim_distribution["Claim Status"]
        ]

        fig = go.Figure()

        fig.add_trace(
            go.Bar(
                x=claim_distribution["Claim Status"],
                y=claim_distribution["Count"],

                marker=dict(
                    color=colors,
                    line=dict(width=0),
                ),

                hovertemplate=(
                    "<b>%{x}</b><br>"
                    "Claims: %{y}<extra></extra>"
                ),
            )
        )

        fig = apply_chart_theme(
            fig,
            height=350,
        )

        fig.update_layout(
            xaxis=dict(
                tickangle=-25,
                color=TEXT_COLOR,
                gridcolor="rgba(0,0,0,0)",
            )
        )

        show_plotly(fig)

    else:

        st.info(
            "No claim data is currently available."
        )


with col_right:

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

        payment_colors = {
            "PAID": "#22c55e",
            "COMPLETED": "#22c55e",
            "SUCCESS": "#22c55e",
            "PENDING": "#f59e0b",
            "OVERDUE": "#ef4444",
            "FAILED": "#dc2626",
            "LATE": "#f97316",
            "UNKNOWN": "#64748b",
        }

        colors = [
            payment_colors.get(
                status,
                "#6366f1"
            )
            for status
            in payment_distribution["Payment Status"]
        ]

        fig = go.Figure()

        fig.add_trace(
            go.Bar(
                x=payment_distribution["Payment Status"],
                y=payment_distribution["Count"],

                marker=dict(
                    color=colors,
                    line=dict(width=0),
                ),

                hovertemplate=(
                    "<b>%{x}</b><br>"
                    "Payments: %{y}<extra></extra>"
                ),
            )
        )

        fig = apply_chart_theme(
            fig,
            height=350,
        )

        fig.update_layout(
            xaxis=dict(
                tickangle=-25,
                color=TEXT_COLOR,
                gridcolor="rgba(0,0,0,0)",
            )
        )

        show_plotly(fig)

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

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=interaction_distribution["Count"],
            y=interaction_distribution["Interaction Type"],

            orientation="h",

            marker=dict(
                color="#6366f1",
                line=dict(width=0),
            ),

            hovertemplate=(
                "<b>%{y}</b><br>"
                "Interactions: %{x}<extra></extra>"
            ),
        )
    )

    fig = apply_chart_theme(
        fig,
        height=max(
            320,
            len(interaction_distribution) * 55,
        ),
    )

    fig.update_layout(
        yaxis=dict(
            autorange="reversed",
            color=TEXT_COLOR,
            gridcolor="rgba(0,0,0,0)",
        ),
        xaxis=dict(
            color=TEXT_COLOR,
            gridcolor=GRID_COLOR,
        ),
    )

    show_plotly(fig)

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


    negative_count = 0
    positive_count = 0
    neutral_count = 0


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
            sentiment_counts.get(
                "NEGATIVE",
                0
            )
        )

        positive_count = int(
            sentiment_counts.get(
                "POSITIVE",
                0
            )
        )

        neutral_count = int(
            sentiment_counts.get(
                "NEUTRAL",
                0
            )
        )


    high_churn = 0


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


    insight_col1.metric(
        "🔴 Negative Sentiment",
        negative_count,
    )

    insight_col2.metric(
        "🟢 Positive Sentiment",
        positive_count,
    )

    insight_col3.metric(
        "🚨 High Churn Signals",
        high_churn,
    )

    chart_left, chart_right = st.columns(2)

    with chart_left:

        st.markdown("### 💭 Sentiment Distribution")

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

            sentiment_colors = {
                "POSITIVE": "#22c55e",
                "NEGATIVE": "#ef4444",
                "NEUTRAL": "#3b82f6",
                "UNKNOWN": "#64748b",
            }

            colors = [
                sentiment_colors.get(
                    sentiment,
                    "#8b5cf6"
                )
                for sentiment
                in sentiment_distribution["Sentiment"]
            ]

            fig = go.Figure(
                data=[
                    go.Pie(
                        labels=sentiment_distribution["Sentiment"],
                        values=sentiment_distribution["Count"],

                        hole=0.64,

                        marker=dict(
                            colors=colors,
                            line=dict(
                                color="#0b1220",
                                width=3,
                            ),
                        ),

                        textinfo="percent",

                        hovertemplate=(
                            "<b>%{label}</b><br>"
                            "Count: %{value}<br>"
                            "Share: %{percent}"
                            "<extra></extra>"
                        ),
                    )
                ]
            )

            fig.update_layout(
                height=390,

                paper_bgcolor="rgba(0,0,0,0)",

                font=dict(
                    family="Inter",
                    color=TEXT_COLOR,
                ),

                margin=dict(
                    l=20,
                    r=20,
                    t=20,
                    b=20,
                ),

                showlegend=True,

                legend=dict(
                    orientation="h",
                    y=-0.05,
                    x=0.5,
                    xanchor="center",
                ),

                annotations=[
                    dict(
                        text="<b>Sentiment</b>",
                        x=0.5,
                        y=0.5,
                        font=dict(
                            size=16,
                            color="#f8fafc",
                        ),
                        showarrow=False,
                    )
                ],
            )

            show_plotly(fig)

        else:

            st.info(
                "Sentiment data is unavailable."
            )


    with chart_right:

        st.markdown("### 🚨 Churn Signal Distribution")

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

            churn_colors = {
                "HIGH": "#ef4444",
                "MEDIUM": "#f59e0b",
                "LOW": "#22c55e",
                "UNKNOWN": "#64748b",
            }

            colors = [
                churn_colors.get(
                    signal,
                    "#6366f1"
                )
                for signal
                in churn_distribution["Churn Signal"]
            ]

            fig = go.Figure(
                data=[
                    go.Pie(
                        labels=churn_distribution["Churn Signal"],
                        values=churn_distribution["Count"],

                        hole=0.64,

                        marker=dict(
                            colors=colors,
                            line=dict(
                                color="#0b1220",
                                width=3,
                            ),
                        ),

                        textinfo="percent",

                        hovertemplate=(
                            "<b>%{label}</b><br>"
                            "Count: %{value}<br>"
                            "Share: %{percent}"
                            "<extra></extra>"
                        ),
                    )
                ]
            )

            fig.update_layout(
                height=390,

                paper_bgcolor="rgba(0,0,0,0)",

                font=dict(
                    family="Inter",
                    color=TEXT_COLOR,
                ),

                margin=dict(
                    l=20,
                    r=20,
                    t=20,
                    b=20,
                ),

                showlegend=True,

                legend=dict(
                    orientation="h",
                    y=-0.05,
                    x=0.5,
                    xanchor="center",
                ),

                annotations=[
                    dict(
                        text="<b>Churn</b>",
                        x=0.5,
                        y=0.5,
                        font=dict(
                            size=16,
                            color="#f8fafc",
                        ),
                        showarrow=False,
                    )
                ],
            )

            show_plotly(fig)

        else:

            st.info(
                "Churn signal data is unavailable."
            )
st.markdown("## 🚨 Customers Requiring Attention")


risk_customers = []


if (
    not customers_df.empty
    and "CUSTOMER_ID" in customers_df.columns
):

    for customer_id in (
        customers_df["CUSTOMER_ID"]
        .dropna()
        .astype(str)
        .unique()
    ):

        policies = get_customer_policies(
            customer_id
        )

        claims = get_customer_claims(
            customer_id
        )

        payments = get_customer_payments(
            customer_id
        )

        interactions = get_customer_interactions(
            customer_id
        )


        risk_reasons = []


        if (
            not policies.empty
            and "RENEWAL_DATE" in policies.columns
        ):

            renewal_dates = safe_datetime(
                policies,
                "RENEWAL_DATE",
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
                "UNDER_INVESTIGATION",
            },
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
                "FAILED",
            },
        ) > 0:

            risk_reasons.append(
                "Payment risk"
            )


        if (
            interactions is not None
            and len(interactions) >= 3
        ):

            risk_reasons.append(
                "Repeated support interactions"
            )

        if risk_reasons:

            customer_name = customer_id

            match = customers_df[
                customers_df["CUSTOMER_ID"]
                .astype(str)
                == customer_id
            ]

            if not match.empty:

                first_name = str(
                    match.iloc[0].get(
                        "FIRST_NAME",
                        ""
                    )
                    or ""
                ).strip()

                last_name = str(
                    match.iloc[0].get(
                        "LAST_NAME",
                        ""
                    )
                    or ""
                ).strip()

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

    risk_df = (
        pd.DataFrame(risk_customers)
        .sort_values(
            "Risk Count",
            ascending=False,
        )
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
        "No customers currently match the configured "
        "operational risk rules."
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
