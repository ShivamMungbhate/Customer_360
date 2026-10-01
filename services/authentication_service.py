import streamlit as st


def get_db_connection():
    return st.connection("snowflake", type="snowflake")


def authenticate_user(email: str, password: str, selected_role: str):
    """
    Authenticate a user directly against the Snowflake USERS table.

    Expected USERS columns:
        USER_ID
        EMAIL
        ROLE
        CUSTOMER_ID
        STATUS
        PASSWORD_HASH

    For the current demo, PASSWORD_HASH contains the plain demo password.
    """

    clean_email = email.strip().lower()
    clean_password = password.strip()
    clean_role = selected_role.strip().upper()

    if not clean_email or "@" not in clean_email:
        return None, "Please enter a valid email address."

    if not clean_password:
        return None, "Please enter your password."

    conn = get_db_connection()

    try:
        users = conn.query(
            """
            SELECT
                USER_ID,
                EMAIL,
                ROLE,
                CUSTOMER_ID,
                STATUS,
                PASSWORD_HASH
            FROM USERS
            WHERE LOWER(EMAIL) = ?
            LIMIT 1
            """,
            params=(clean_email,),
            ttl=0
        )

    except Exception as e:
        return None, f"Unable to connect to the authentication database: {e}"

    if users.empty:
        return None, "Invalid email or password."

    user = users.iloc[0]

    
    db_email = str(user["EMAIL"]).strip().lower()
    db_role = str(user["ROLE"]).strip().upper()
    db_status = str(user["STATUS"]).strip().upper()

    db_password = user["PASSWORD_HASH"]

    if db_password is None:
        return None, "This account does not have a password configured."

    db_password = str(db_password)

    
    if db_status != "ACTIVE":
        return None, "This account is not active. Please contact an administrator."

    
    if db_role != clean_role:
        return (
            None,
            f"Access Denied: This email is registered as {db_role}, "
            f"not {clean_role}."
        )

   
    if db_password != clean_password:
        return None, "Incorrect password. Please try again."

    
    user_record = {
        "user_id": str(user["USER_ID"]),
        "email": db_email,
        "role": db_role,
        "customer_id": (
            None
            if user["CUSTOMER_ID"] is None
            else str(user["CUSTOMER_ID"])
        ),
        "status": db_status,
    }

    return user_record, None