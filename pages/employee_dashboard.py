import streamlit as st
import pandas as pd

from utils.security import enforce_employee_boundary

from services.snowflake_service import (
    get_all_customers,
    get_all_interactions,
    get_customer_policies,
    get_customer_claims,
    get_customer_payments,
    get_customer_interactions,
)
enforce_employee_boundary()

st.markdown("""
<style>

    /* Main application background */
    .stApp {
        background:
            radial-gradient(
                circle at 15% 10%,
                rgba(37, 99, 235, 0.16),
                transparent 28%
            ),
            radial-gradient(
                circle at 85% 20%,
                rgba(14, 165, 233, 0.10),
                transparent 25%
            ),
            linear-gradient(
                135deg,
                #07111f 0%,
                #0b1728 45%,
                #0f1f33 100%
            );

        color: #e5e7eb;
    }


    /* Main content area */
    .main .block-container {
        max-width: 1400px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }


    /* Sidebar */
    section[data-testid="stSidebar"] {
        background:
            linear-gradient(
                180deg,
                #07111f 0%,
                #0b1728 100%
            );

        border-right: 1px solid rgba(148, 163, 184, 0.15);
    }


    /* Headings */
    h1, h2, h3, h4, h5 {
        color: #f8fafc !important;
        font-weight: 700;
    }


    /* Normal text */
    p, label, span {
        color: #d1d5db;
    }


    /* Caption */
    .stCaption,
    [data-testid="stCaptionContainer"] {
        color: #94a3b8 !important;
    }


    /* Metric cards */
    [data-testid="stMetric"] {
        background:
            linear-gradient(
                145deg,
                rgba(30, 41, 59, 0.95),
                rgba(15, 31, 51, 0.95)
            );

        border: 1px solid rgba(96, 165, 250, 0.18);
        border-radius: 14px;
        padding: 18px;

        box-shadow:
            0 8px 25px rgba(0, 0, 0, 0.25);

        transition: all 0.2s ease;
    }


    [data-testid="stMetric"]:hover {
        border-color: rgba(59, 130, 246, 0.45);

        box-shadow:
            0 10px 30px rgba(37, 99, 235, 0.15);
    }


    [data-testid="stMetricLabel"] {
        color: #94a3b8 !important;
    }


    [data-testid="stMetricValue"] {
        color: #f8fafc !important;
        font-weight: 700;
    }


    /* Containers / cards */
    [data-testid="stVerticalBlockBorderWrapper"] {
        background:
            rgba(15, 31, 51, 0.78);

        border: 1px solid rgba(148, 163, 184, 0.16);
        border-radius: 14px;

        box-shadow:
            0 8px 24px rgba(0, 0, 0, 0.20);
    }


    /* Buttons */
    .stButton > button {
        background:
            linear-gradient(
                135deg,
                #2563eb,
                #1d4ed8
            );

        color: white !important;

        border: 1px solid rgba(96, 165, 250, 0.35);
        border-radius: 9px;

        font-weight: 600;

        min-height: 42px;

        transition:
            transform 0.15s ease,
            box-shadow 0.15s ease,
            background 0.15s ease;
    }


    .stButton > button:hover {
        background:
            linear-gradient(
                135deg,
                #3b82f6,
                #2563eb
            );

        color: white !important;

        transform: translateY(-1px);

        box-shadow:
            0 6px 18px rgba(37, 99, 235, 0.30);
    }


    /* Text inputs */
    div[data-baseweb="input"] {
        background-color: #111f33 !important;
        border: 1px solid #334155 !important;
        border-radius: 9px !important;
    }


    div[data-baseweb="input"]:focus-within {
        border-color: #3b82f6 !important;
        box-shadow:
            0 0 0 1px #3b82f6 !important;
    }


    input {
        color: #f8fafc !important;
        background-color: transparent !important;
    }


    input::placeholder {
        color: #64748b !important;
    }


    /* Select boxes */
    div[data-baseweb="select"] > div {
        background-color: #111f33 !important;
        border-color: #334155 !important;
        color: #f8fafc !important;
        border-radius: 9px !important;
    }


    /* Dataframes */
    [data-testid="stDataFrame"] {
        border: 1px solid rgba(148, 163, 184, 0.15);
        border-radius: 10px;
        overflow: hidden;
    }


    /* Tabs */
    button[data-baseweb="tab"] {
        color: #94a3b8 !important;
        font-weight: 600;
    }


    button[data-baseweb="tab"][aria-selected="true"] {
        color: #60a5fa !important;
    }


    /* Dividers */
    hr {
        border-color: rgba(148, 163, 184, 0.14) !important;
    }


    /* Success message */
    div[data-testid="stAlert"] {
        border-radius: 10px;
    }


    /* Search / filter section */
    div[data-testid="stTextInput"] {
        margin-bottom: 10px;
    }


    /* Code blocks */
    code {
        background-color: #111f33 !important;
        color: #93c5fd !important;
    }


    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }


    ::-webkit-scrollbar-track {
        background: #07111f;
    }


    ::-webkit-scrollbar-thumb {
        background: #334155;
        border-radius: 10px;
    }


    ::-webkit-scrollbar-thumb:hover {
        background: #475569;
    }

</style>
""", unsafe_allow_html=True)
user_email = st.session_state.get(
    "user_email",
    "RM User"
)

display_name = st.session_state.get("display_name")

if not display_name:
    display_name = user_email.split("@")[0].capitalize()


st.markdown(
    f"### Welcome, {display_name}"
)

st.caption(
    "Relationship Manager Command Center"
)

customers_df = get_all_customers()
interactions_df = get_all_interactions()


def safe_datetime(df, column):

    if df.empty or column not in df.columns:
        return pd.Series(dtype="datetime64[ns]")

    return pd.to_datetime(
        df[column],
        errors="coerce"
    )


def count_status(df, column, statuses):

    if df.empty or column not in df.columns:
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

all_policies = []
all_claims = []
all_payments = []

if (
    not customers_df.empty
    and "CUSTOMER_ID" in customers_df.columns
):

    customer_ids = (
        customers_df["CUSTOMER_ID"]
        .dropna()
        .astype(str)
        .str.strip()
        .str.upper()
        .unique()
    )

    for customer_id in customer_ids:

        policies = get_customer_policies(
            customer_id
        )

        if not policies.empty:
            all_policies.append(
                policies
            )

        claims = get_customer_claims(
            customer_id
        )

        if not claims.empty:
            all_claims.append(
                claims
            )

        payments = get_customer_payments(
            customer_id
        )

        if not payments.empty:
            all_payments.append(
                payments
            )


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
total_customers = len(
    customers_df
)
renewals_30d = 0

if (
    not policies_df.empty
    and "RENEWAL_DATE" in policies_df.columns
):

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
            &
            (days_to_renewal <= 30)
        ).sum()
    )
pending_claims = count_status(
    claims_df,
    "CLAIM_STATUS",
    {
        "OPEN",
        "PENDING",
        "IN_PROGRESS",
        "UNDER_INVESTIGATION",
    }
)
payment_risk = count_status(
    payments_df,
    "PAYMENT_STATUS",
    {
        "OVERDUE",
        "LATE",
        "FAILED",
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
        (
            interaction_counts >= 3
        ).sum()
    )


col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "👥 Total Customers",
    f"{total_customers:,}"
)

col2.metric(
    "🔄 Renewals ≤ 30 Days",
    f"{renewals_30d:,}"
)

col3.metric(
    "🧾 Pending / Open Claims",
    f"{pending_claims:,}"
)

col4.metric(
    "🔁 Repeated Interaction Customers",
    f"{repeated_interaction_customers:,}"
)

st.markdown("---")

col1, col2, col3 = st.columns(3)

col1.metric(
    "💳 Payment Risk",
    f"{payment_risk:,}"
)

col2.metric(
    "💬 Total Interactions",
    f"{len(interactions_df):,}"
)

col3.metric(
    "📄 Total Policies",
    f"{len(policies_df):,}"
)

st.markdown("---")

st.markdown(
    "## 🔴 Customers Needing Attention"
)

risk_customers = []


if (
    not customers_df.empty
    and "CUSTOMER_ID" in customers_df.columns
):

    for customer_id in (
        customers_df["CUSTOMER_ID"]
        .dropna()
        .astype(str)
        .str.strip()
        .str.upper()
        .unique()
    ):

        customer_policies = get_customer_policies(
            customer_id
        )

        customer_claims = get_customer_claims(
            customer_id
        )

        customer_payments = get_customer_payments(
            customer_id
        )

        customer_interactions = get_customer_interactions(
            customer_id
        )

        reasons = []
        if (
            not customer_policies.empty
            and "RENEWAL_DATE"
            in customer_policies.columns
        ):

            renewal_dates = safe_datetime(
                customer_policies,
                "RENEWAL_DATE"
            )

            today = pd.Timestamp.today().normalize()

            days_to_renewal = (
                renewal_dates - today
            ).dt.days

            if (
                (
                    (days_to_renewal >= 0)
                    &
                    (days_to_renewal <= 30)
                ).any()
            ):

                reasons.append(
                    "Renewal within 30 days"
                )

        if count_status(
            customer_claims,
            "CLAIM_STATUS",
            {
                "OPEN",
                "PENDING",
                "IN_PROGRESS",
                "UNDER_INVESTIGATION",
            }
        ) > 0:

            reasons.append(
                "Open / pending claim"
            )


        if count_status(
            customer_payments,
            "PAYMENT_STATUS",
            {
                "OVERDUE",
                "LATE",
                "FAILED",
            }
        ) > 0:

            reasons.append(
                "Payment risk"
            )

        if len(customer_interactions) >= 3:

            reasons.append(
                f"{len(customer_interactions)} interactions"
            )


        if reasons:

            customer_name = customer_id

            customer_match = customers_df[
                customers_df["CUSTOMER_ID"]
                .astype(str)
                .str.upper()
                == customer_id
            ]

            if not customer_match.empty:

                first_name = str(
                    customer_match.iloc[0].get(
                        "FIRST_NAME",
                        ""
                    )
                ).strip()

                last_name = str(
                    customer_match.iloc[0].get(
                        "LAST_NAME",
                        ""
                    )
                ).strip()

                full_name = (
                    f"{first_name} {last_name}"
                ).strip()

                if full_name:
                    customer_name = full_name


            risk_customers.append(
                {
                    "customer_id": customer_id,
                    "name": customer_name,
                    "reasons": reasons,
                    "risk_count": len(reasons),
                }
            )


risk_customers = sorted(
    risk_customers,
    key=lambda x: x["risk_count"],
    reverse=True,
)
if not risk_customers:

    st.success(
        "✅ No customers currently match "
        "the configured operational risk rules."
    )

else:

    for index, customer in enumerate(
        risk_customers[:10]
    ):

        with st.container(border=True):

            col_info, col_action = st.columns(
                [3, 1]
            )

            with col_info:

                st.markdown(
                    f"##### {customer['name']} "
                    f"`{customer['customer_id']}`"
                )

                st.markdown(
                    "**Risk triggers:** "
                    + " • ".join(
                        customer["reasons"]
                    )
                )

                st.caption(
                    "Operational risk detected from "
                    "live customer, policy, claim, "
                    "payment and interaction data."
                )


            with col_action:

                st.write("")

                if st.button(
                    "View Customer 360",
                    key=f"customer360_{index}_{customer['customer_id']}",
                    use_container_width=True,
                    type="primary",
                ):

                    st.session_state[
                        "selected_customer_id"
                    ] = customer["customer_id"]

                    st.switch_page(
                        "pages/customer_360.py"
                    )
st.markdown("---")

st.subheader(
    "🔍 Quick Customer Search"
)

search_query = st.text_input(
    "Search by customer name, ID, city or state...",
    placeholder="Example: Rahul, C001, Mumbai"
)


if search_query:

    search_text = (
        search_query
        .strip()
        .lower()
    )

    if not customers_df.empty:

        searchable_df = customers_df.copy()

        searchable_df["_SEARCH"] = (
            searchable_df
            .fillna("")
            .astype(str)
            .agg(" ".join, axis=1)
            .str.lower()
        )

        results = searchable_df[
            searchable_df["_SEARCH"]
            .str.contains(
                search_text,
                na=False
            )
        ].copy()

        if not results.empty:

            st.success(
                f"Found {len(results)} customer(s)."
            )

            display_columns = [
                column
                for column in [
                    "CUSTOMER_ID",
                    "FIRST_NAME",
                    "LAST_NAME",
                    "CITY",
                    "STATE",
                    "AGE",
                    "OCCUPATION",
                ]
                if column in results.columns
            ]

            st.dataframe(
                results[display_columns],
                use_container_width=True,
                hide_index=True,
            )

            customer_options = (
                results["CUSTOMER_ID"]
                .astype(str)
                .tolist()
                if "CUSTOMER_ID"
                in results.columns
                else []
            )

            if customer_options:

                selected_customer = st.selectbox(
                    "Select customer to open Customer 360",
                    customer_options,
                )

                if st.button(
                    "🔍 Open Selected Customer",
                    use_container_width=True,
                ):

                    st.session_state[
                        "selected_customer_id"
                    ] = selected_customer

                    st.switch_page(
                        "pages/customer_360.py"
                    )

        else:

            st.warning(
                "No matching customers found."
            )


st.markdown("---")

st.subheader(
    "⚡ Quick Actions"
)

quick1, quick2, quick3 = st.columns(3)


with quick1:

    if st.button(
        "🔍 Customer 360",
        use_container_width=True,
    ):

        st.switch_page(
            "pages/customer_360.py"
        )


with quick2:

    if st.button(
        "⚡ Next Best Actions",
        use_container_width=True,
    ):

        st.switch_page(
            "pages/next_best_action.py"
        )


with quick3:

    if st.button(
        "📋 Action History",
        use_container_width=True,
    ):

        st.switch_page(
            "pages/action_history.py"
        )


st.markdown("---")

st.caption(
    "Dashboard metrics and customer risk indicators are "
    "calculated from the current Snowflake data. "
    "No simulated customer records are displayed."
)