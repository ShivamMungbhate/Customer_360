import streamlit as st
from services.authentication_service import authenticate_user

st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("<h1 style='text-align: center;'>🛡️ Enterprise Insurance Hub</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: gray;'>Customer 360 & Next Best Action Engine</p>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 1.2, 1])

with col2:
    with st.container(border=True):
        st.subheader("Secure Sign In")
        
       
        login_role = st.radio("I am logging in as a:", ["CUSTOMER", "EMPLOYEE"], horizontal=True)

        with st.form("login_form"):
           
            email = st.text_input("Email Address", placeholder="Enter any email...")
            password = st.text_input("Password", type="password", placeholder="Enter password")
            submit = st.form_submit_button("Sign In", use_container_width=True)

            if submit:
                if not email or not password:
                    st.error("Please enter both email and password.")
                else:
                   
                    user, error_msg = authenticate_user(email, password, login_role)
                    if user:
                        st.session_state["logged_in"] = True
                        st.session_state["user_id"] = user["user_id"]
                        st.session_state["user_email"] = email.strip().lower()
                        st.session_state["role"] = user["role"]
                        st.session_state["customer_id"] = user["customer_id"]
                        
                        st.success("Authentication successful! Redirecting...")
                        st.rerun()
                    else:
                        st.error(error_msg)

        with st.expander("💡 Demo & Auto-Registration Info"):
            st.markdown("""
            * **New Emails:** Type *any* email address on your PC, and it will instantly auto-register!
            * **Pre-set Employee:** `priya@insurance.com` (Role: EMPLOYEE)
            * **Pre-set Customer:** `rahul@insurance.com` (Role: CUSTOMER)
            """)