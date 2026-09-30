import json
import os


DB_FILE = "users_db.json"

def _load_users():
    """Loads users from the local JSON database file if it exists."""
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r") as f:
                return json.load(f)
        except Exception:
            pass
            
    # Default
    default_users = {
        "employee@insurance.com": {"password": "demo123", "user_id": "EMP-01", "role": "EMPLOYEE", "customer_id": None},
        "priya@insurance.com": {"password": "demo123", "user_id": "EMP-02", "role": "EMPLOYEE", "customer_id": None},
        "customer@insurance.com": {"password": "demo123", "user_id": "USR-01", "role": "CUSTOMER", "customer_id": "CUST-1001"},
        "rahul@insurance.com": {"password": "demo123", "user_id": "USR-02", "role": "CUSTOMER", "customer_id": "CUST-1001"},
        "ananya@insurance.com": {"password": "demo123", "user_id": "USR-03", "role": "CUSTOMER", "customer_id": "CUST-1045"}
    }
    _save_users(default_users)
    return default_users

def _save_users(users_dict):
    """Saves the updated users dictionary to the local JSON file."""
    try:
        with open(DB_FILE, "w") as f:
            json.dump(users_dict, f, indent=4)
    except Exception as e:
        print(f"Error saving users DB: {e}")

def authenticate_user(email: str, password: str, selected_role: str):
    """
    Persistently registers new emails with their chosen password, 
    and validates existing user passwords against stored records.
    """
    clean_email = email.strip().lower()
    
    if not clean_email or "@" not in clean_email:
        return None, "Please enter a valid email address."
        
    users = _load_users()
    
    # If email is completely new, auto-register it and save the password they typed!
    if clean_email not in users:
        new_user_id = f"AUTO-{len(users) + 100}"
        new_cust_id = f"CUST-{len(users) + 2000}" if selected_role == "CUSTOMER" else None
        
        users[clean_email] = {
            "password": password,  # Saves their chosen password
            "user_id": new_user_id,
            "role": selected_role,
            "customer_id": new_cust_id
        }
        _save_users(users)
        return users[clean_email], None
        
    user_record = users[clean_email]
    
    
    if user_record["role"] != selected_role:
        return None, f"Access Denied: This email is already registered as a {user_record['role']}, not a {selected_role}."
        
    # Verify the password 
    if user_record.get("password") == password:
        return user_record, None
    else:
        return None, "Incorrect password. Please enter the password you used when registering."