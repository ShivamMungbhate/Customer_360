import streamlit as st
import pandas as pd

from utils.security import enforce_employee_boundary

from services.snowflake_service import (
    get_all_customers,
    get_customer_policies,
    get_customer_claims,
    get_customer_payments,
    get_customer_interactions,
    get_ai_insights,
)
enforce_employee_boundary()

st.title("⚡ Next Best Action")
st.caption(
    "Live customer recommendations based on Snowflake data. "
    "AI insights will be integrated later."
)


customers_df = get_all_customers()

if customers_df.empty:
    st.warning("No customer data is currently available.")
    st.stop()

if "CUSTOMER_ID" not in customers_df.columns:
    st.error("CUSTOMERS table is missing CUSTOMER_ID.")
    st.stop()

st.subheader("🔎 Customer Selection")

search_text = st.text_input(
    "Search by Customer ID, first name, last name, city or state",
    placeholder="Example: CUST-1001 or Rahul"
)


filtered_customers = customers_df.copy()


if search_text.strip():

    search_text = search_text.strip().lower()

    searchable_columns = [
        "CUSTOMER_ID",
        "FIRST_NAME",
        "LAST_NAME",
        "CITY",
        "STATE",
    ]

    existing_columns = [
        col
        for col in searchable_columns
        if col in filtered_customers.columns
    ]

    mask = pd.Series(
        False,
        index=filtered_customers.index
    )

    for column in existing_columns:

        mask = mask | (
            filtered_customers[column]
            .astype(str)
            .str.lower()
            .str.contains(
                search_text,
                na=False
            )
        )

    filtered_customers = filtered_customers[mask]


if filtered_customers.empty:

    st.warning(
        "No customers matched your search."
    )

    st.stop()


# ============================================================
# CUSTOMER OPTIONS
# ============================================================

customer_options = []

customer_lookup = {}


for _, row in filtered_customers.iterrows():

    customer_id = str(
        row.get("CUSTOMER_ID", "")
    ).strip()

    if not customer_id:
        continue

    first_name = str(
        row.get("FIRST_NAME", "")
    ).strip()

    last_name = str(
        row.get("LAST_NAME", "")
    ).strip()

    full_name = (
        f"{first_name} {last_name}"
    ).strip()

    if not full_name:
        full_name = "Customer"

    label = (
        f"{customer_id} — {full_name}"
    )

    customer_options.append(label)
    customer_lookup[label] = customer_id


if not customer_options:

    st.warning("No valid customers found.")
    st.stop()


selected_customer_label = st.selectbox(
    "Select customer",
    customer_options
)


customer_id = customer_lookup[
    selected_customer_label
]

customer_rows = customers_df[
    customers_df["CUSTOMER_ID"]
    .astype(str)
    .str.upper()
    .eq(customer_id.upper())
]


if customer_rows.empty:

    st.error(
        f"Customer {customer_id} could not be loaded."
    )

    st.stop()


customer = customer_rows.iloc[0]


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

with st.spinner("Loading customer data..."):

    policies_df = get_customer_policies(
        customer_id
    )

    claims_df = get_customer_claims(
        customer_id
    )

    payments_df = get_customer_payments(
        customer_id
    )

    interactions_df = get_customer_interactions(
        customer_id
    )

ai_insights_df = pd.DataFrame()

st.markdown("---")

st.subheader(
    f"👤 {customer_name}"
)

st.caption(
    f"Customer ID: {customer_id}"
)


col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "Policies",
        len(policies_df)
    )


with col2:

    st.metric(
        "Claims",
        len(claims_df)
    )


with col3:

    st.metric(
        "Payments",
        len(payments_df)
    )


with col4:

    st.metric(
        "Interactions",
        len(interactions_df)
    )
with st.expander("👤 Customer Profile"):

    profile_data = {}

    for column in [
        "CUSTOMER_ID",
        "FIRST_NAME",
        "LAST_NAME",
        "AGE",
        "CITY",
        "STATE",
        "OCCUPATION",
        "ANNUAL_INCOME",
    ]:

        if column in customer.index:

            profile_data[column] = customer[column]

    if profile_data:

        profile_df = pd.DataFrame(
            list(profile_data.items()),
            columns=[
                "Field",
                "Value"
            ]
        )

        st.dataframe(
            profile_df,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info(
            "No additional profile fields available."
        )

recommendations = []

if (
    not policies_df.empty
    and "RENEWAL_DATE" in policies_df.columns
):

    today = pd.Timestamp.now().normalize()

    for _, policy in policies_df.iterrows():

        renewal_date = pd.to_datetime(
            policy.get("RENEWAL_DATE"),
            errors="coerce"
        )

        if pd.isna(renewal_date):
            continue

        days_to_renewal = (
            renewal_date.normalize()
            - today
        ).days

        status = str(
            policy.get("STATUS", "")
        ).strip().upper()

        if (
            status == "ACTIVE"
            and 0 <= days_to_renewal <= 30
        ):

            policy_id = str(
                policy.get(
                    "POLICY_ID",
                    "N/A"
                )
            )

            recommendations.append({

                "ACTION_TYPE": "RETENTION",

                "ACTION": "Renewal follow-up",

                "PRIORITY": "HIGH",

                "REASON": (
                    f"Policy {policy_id} "
                    f"renews in "
                    f"{days_to_renewal} day(s)."
                ),

                "EVIDENCE": (
                    f"Renewal date: "
                    f"{renewal_date.date()}"
                ),

            })

if not claims_df.empty:

    claim_status_column = None

    for column in [
        "CLAIM_STATUS",
        "STATUS",
    ]:

        if column in claims_df.columns:

            claim_status_column = column
            break


    if claim_status_column:

        open_statuses = {
            "OPEN",
            "PENDING",
            "IN PROGRESS",
            "PROCESSING",
            "UNDER REVIEW",
        }

        open_claims = claims_df[
            claims_df[
                claim_status_column
            ]
            .astype(str)
            .str.upper()
            .isin(open_statuses)
        ]


        if not open_claims.empty:

            recommendations.append({

                "ACTION_TYPE": "CLAIMS",

                "ACTION": "Claims follow-up",

                "PRIORITY": "MEDIUM",

                "REASON": (
                    f"{len(open_claims)} "
                    "claim(s) currently "
                    "require attention."
                ),

                "EVIDENCE": (
                    f"Open/pending claims: "
                    f"{len(open_claims)}"
                ),

            })

if not payments_df.empty:

    payment_status_column = None

    for column in [
        "PAYMENT_STATUS",
        "STATUS",
    ]:

        if column in payments_df.columns:

            payment_status_column = column
            break


    if payment_status_column:

        payment_attention_statuses = {
            "OVERDUE",
            "LATE",
            "FAILED",
            "PENDING",
        }

        attention_payments = payments_df[
            payments_df[
                payment_status_column
            ]
            .astype(str)
            .str.upper()
            .isin(
                payment_attention_statuses
            )
        ]


        if not attention_payments.empty:

            recommendations.append({

                "ACTION_TYPE": "PAYMENT",

                "ACTION": "Payment follow-up",

                "PRIORITY": "HIGH",

                "REASON": (
                    f"{len(attention_payments)} "
                    "payment record(s) "
                    "require attention."
                ),

                "EVIDENCE": (
                    "Payment status indicates "
                    "overdue, late, failed, "
                    "or pending payment."
                ),

            })


if len(interactions_df) >= 3:

    recommendations.append({

        "ACTION_TYPE": "SERVICE",

        "ACTION": (
            "Proactive customer service "
            "follow-up"
        ),

        "PRIORITY": "MEDIUM",

        "REASON": (
            f"Customer has "
            f"{len(interactions_df)} "
            "recorded interactions."
        ),

        "EVIDENCE": (
            "Interaction history"
        ),

    })

if (
    not interactions_df.empty
    and "INTERACTION_DATE"
    in interactions_df.columns
):

    interaction_dates = pd.to_datetime(
        interactions_df[
            "INTERACTION_DATE"
        ],
        errors="coerce"
    )

    valid_dates = (
        interaction_dates
        .dropna()
    )


    if not valid_dates.empty:

        latest_interaction = (
            valid_dates.max()
        )

        days_since = (
            pd.Timestamp.now().normalize()
            - latest_interaction.normalize()
        ).days


        if 0 <= days_since <= 7:

            recommendations.append({

                "ACTION_TYPE": "SERVICE",

                "ACTION": (
                    "Review recent "
                    "customer interaction"
                ),

                "PRIORITY": "LOW",

                "REASON": (
                    "Customer had a recent "
                    "interaction."
                ),

                "EVIDENCE": (
                    f"Latest interaction: "
                    f"{latest_interaction.date()}"
                ),

            })

unique_recommendations = []

seen = set()


for recommendation in recommendations:

    key = (
        recommendation["ACTION_TYPE"],
        recommendation["ACTION"]
    )

    if key not in seen:

        seen.add(key)

        unique_recommendations.append(
            recommendation
        )


recommendations = (
    unique_recommendations
)

priority_order = {
    "HIGH": 1,
    "MEDIUM": 2,
    "LOW": 3,
}


recommendations = sorted(
    recommendations,
    key=lambda item: priority_order.get(
        item["PRIORITY"],
        99
    )
)


st.markdown("---")

st.subheader("⚡ Recommended Actions")


if not recommendations:

    st.success(
        "No rule-based action is currently "
        "required from the available data."
    )

else:

    st.caption(
        f"{len(recommendations)} "
        "recommendation(s) generated "
        "from live customer data."
    )


    for index, recommendation in enumerate(
        recommendations,
        start=1
    ):

        with st.container(border=True):

            col1, col2 = st.columns(
                [5, 1]
            )


            with col1:

                st.markdown(
                    f"### {index}. "
                    f"{recommendation['ACTION']}"
                )

                st.write(
                    recommendation["REASON"]
                )

                st.caption(
                    f"Type: "
                    f"{recommendation['ACTION_TYPE']}"
                )

                st.caption(
                    f"Evidence: "
                    f"{recommendation['EVIDENCE']}"
                )


            with col2:

                st.metric(
                    "Priority",
                    recommendation[
                        "PRIORITY"
                    ]
                )

st.markdown("---")

st.subheader(
    "📚 Supporting Customer Data"
)


tab1, tab2, tab3, tab4 = st.tabs(
    [
        "🛡️ Policies",
        "📑 Claims",
        "💳 Payments",
        "💬 Interactions",
    ]
)


with tab1:

    if policies_df.empty:

        st.info(
            "No policy records found."
        )

    else:

        st.dataframe(
            policies_df,
            use_container_width=True,
            hide_index=True
        )


with tab2:

    if claims_df.empty:

        st.info(
            "No claim records found."
        )

    else:

        st.dataframe(
            claims_df,
            use_container_width=True,
            hide_index=True
        )


with tab3:

    if payments_df.empty:

        st.info(
            "No payment records found."
        )

    else:

        st.dataframe(
            payments_df,
            use_container_width=True,
            hide_index=True
        )


with tab4:

    if interactions_df.empty:

        st.info(
            "No interaction records found."
        )

    else:

        st.dataframe(
            interactions_df,
            use_container_width=True,
            hide_index=True
        )

st.markdown("---")

st.subheader("🤖 AI Insights")

st.info(
    "AI insights are reserved for the next phase. "
    "The NBA engine is currently using live "
    "customer, policy, claim, payment, and "
    "interaction data only."
)

st.subheader("📌 Action Execution")

st.info(
    "Action creation and ACTION_HISTORY persistence "
    "will be enabled in the action-management phase."
)