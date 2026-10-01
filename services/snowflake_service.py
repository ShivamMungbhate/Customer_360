import streamlit as st
import pandas as pd

@st.cache_resource
def get_db_connection():
    """
    Create and cache the Snowflake connection.

    Credentials are read from:
    .streamlit/secrets.toml
    """
    return st.connection("snowflake", type="snowflake")

def _normalize_customer_id(customer_id: str) -> str:
    """
    Normalize customer IDs before querying Snowflake.

    Example:
        ' c001 ' -> 'C001'
    """
    if customer_id is None:
        return ""

    return str(customer_id).strip().upper()


def _empty_dataframe() -> pd.DataFrame:
    """Return an empty DataFrame when a query fails."""
    return pd.DataFrame()

def get_customer_profile(customer_id: str) -> pd.DataFrame:
    """Fetch live customer profile from Snowflake CUSTOMERS table."""

    customer_id = _normalize_customer_id(customer_id)

    if not customer_id:
        return _empty_dataframe()

    try:
        conn = get_db_connection()

        query = """
            SELECT *
            FROM CUSTOMERS
            WHERE CUSTOMER_ID = ?
        """

        return conn.query(
            query,
            params=(customer_id,),
            ttl=0
        )

    except Exception as e:
        st.error(f"Error fetching customer profile: {e}")
        return _empty_dataframe()

def search_customers(search_text: str) -> pd.DataFrame:
    """Search customers by ID, name, city or state."""

    search_text = str(search_text).strip()

    if not search_text:
        return _empty_dataframe()

    try:
        conn = get_db_connection()

        search_pattern = f"%{search_text}%"

        query = """
            SELECT *
            FROM CUSTOMERS
            WHERE
                CUSTOMER_ID ILIKE ?
                OR FIRST_NAME ILIKE ?
                OR LAST_NAME ILIKE ?
                OR CITY ILIKE ?
                OR STATE ILIKE ?
            ORDER BY FIRST_NAME, LAST_NAME
        """

        return conn.query(
            query,
            params=(
        search_pattern,
        search_pattern,
        search_pattern,
        search_pattern,
        search_pattern,
    ),
    ttl=0
)

    except Exception as e:
        st.error(f"Error searching customers: {e}")
        return _empty_dataframe()

def get_customer_policies(customer_id: str) -> pd.DataFrame:
    """Fetch policies associated with a customer."""

    customer_id = _normalize_customer_id(customer_id)

    if not customer_id:
        return _empty_dataframe()

    try:
        conn = get_db_connection()

        query = """
            SELECT *
            FROM POLICIES
            WHERE CUSTOMER_ID = ?
            ORDER BY RENEWAL_DATE
        """

        return conn.query(
            query,
            params=(customer_id,),
            ttl=0
        )

    except Exception as e:
        st.error(f"Error fetching policies: {e}")
        return _empty_dataframe()

def get_customer_claims(customer_id: str) -> pd.DataFrame:
    """Fetch claims associated with a customer."""

    customer_id = _normalize_customer_id(customer_id)

    if not customer_id:
        return _empty_dataframe()

    try:
        conn = get_db_connection()

        query = """
            SELECT *
            FROM CLAIMS
            WHERE CUSTOMER_ID = ?
            ORDER BY CLAIM_DATE DESC
        """

        return conn.query(
            query,
            params=(customer_id,),
            ttl=0
        )

    except Exception as e:
        st.error(f"Error fetching claims: {e}")
        return _empty_dataframe()

def get_customer_payments(customer_id: str) -> pd.DataFrame:
    """Fetch payment history for a customer."""

    customer_id = _normalize_customer_id(customer_id)

    if not customer_id:
        return _empty_dataframe()

    try:
        conn = get_db_connection()

        query = """
            SELECT *
            FROM PAYMENTS
            WHERE CUSTOMER_ID = ?
            ORDER BY PAYMENT_DATE DESC
        """

        return conn.query(
            query,
            params=(customer_id,),
            ttl=0
        )

    except Exception as e:
        st.error(f"Error fetching payments: {e}")
        return _empty_dataframe()

def get_customer_interactions(customer_id: str) -> pd.DataFrame:
    """Fetch customer interactions and transcripts."""

    customer_id = _normalize_customer_id(customer_id)

    if not customer_id:
        return _empty_dataframe()

    try:
        conn = get_db_connection()

        query = """
            SELECT *
            FROM INTERACTIONS
            WHERE CUSTOMER_ID = ?
            ORDER BY INTERACTION_DATE DESC
        """

        return conn.query(
            query,
            params=(customer_id,),
            ttl=0
        )

    except Exception as e:
        st.error(f"Error fetching interactions: {e}")
        return _empty_dataframe()

def get_ai_insights(customer_id: str) -> pd.DataFrame:
    """
    Fetch AI-generated customer insights.

    AI_INSIGHTS is not yet part of the active database pipeline,
    so missing-table/query errors are silently handled.
    """

    customer_id = _normalize_customer_id(customer_id)

    if not customer_id:
        return _empty_dataframe()

    try:
        conn = get_db_connection()

        query = """
            SELECT *
            FROM AI_INSIGHTS
            WHERE CUSTOMER_ID = ?
            ORDER BY GENERATED_AT DESC
        """

        return conn.query(
            query,
            params=(customer_id,),
            ttl=0
        )

    except Exception:
        return _empty_dataframe()

def get_next_best_actions(customer_id: str) -> pd.DataFrame:
    """Fetch stored Next Best Action recommendations."""

    customer_id = _normalize_customer_id(customer_id)

    if not customer_id:
        return _empty_dataframe()

    try:
        conn = get_db_connection()

        query = """
            SELECT *
            FROM NEXT_BEST_ACTIONS
            WHERE CUSTOMER_ID = ?
            ORDER BY GENERATED_AT DESC
        """

        return conn.query(
            query,
            params=(customer_id,),
            ttl=0
        )

    except Exception:
        return _empty_dataframe()

def get_customer_actions(customer_id: str) -> pd.DataFrame:
    """
    Fetch action history for a specific customer.
    """

    customer_id = _normalize_customer_id(customer_id)

    if not customer_id:
        return _empty_dataframe()

    try:
        conn = get_db_connection()

        query = """
            SELECT
                ACTION_ID,
                CUSTOMER_ID,
                EMPLOYEE_ID,
                ACTION_TYPE,
                ACTION_DETAILS,
                CREATED_AT,
                STATUS,
                COMPLETED_AT
            FROM ACTION_HISTORY
            WHERE CUSTOMER_ID = ?
            ORDER BY CREATED_AT DESC
        """

        return conn.query(
            query,
            params=(customer_id,),
            ttl=0
        )

    except Exception as e:
        st.error(f"Error fetching customer action history: {e}")
        return _empty_dataframe()


def get_all_action_history() -> pd.DataFrame:
    """
    Fetch all employee action history.
    """

    try:
        conn = get_db_connection()

        query = """
            SELECT
                ACTION_ID,
                CUSTOMER_ID,
                EMPLOYEE_ID,
                ACTION_TYPE,
                ACTION_DETAILS,
                CREATED_AT,
                STATUS,
                COMPLETED_AT
            FROM ACTION_HISTORY
            ORDER BY CREATED_AT DESC
        """

        return conn.query(
            query,
            ttl=0
        )

    except Exception as e:
        st.error(f"Error fetching action history: {e}")
        return _empty_dataframe()


def get_action_by_id(action_id: str) -> pd.DataFrame:
    """
    Fetch one action by ACTION_ID.
    """

    action_id = str(action_id).strip()

    if not action_id:
        return _empty_dataframe()

    try:
        conn = get_db_connection()

        query = """
            SELECT
                ACTION_ID,
                CUSTOMER_ID,
                EMPLOYEE_ID,
                ACTION_TYPE,
                ACTION_DETAILS,
                CREATED_AT,
                STATUS,
                COMPLETED_AT
            FROM ACTION_HISTORY
            WHERE ACTION_ID = ?
            LIMIT 1
        """

        return conn.query(
            query,
            params=(action_id,),
            ttl=0
        )

    except Exception as e:
        st.error(f"Error fetching action: {e}")
        return _empty_dataframe()


def create_action_history(
    action_id,
    customer_id,
    employee_id,
    action_type,
    action_details,
    status="OPEN",
):
    try:
        conn = get_db_connection()

        query = """
            INSERT INTO ACTION_HISTORY (
                ACTION_ID,
                CUSTOMER_ID,
                EMPLOYEE_ID,
                ACTION_TYPE,
                ACTION_DETAILS,
                CREATED_AT,
                STATUS,
                COMPLETED_AT
            )
            VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP(), ?, NULL)
        """

        
        session = conn.session()

        session.sql(
            query,
            params=[
                str(action_id),
                str(customer_id),
                str(employee_id),
                str(action_type),
                str(action_details),
                str(status),
            ],
        ).collect()

        return True

    except Exception as e:
        st.error(
            f"Snowflake error while creating action: "
            f"{type(e).__name__}: {e}"
        )
        return False


def update_action_status(
    action_id: str,
    status: str,
) -> bool:
    """
    Update action status directly through the Snowflake connector.
    """

    action_id = str(action_id).strip()
    status = str(status).strip().upper()

    if not action_id:
        st.error("Action ID is required.")
        return False

    allowed_statuses = {
        "OPEN",
        "IN_PROGRESS",
        "COMPLETED",
    }

    if status not in allowed_statuses:
        st.error(f"Invalid action status: {status}")
        return False

    try:
        conn = get_db_connection()

        if status == "COMPLETED":
            query = """
                UPDATE ACTION_HISTORY
                SET
                    STATUS = ?,
                    COMPLETED_AT = CURRENT_TIMESTAMP()
                WHERE ACTION_ID = ?
            """
        else:
            query = """
                UPDATE ACTION_HISTORY
                SET
                    STATUS = ?,
                    COMPLETED_AT = NULL
                WHERE ACTION_ID = ?
            """

        cursor = conn.cursor()

        cursor.execute(
            query,
            (
                status,
                action_id,
            )
        )

        cursor.close()

        return True

    except Exception as e:
        st.error(
            f"Snowflake error while updating action status: "
            f"{type(e).__name__}: {e}"
        )
        return False
        
def update_action_employee(
    action_id: str,
    employee_id: str,
) -> bool:
    """
    Assign/reassign an employee to an action.
    """

    action_id = str(action_id).strip()
    employee_id = str(employee_id).strip()

    if not action_id:
        st.error("Action ID is required.")
        return False

    if not employee_id:
        st.error("Employee ID is required.")
        return False

    try:
        conn = get_db_connection()

        query = """
            UPDATE ACTION_HISTORY
            SET EMPLOYEE_ID = ?
            WHERE ACTION_ID = ?
        """

        conn.query(
            query,
            params=(
                employee_id,
                action_id,
            ),
            ttl=0
        )

        return True

    except Exception as e:
        st.error(f"Error assigning employee: {e}")
        return False


def get_all_customers() -> pd.DataFrame:
    """Fetch all customers."""

    try:
        conn = get_db_connection()

        query = """
            SELECT *
            FROM CUSTOMERS
            ORDER BY CUSTOMER_ID
        """

        return conn.query(
            query,
            ttl=0
        )

    except Exception as e:
        st.error(f"Error fetching customers: {e}")
        return _empty_dataframe()


def get_all_interactions() -> pd.DataFrame:
    """Fetch all customer interactions."""

    try:
        conn = get_db_connection()

        query = """
            SELECT *
            FROM INTERACTIONS
            ORDER BY INTERACTION_DATE DESC
        """

        return conn.query(
            query,
            ttl=0
        )

    except Exception as e:
        st.error(f"Error fetching interactions: {e}")
        return _empty_dataframe()


def get_all_ai_insights() -> pd.DataFrame:
    """
    Fetch all AI insights.

    Returns an empty DataFrame until AI_INSIGHTS is available.
    """

    try:
        conn = get_db_connection()

        query = """
            SELECT *
            FROM AI_INSIGHTS
            ORDER BY GENERATED_AT DESC
        """

        return conn.query(
            query,
            ttl=0
        )

    except Exception:
        return _empty_dataframe()



def get_customer_360(customer_id: str) -> pd.DataFrame:
    """
    Fetch consolidated Customer 360 view.
    """

    customer_id = _normalize_customer_id(customer_id)

    if not customer_id:
        return _empty_dataframe()

    try:
        conn = get_db_connection()

        query = """
            SELECT *
            FROM CUSTOMER_360
            WHERE CUSTOMER_ID = ?
        """

        return conn.query(
            query,
            params=(customer_id,),
            ttl=0
        )

    except Exception as e:
        st.error(f"Error fetching Customer 360 data: {e}")
        return _empty_dataframe()


def get_table_count(table_name: str) -> int:
    """
    Return row count for a trusted Snowflake table.
    """

    allowed_tables = {
        "CUSTOMERS",
        "POLICIES",
        "CLAIMS",
        "PAYMENTS",
        "INTERACTIONS",
        "AI_INSIGHTS",
        "NEXT_BEST_ACTIONS",
        "ACTION_HISTORY",
        "USERS",
    }

    table_name = str(table_name).strip().upper()

    if table_name not in allowed_tables:
        return 0

    try:
        conn = get_db_connection()

        query = f"""
            SELECT COUNT(*) AS ROW_COUNT
            FROM {table_name}
        """

        df = conn.query(
            query,
            ttl=0
        )

        if df.empty:
            return 0

        return int(df.iloc[0]["ROW_COUNT"])

    except Exception:
        return 0


def get_system_health() -> dict:
    """
    Return live row counts for major Snowflake tables.
    """

    tables = [
        "CUSTOMERS",
        "POLICIES",
        "CLAIMS",
        "PAYMENTS",
        "INTERACTIONS",
        "AI_INSIGHTS",
        "NEXT_BEST_ACTIONS",
        "ACTION_HISTORY",
        "USERS",
    ]

    return {
        table: get_table_count(table)
        for table in tables
    }