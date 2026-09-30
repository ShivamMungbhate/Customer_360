import streamlit as st
from utils.security import enforce_customer_boundary


enforce_customer_boundary()

display_name = st.session_state.get("display_name", "Valued Customer")
st.markdown(f"### 🎉 Exclusive Offers & Recommendations for {display_name}")
st.write("Explore personalized policy discounts, loyalty rewards, and cross-sell benefits curated for you by our AI Next Best Action engine.")

st.markdown("---")


with st.container(border=True):
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("##### 🛡️ Cyber Shield Add-on Extension")
        st.markdown("**Discount:** `20% OFF` your first year &nbsp;|&nbsp; **Status:** Pre-approved")
        st.caption("Based on your active Home & Health insurance bundle, protect your digital assets and online family accounts against emerging cyber risks.")
    with col2:
        st.write("")
        if st.button("Claim Offer", key="offer_1", type="primary", use_container_width=True):
            st.success("Offer claimed successfully! Your agent will reach out shortly.")

with st.container(border=True):
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("##### 🚗 Safe Driver Car Insurance Renewal Bonus")
        st.markdown("**Discount:** `15% No-Claim Bonus` &nbsp;|&nbsp; **Expires:** In 30 days")
        st.caption("You have maintained zero claim logs on your vehicle policy this term. Apply this reward instantly to your upcoming renewal.")
    with col2:
        st.write("")
        if st.button("Apply Bonus", key="offer_2", type="primary", use_container_width=True):
            st.success("No-claim bonus applied to your renewal invoice!")

with st.container(border=True):
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("##### 🏥 Comprehensive Health Plus Family Top-up")
        st.markdown("**Benefit:** `Free Health Checkup Voucher` included")
        st.caption("Upgrade your current health coverage tier to include critical illness protection and annual dental screenings.")
    with col2:
        st.write("")
        if st.button("Learn More", key="offer_3", use_container_width=True):
            st.info("Brochure downloaded to your account messages.")