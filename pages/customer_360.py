import streamlit as st
import pandas as pd

from services.snowflake_service import (
    get_customer_profile,
    get_customer_policies,
    get_customer_claims,
    get_customer_interactions,
    get_ai_insights,
)


st.title("🔍 Customer 360 View")
st.caption("Live customer data from Snowflake")

customer_id = st.text_input(
    "Search Customer ID",
    placeholder="Example: C001",
)

if st.button("🔎 Search Customer", type="primary"):

    customer_id = str(customer_id).strip().upper()

    if not customer_id:
        st.warning("Please enter a Customer ID.")
        st.stop()

    profile_df = get_customer_profile(customer_id)

    if profile_df.empty:
        st.error(
            f"No customer record found in Snowflake for `{customer_id}`."
        )
        st.stop()

    customer = profile_df.iloc[0]

    first_name = str(customer.get("FIRST_NAME", "")).strip()
    last_name = str(customer.get("LAST_NAME", "")).strip()

    customer_name = f"{first_name} {last_name}".strip()

    if not customer_name:
        customer_name = customer_id

    st.success(f"Customer found: {customer_name}")

    st.markdown("---")


    st.subheader("👤 Customer Profile")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Customer ID",
            customer.get("CUSTOMER_ID", customer_id)
        )

    with col2:
        st.metric(
            "Name",
            customer_name
        )

    with col3:
        st.metric(
            "City",
            customer.get("CITY", "N/A")
        )

    with col4:
        st.metric(
            "State",
            customer.get("STATE", "N/A")
        )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Occupation",
            customer.get("OCCUPATION", "N/A")
        )

    with col2:
        income = customer.get("ANNUAL_INCOME")

        if pd.notna(income):
            st.metric(
                "Annual Income",
                f"₹{float(income):,.0f}"
            )
        else:
            st.metric("Annual Income", "N/A")

    with col3:
        st.metric(
            "Age",
            customer.get("AGE", "N/A")
        )

    st.markdown("---")
    st.subheader("🛡️ Policies")

    policies_df = get_customer_policies(customer_id)

    if policies_df.empty:

        st.info("No policy records found.")

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

    claims_df = get_customer_claims(customer_id)

    if claims_df.empty:

        st.info("No claim records found.")

    else:

        if "CLAIM_STATUS" in claims_df.columns:

            open_claims = (
                ~claims_df["CLAIM_STATUS"]
                .astype(str)
                .str.upper()
                .isin(["CLOSED", "SETTLED", "REJECTED"])
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


    st.subheader("💬 Interactions & Call Transcripts")

    interactions_df = get_customer_interactions(customer_id)

    if interactions_df.empty:

        st.info("No interaction records found.")

    else:

        st.caption(
            f"Total interactions: {len(interactions_df)}"
        )

        for index, row in interactions_df.iterrows():

            interaction_type = str(
                row.get("INTERACTION_TYPE", "Interaction")
            )

            interaction_date = str(
                row.get("INTERACTION_DATE", "Date unavailable")
            )

            transcript = row.get(
                "TRANSCRIPT",
                "No transcript recorded."
            )

            if pd.isna(transcript):
                transcript = "No transcript recorded."

            with st.expander(
                f"💬 {interaction_type} — {interaction_date}"
            ):

                st.markdown("**Transcript**")

                st.write(str(transcript))

                
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
                                f"**{field.replace('_', ' ').title()}:** {value}"
                            )

                if extra_fields:

                    st.markdown(
                        "  \n".join(extra_fields)
                    )

    st.markdown("---")

    st.subheader("🤖 AI Insights")

    insights_df = get_ai_insights(customer_id)

    if insights_df.empty:

        st.info(
            "No AI insights are available for this customer yet."
        )

    else:

        st.caption(
            f"AI insight records: {len(insights_df)}"
        )
        insight = insights_df.iloc[0]

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "Sentiment",
                insight.get("SENTIMENT", "UNKNOWN")
            )

        with col2:
            st.metric(
                "Intent",
                insight.get("INTENT", "UNKNOWN")
            )

        with col3:
            st.metric(
                "Churn Signal",
                insight.get("CHURN_SIGNAL", "UNKNOWN")
            )

        with col4:
            st.metric(
                "Urgency",
                insight.get("URGENCY", "UNKNOWN")
            )

        st.markdown("#### Insight Details")

  
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

                value = insight.get(field)

                if pd.notna(value):
                    insight_display[
                        field.replace("_", " ").title()
                    ] = value

        if insight_display:
            st.dataframe(
                pd.DataFrame(
                    list(insight_display.items()),
                    columns=["Field", "Value"]
                ),
                use_container_width=True,
                hide_index=True,
            )

        st.markdown("#### Raw AI Insight Record")

        st.dataframe(
            insights_df,
            use_container_width=True,
            hide_index=True,
        )

    st.markdown("---")

    st.subheader("📊 Customer 360 Summary")

    summary_col1, summary_col2, summary_col3, summary_col4 = st.columns(4)

    with summary_col1:
        st.metric(
            "Policies",
            len(policies_df)
        )

    with summary_col2:
        st.metric(
            "Claims",
            len(claims_df)
        )

    with summary_col3:
        st.metric(
            "Interactions",
            len(interactions_df)
        )

    with summary_col4:
        st.metric(
            "AI Insights",
            len(insights_df)
        )