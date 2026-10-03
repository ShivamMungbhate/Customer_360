import pandas as pd

from services.snowflake_service import (
    get_customer_profile,
    get_customer_policies,
    get_customer_claims,
    get_customer_payments,
    get_customer_interactions,
    get_ai_insights,
)


def fetch_customer_360(customer_id: str):
    """
    Fetch the complete Customer 360 dataset for a customer.

    Returns a dictionary containing:
        - profile
        - policies
        - claims
        - payments
        - interactions
        - ai_insights

    No data is modified by this function.
    """
    customer_id = (
        str(customer_id)
        .strip()
        .upper()
    )

    if not customer_id:
        return None

    profile_df = get_customer_profile(
        customer_id
    )

    if profile_df.empty:
        return None


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


    insights_df = get_ai_insights(
        customer_id
    )


    customer = profile_df.iloc[0]

    first_name = str(
        customer.get(
            "FIRST_NAME",
            ""
        )
    ).strip()

    last_name = str(
        customer.get(
            "LAST_NAME",
            ""
        )
    ).strip()

    customer_name = (
        f"{first_name} {last_name}"
    ).strip()

    if not customer_name:
        customer_name = customer_id


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
        and "CLAIM_STATUS"
        in claims_df.columns
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
        ).sum())


    return {
        "customer_id": customer_id,
        "customer_name": customer_name,

        "profile": profile_df,

        "policies": policies_df,

        "claims": claims_df,

        "payments": payments_df,

        "interactions": interactions_df,

        "ai_insights": insights_df,

        "summary": {
            "total_policies": len(
                policies_df
            ),
            "active_policies": active_policies,
            "total_claims": len(
                claims_df
            ),
            "open_claims": open_claims,
            "total_payments": len(
                payments_df
            ),
            "total_interactions": len(
                interactions_df
            ),
            "total_ai_insights": len(
                insights_df
            ),
        },
    }