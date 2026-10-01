import pandas as pd

from services.snowflake_service import (
    get_customer_profile,
    get_customer_policies,
    get_customer_claims,
    get_customer_payments,
    get_customer_interactions,
)


def _safe_datetime(df, column):
    """
    Safely convert a dataframe column to datetime.
    """

    if df.empty or column not in df.columns:
        return pd.Series(dtype="datetime64[ns]")

    return pd.to_datetime(
        df[column],
        errors="coerce"
    )


def _status_count(df, column, statuses):
    """
    Count records whose status matches one of the supplied statuses.
    """

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


def generate_next_best_action(customer_id: str):
    """
    Generate transparent, evidence-based recommendations
    for a customer.

    This function only generates recommendations.

    It does NOT:
    - create ACTION_HISTORY records
    - modify customer data
    - modify policies
    - send notifications
    - execute an action

    Returns:
        list[dict]
    """

    customer_id = (
        str(customer_id)
        .strip()
        .upper()
    )

    if not customer_id:
        return []

    profile_df = get_customer_profile(
        customer_id
    )

    if profile_df.empty:
        return []


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


    recommendations = []


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


    if (
        not policies_df.empty
        and "RENEWAL_DATE"
        in policies_df.columns
    ):

        renewal_dates = _safe_datetime(
            policies_df,
            "RENEWAL_DATE"
        )

        today = pd.Timestamp.today().normalize()

        days_to_renewal = (
            renewal_dates - today
        ).dt.days

        upcoming = days_to_renewal[
            (days_to_renewal >= 0)
            &
            (days_to_renewal <= 30)
        ]

        if not upcoming.empty:

            nearest_days = int(
                upcoming.min()
            )

            recommendations.append(
                {
                    "customer_id": customer_id,
                    "customer_name": customer_name,
                    "action_type": "RENEWAL_FOLLOW_UP",
                    "action": "Schedule renewal follow-up",
                    "reason": (
                        f"Customer has a policy renewal "
                        f"within {nearest_days} days."
                    ),
                    "priority": "HIGH",
                    "confidence": 0.90,
                    "evidence": {
                        "renewal_days": nearest_days,
                        "renewal_rule": "0-30 days",
                    },
                }
            )



    open_claims = _status_count(
        claims_df,
        "CLAIM_STATUS",
        {
            "OPEN",
            "PENDING",
            "IN_PROGRESS",
            "UNDER_INVESTIGATION",
        }
    )

    if open_claims > 0:

        recommendations.append(
            {
                "customer_id": customer_id,
                "customer_name": customer_name,
                "action_type": "CLAIMS_FOLLOW_UP",
                "action": "Review pending claim with customer",
                "reason": (
                    f"Customer has {open_claims} "
                    f"open or pending claim(s)."
                ),
                "priority": "MEDIUM",
                "confidence": 0.85,
                "evidence": {
                    "open_claims": open_claims,
                    "claim_statuses": [
                        "OPEN",
                        "PENDING",
                        "IN_PROGRESS",
                        "UNDER_INVESTIGATION",
                    ],
                },
            }
        )


    interaction_count = len(
        interactions_df
    )

    if interaction_count >= 3:

        recommendations.append(
            {
                "customer_id": customer_id,
                "customer_name": customer_name,
                "action_type": "CUSTOMER_SERVICE_FOLLOW_UP",
                "action": "Proactive customer service follow-up",
                "reason": (
                    f"Customer has {interaction_count} "
                    f"recorded interactions."
                ),
                "priority": "MEDIUM",
                "confidence": 0.75,
                "evidence": {
                    "interaction_count": interaction_count,
                    "threshold": 3,
                },
            }
        )


    payment_risk = _status_count(
        payments_df,
        "PAYMENT_STATUS",
        {
            "OVERDUE",
            "LATE",
            "FAILED",
        }
    )

    if payment_risk > 0:

        recommendations.append(
            {
                "customer_id": customer_id,
                "customer_name": customer_name,
                "action_type": "PAYMENT_FOLLOW_UP",
                "action": "Follow up on payment status",
                "reason": (
                    f"Customer has {payment_risk} "
                    f"payment record(s) requiring attention."
                ),
                "priority": "HIGH",
                "confidence": 0.90,
                "evidence": {
                    "payment_risk_records": payment_risk,
                    "risk_statuses": [
                        "OVERDUE",
                        "LATE",
                        "FAILED",
                    ],
                },
            }
        )


    if not recommendations:

        recommendations.append(
            {
                "customer_id": customer_id,
                "customer_name": customer_name,
                "action_type": "NO_ACTION",
                "action": "No immediate action required",
                "reason": (
                    "No configured operational risk "
                    "or follow-up condition was detected."
                ),
                "priority": "LOW",
                "confidence": 0.70,
                "evidence": {},
            }
        )


    priority_order = {
        "HIGH": 1,
        "MEDIUM": 2,
        "LOW": 3,
    }

    recommendations.sort(
        key=lambda item: priority_order.get(
            item.get("priority", "LOW"),
            3,
        )
    )


    return recommendations