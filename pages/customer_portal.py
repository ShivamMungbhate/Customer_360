'''import streamlit as st
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


enforce_customer_boundary()


customer_id = st.session_state.get("customer_id")

customer_id = st.session_state.get("customer_id")

# TEMPORARY.
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
    f"### Welcome back, {display_name} 👋"
)

st.caption(
    f"Customer ID: `{customer_id}`"
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
                    f"##### {policy_type}"
                )

                st.caption(
                    f"Policy ID: `{policy_id}`"
                )

                st.markdown(
                    f"Status: **{status}**"
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

                st.markdown(
                    f"**{claim_status}**"
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
                f"**{interaction_type}**"
            )

            st.caption(
                str(interaction_date)
            )

            if pd.notna(transcript) and str(transcript).strip():

                st.write(
                    str(transcript)
                )'''


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


# ============================================================
# CUSTOMER SECURITY
# ============================================================

enforce_customer_boundary()


# ============================================================
# CUSTOMER ID
# ============================================================

customer_id = st.session_state.get("customer_id")

# TEMPORARY:
# Keep this until authentication/customer IDs are fully aligned
# with the Snowflake customer IDs.
if not customer_id or str(customer_id).startswith("CUST-"):
    customer_id = "C001"

customer_id = str(customer_id).strip().upper()


# ============================================================
# LOAD CUSTOMER DATA
# ============================================================

profile_df = get_customer_profile(customer_id)
policies_df = get_customer_policies(customer_id)
claims_df = get_customer_claims(customer_id)
payments_df = get_customer_payments(customer_id)
interactions_df = get_customer_interactions(customer_id)


# ============================================================
# CUSTOMER VALIDATION
# ============================================================

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


# ============================================================
# HEADER
# ============================================================

st.markdown(
    f"### Welcome back, {display_name} 👋"
)

st.caption(
    f"Customer ID: `{customer_id}`"
)


# ============================================================
# DASHBOARD METRICS
# ============================================================

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


# ============================================================
# POLICIES
# ============================================================

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


        # ====================================================
        # POLICY CARD
        # ====================================================

        with st.container(border=True):

            col1, col2 = st.columns([2, 1])

            with col1:

                st.markdown(
                    f"##### {policy_type}"
                )

                st.caption(
                    f"Policy ID: `{policy_id}`"
                )

                st.markdown(
                    f"Status: **{status}**"
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


            # ====================================================
            # POLICY FEEDBACK
            # ====================================================

            st.markdown("---")

            st.markdown("##### ⭐ Policy Feedback")

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

                    # ------------------------------
                    # Validate comments
                    # ------------------------------

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


            # ====================================================
            # PREVIOUS FEEDBACK
            # ====================================================

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


# ============================================================
# CLAIMS
# ============================================================

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

                st.markdown(
                    f"**{claim_status}**"
                )


# ============================================================
# PAYMENTS
# ============================================================

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


# ============================================================
# RECENT INTERACTIONS
# ============================================================

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
                f"**{interaction_type}**"
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