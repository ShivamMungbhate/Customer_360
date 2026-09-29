def authenticate_user(email: str, password: str):
    
    if email == "employee@insurance.com" and password == "demo123":
        return {"user_id": "EMP-01", "email": email, "role": "EMPLOYEE", "customer_id": None}
    elif email == "customer@insurance.com" and password == "demo123":
        return {"user_id": "USR-02", "email": email, "role": "CUSTOMER", "customer_id": "CUST-1001"}
    return None