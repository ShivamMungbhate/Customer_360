import streamlit as st
import pandas as pd

from utils.security import enforce_customer_boundary

from services.snowflake_service import (
    get_customer_profile,
    get_customer_policies,
    get_customer_claims,
)

enforce_customer_boundary()
st.markdown( """ <style> /* ============================== GLOBAL APP ============================== */ .stApp { background: radial-gradient( circle at 85% 5%, rgba(37, 99, 235, 0.12), transparent 28% ), radial-gradient( circle at 10% 20%, rgba(20, 184, 166, 0.08), transparent 25% ), #07111f; color: #e5edf7; } .block-container { max-width: 1450px; padding-top: 2rem; padding-bottom: 3rem; } /* ============================== HEADINGS ============================== */ h1, h2, h3, h4 { color: #f8fafc !important; letter-spacing: -0.02em; } h1 { font-size: 2.15rem !important; font-weight: 750 !important; } h2, h3 { font-weight: 700 !important; } p, label, .stCaption { color: #aebed0 !important; } /* ============================== METRIC CARDS ============================== */ [data-testid="stMetric"] { background: linear-gradient( 145deg, rgba(15, 31, 52, 0.95), rgba(9, 23, 40, 0.92) ); border: 1px solid rgba(71, 102, 138, 0.30); border-radius: 16px; padding: 18px 20px; min-height: 105px; box-shadow: 0 10px 30px rgba(0, 0, 0, 0.22), inset 0 1px 0 rgba(255, 255, 255, 0.035); transition: transform 0.18s ease, border-color 0.18s ease, box-shadow 0.18s ease; } [data-testid="stMetric"]:hover { transform: translateY(-3px); border-color: rgba(45, 212, 191, 0.55); box-shadow: 0 14px 35px rgba(0, 0, 0, 0.30), 0 0 20px rgba(20, 184, 166, 0.08); } [data-testid="stMetricLabel"] { color: #8fa4bb !important; font-size: 0.82rem !important; font-weight: 600 !important; } [data-testid="stMetricValue"] { color: #f8fafc !important; font-size: 1.65rem !important; font-weight: 750 !important; } /* ============================== DIVIDERS ============================== */ hr { border: none !important; height: 1px !important; background: linear-gradient( 90deg, transparent, rgba(71, 102, 138, 0.55), transparent ) !important; margin: 28px 0 !important; } /* ============================== INPUTS ============================== */ div[data-baseweb="input"] { background: rgba(11, 27, 45, 0.92) !important; border: 1px solid rgba(71, 102, 138, 0.42) !important; border-radius: 10px !important; transition: border-color 0.18s ease, box-shadow 0.18s ease; } div[data-baseweb="input"]:focus-within { border-color: rgba(45, 212, 191, 0.75) !important; box-shadow: 0 0 0 2px rgba(20, 184, 166, 0.10) !important; } div[data-baseweb="input"] input { color: #e5edf7 !important; } div[data-baseweb="input"] input::placeholder { color: #64748b !important; } /* ============================== SELECT BOX ============================== */ div[data-baseweb="select"] > div { background: rgba(11, 27, 45, 0.92) !important; border-color: rgba(71, 102, 138, 0.42) !important; border-radius: 10px !important; } div[data-baseweb="select"] span { color: #dbeafe !important; } /* ============================== CONTAINERS / CARDS ============================== */ div[data-testid="stVerticalBlockBorderWrapper"] { background: linear-gradient( 145deg, rgba(15, 31, 52, 0.94), rgba(8, 22, 38, 0.94) ); border: 1px solid rgba(71, 102, 138, 0.30) !important; border-radius: 16px !important; box-shadow: 0 10px 28px rgba(0, 0, 0, 0.20); padding: 5px; margin-bottom: 14px; transition: border-color 0.18s ease, transform 0.18s ease, box-shadow 0.18s ease; } div[data-testid="stVerticalBlockBorderWrapper"]:hover { border-color: rgba(45, 212, 191, 0.38) !important; box-shadow: 0 14px 35px rgba(0, 0, 0, 0.28), 0 0 20px rgba(20, 184, 166, 0.05); transform: translateY(-1px); } /* ============================== BUTTONS ============================== */ .stButton > button { background: linear-gradient( 135deg, #0f766e, #0891b2 ) !important; color: #ffffff !important; border: 1px solid rgba(103, 232, 249, 0.20) !important; border-radius: 9px !important; font-weight: 650 !important; min-height: 42px; box-shadow: 0 7px 18px rgba(8, 145, 178, 0.16); transition: transform 0.18s ease, box-shadow 0.18s ease, filter 0.18s ease; } .stButton > button:hover { filter: brightness(1.08); transform: translateY(-1px); box-shadow: 0 10px 24px rgba(8, 145, 178, 0.25); } /* ============================== PRIMARY BUTTON ============================== */ button[kind="primary"] { background: linear-gradient( 135deg, #0f766e, #0891b2 ) !important; color: white !important; border: none !important; } /* ============================== EXPANDERS ============================== */ [data-testid="stExpander"] { background: rgba(10, 28, 47, 0.88) !important; border: 1px solid rgba(71, 102, 138, 0.32) !important; border-radius: 12px !important; overflow: hidden; } [data-testid="stExpander"]:hover { border-color: rgba(45, 212, 191, 0.42) !important; } [data-testid="stExpander"] summary { color: #dce8f5 !important; font-weight: 650 !important; } /* ============================== TABS ============================== */ button[data-baseweb="tab"] { color: #8fa4bb !important; font-weight: 600 !important; } button[data-baseweb="tab"][aria-selected="true"] { color: #67e8f9 !important; } div[data-baseweb="tab-highlight"] { background-color: #14b8a6 !important; } /* ============================== ALERTS ============================== */ div[data-testid="stAlert"] { border-radius: 12px !important; border: 1px solid rgba(71, 102, 138, 0.30) !important; background: rgba(12, 29, 48, 0.90) !important; } div[data-testid="stAlert"] p { color: #d8e5f2 !important; } /* ============================== DATAFRAME ============================== */ [data-testid="stDataFrame"] { border: 1px solid rgba(71, 102, 138, 0.30); border-radius: 12px; overflow: hidden; box-shadow: 0 8px 25px rgba(0, 0, 0, 0.18); } /* ============================== SCROLLBAR ============================== */ ::-webkit-scrollbar { width: 8px; height: 8px; } ::-webkit-scrollbar-track { background: #07111f; } ::-webkit-scrollbar-thumb { background: #263b52; border-radius: 999px; } ::-webkit-scrollbar-thumb:hover { background: #36536f; } /* ============================== MOBILE ============================== */ @media (max-width: 900px) { .block-container { padding-left: 1rem; padding-right: 1rem; } h1 { font-size: 1.75rem !important; } } </style> """, unsafe_allow_html=True, )
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