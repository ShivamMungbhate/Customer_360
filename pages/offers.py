'''import streamlit as st
import pandas as pd

from utils.security import enforce_customer_boundary

from services.snowflake_service import (
    get_customer_profile,
    get_customer_policies,
    get_customer_claims,
)

enforce_customer_boundary()

customer_id = st.session_state.get("customer_id")

if not customer_id:
    st.error(
        "Customer identity is not available. "
        "Please sign in again."
    )
    st.stop()

customer_id = str(customer_id).strip().upper()


profile_df = get_customer_profile(customer_id)
policies_df = get_customer_policies(customer_id)
claims_df = get_customer_claims(customer_id)


display_name = st.session_state.get(
    "display_name",
    "Valued Customer"
)

if not profile_df.empty:

    customer = profile_df.iloc[0]

    first_name = str(
        customer.get("FIRST_NAME", "")
    ).strip()

    last_name = str(
        customer.get("LAST_NAME", "")
    ).strip()

    full_name = (
        f"{first_name} {last_name}"
    ).strip()

    if full_name:
        display_name = full_name



st.markdown(
    f"### 🎉 Offers & Recommendations for {display_name}"
)

st.caption(
    "Personalized opportunities based on your current "
    "insurance relationship and available policy data."
)

st.markdown("---")


policy_types = []

if (
    not policies_df.empty
    and "POLICY_TYPE" in policies_df.columns
):

    policy_types = (
        policies_df["POLICY_TYPE"]
        .dropna()
        .astype(str)
        .str.strip()
        .tolist()
    )


policy_types_upper = [
    policy.upper()
    for policy in policy_types
]


active_policies = 0

if (
    not policies_df.empty
    and "STATUS" in policies_df.columns
):

    active_policies = int(
        policies_df["STATUS"]
        .astype(str)
        .str.upper()
        .eq("ACTIVE")
        .sum()
    )
open_claims = 0

if (
    not claims_df.empty
    and "CLAIM_STATUS" in claims_df.columns
):

    open_claims = int(
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
col1, col2, col3 = st.columns(3)

col1.metric(
    "Active Policies",
    active_policies
)

col2.metric(
    "Total Policies",
    len(policies_df)
)

col3.metric(
    "Open Claims",
    open_claims
)


st.markdown("---")
offers = []
has_health = any(
    "HEALTH" in policy
    for policy in policy_types_upper
)

if has_health:

    offers.append(
        {
            "title": "🏥 Health Coverage Enhancement",
            "type": "Coverage Enhancement",
            "benefit": "Explore additional health protection",
            "description": (
                "You already have health insurance with us. "
                "Review available coverage enhancements, "
                "including additional protection options "
                "that may be available for your profile."
            ),
            "button": "Explore Health Options",
            "key": "health_offer",
        }
    )
if active_policies >= 2:

    offers.append(
        {
            "title": "🎁 Multi-Policy Relationship Benefits",
            "type": "Loyalty Opportunity",
            "benefit": "Review benefits available across your policies",
            "description": (
                "You currently have multiple active policies. "
                "Review whether additional relationship or "
                "bundling benefits are available."
            ),
            "button": "View Benefits",
            "key": "multi_policy_offer",
        }
    )
if active_policies > 0:

    offers.append(
        {
            "title": "🛡️ Review Your Protection Coverage",
            "type": "Coverage Review",
            "benefit": "Check whether your current protection still fits your needs",
            "description": (
                "Your current policies can be reviewed for "
                "coverage gaps, renewal requirements and "
                "additional protection options."
            ),
            "button": "Review Coverage",
            "key": "coverage_offer",
        }
    )
if active_policies == 0:

    offers.append(
        {
            "title": "🛡️ Explore Insurance Protection",
            "type": "Insurance Options",
            "benefit": "Explore available insurance products",
            "description": (
                "No active policy was found for your customer "
                "profile. Explore available insurance options "
                "with your relationship manager."
            ),
            "button": "Explore Options",
            "key": "general_offer",
        }
    )
st.subheader("✨ Available Opportunities")


if not offers:

    st.info(
        "No personalized offers are currently available."
    )

else:

    for offer in offers:

        with st.container(border=True):

            col1, col2 = st.columns(
                [3, 1]
            )

            with col1:

                st.markdown(
                    f"##### {offer['title']}"
                )

                st.markdown(
                    f"**Type:** `{offer['type']}`"
                )

                st.markdown(
                    f"**Benefit:** {offer['benefit']}"
                )

                st.caption(
                    offer["description"]
                )

            with col2:

                st.write("")

                if st.button(
                    offer["button"],
                    key=offer["key"],
                    use_container_width=True,
                    type="primary",
                ):

                    st.info(
                        "This opportunity has been noted. "
                        "Your relationship manager can help "
                        "you review the available options."
                    )
st.markdown("---")

st.caption(
    "Offers shown here are informational recommendations "
    "based on available customer and policy data. "
    "Final eligibility, pricing and discounts are subject "
    "to applicable policy rules and verification."
)'''


import streamlit as st
import pandas as pd

from utils.security import enforce_customer_boundary

from services.snowflake_service import (
    get_customer_profile,
    get_customer_policies,
    get_customer_claims,
)

enforce_customer_boundary()

customer_id = st.session_state.get("customer_id")

if not customer_id:
    st.error(
        "Customer identity is not available. "
        "Please sign in again."
    )
    st.stop()

customer_id = str(customer_id).strip().upper()

profile_df = get_customer_profile(customer_id)
policies_df = get_customer_policies(customer_id)
claims_df = get_customer_claims(customer_id)

display_name = st.session_state.get(
    "display_name",
    "Valued Customer"
)

if not profile_df.empty:

    customer = profile_df.iloc[0]

    first_name = str(
        customer.get("FIRST_NAME", "")
    ).strip()

    last_name = str(
        customer.get("LAST_NAME", "")
    ).strip()

    full_name = (
        f"{first_name} {last_name}"
    ).strip()

    if full_name:
        display_name = full_name

st.markdown(
    f"### 🎉 Offers & Recommendations for {display_name}"
)

st.caption(
    "Personalized opportunities based on your current "
    "insurance relationship and available policy data."
)

st.markdown("---")

policy_types = []

if (
    not policies_df.empty
    and "POLICY_TYPE" in policies_df.columns
):

    policy_types = (
        policies_df["POLICY_TYPE"]
        .dropna()
        .astype(str)
        .str.strip()
        .tolist()
    )

policy_types_upper = [
    policy.upper()
    for policy in policy_types
]

active_policies = 0

if (
    not policies_df.empty
    and "STATUS" in policies_df.columns
):

    active_policies = int(
        policies_df["STATUS"]
        .astype(str)
        .str.upper()
        .eq("ACTIVE")
        .sum()
    )

open_claims = 0

if (
    not claims_df.empty
    and "CLAIM_STATUS" in claims_df.columns
):

    open_claims = int(
        (
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
    )

col1, col2, col3 = st.columns(3)

col1.metric(
    "Active Policies",
    active_policies
)

col2.metric(
    "Total Policies",
    len(policies_df)
)

col3.metric(
    "Open Claims",
    open_claims
)

st.markdown("---")

offers = []

has_health = any(
    "HEALTH" in policy
    for policy in policy_types_upper
)

if has_health:

    offers.append(
        {
            "title": "🏥 Health Coverage Enhancement",
            "type": "Coverage Enhancement",
            "benefit": "Explore additional health protection",
            "description": (
                "You already have health insurance with us. "
                "Review available coverage enhancements, "
                "including additional protection options "
                "that may be available for your profile."
            ),
            "button": "Explore Health Options",
            "key": "health_offer",
        }
    )

if active_policies >= 2:

    offers.append(
        {
            "title": "🎁 Multi-Policy Relationship Benefits",
            "type": "Loyalty Opportunity",
            "benefit": "Review benefits available across your policies",
            "description": (
                "You currently have multiple active policies. "
                "Review whether additional relationship or "
                "bundling benefits are available."
            ),
            "button": "View Benefits",
            "key": "multi_policy_offer",
        }
    )

if active_policies > 0:

    offers.append(
        {
            "title": "🛡️ Review Your Protection Coverage",
            "type": "Coverage Review",
            "benefit": (
                "Check whether your current protection "
                "still fits your needs"
            ),
            "description": (
                "Your current policies can be reviewed for "
                "coverage gaps, renewal requirements and "
                "additional protection options."
            ),
            "button": "Review Coverage",
            "key": "coverage_offer",
        }
    )

if active_policies == 0:

    offers.append(
        {
            "title": "🛡️ Explore Insurance Protection",
            "type": "Insurance Options",
            "benefit": "Explore available insurance products",
            "description": (
                "No active policy was found for your customer "
                "profile. Explore available insurance options "
                "with your relationship manager."
            ),
            "button": "Explore Options",
            "key": "general_offer",
        }
    )

st.subheader("✨ Available Opportunities")

if not offers:

    st.info(
        "No personalized offers are currently available."
    )

else:

    for offer in offers:

        with st.container(border=True):

            col1, col2 = st.columns(
                [3, 1]
            )

            with col1:

                st.markdown(
                    f"##### {offer['title']}"
                )

                st.markdown(
                    f"**Type:** `{offer['type']}`"
                )

                st.markdown(
                    f"**Benefit:** {offer['benefit']}"
                )

                st.caption(
                    offer["description"]
                )

            with col2:

                st.write("")

                if st.button(
                    offer["button"],
                    key=offer["key"],
                    use_container_width=True,
                    type="primary",
                ):

                    st.info(
                        "This opportunity has been noted. "
                        "Your relationship manager can help "
                        "you review the available options."
                    )

st.markdown("---")

st.caption(
    "Offers shown here are informational recommendations "
    "based on available customer and policy data. "
    "Final eligibility, pricing and discounts are subject "
    "to applicable policy rules and verification."
)