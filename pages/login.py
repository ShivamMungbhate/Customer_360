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
        
        # Demo Role Switcher
        demo_role = st.selectbox("Select Demo Role", ["EMPLOYEE", "CUSTOMER"])
        
        default_email = "employee@insurance.com" if demo_role == "EMPLOYEE" else "customer@insurance.com"

        with st.form("login_form"):
            email = st.text_input("Email Address", value=default_email)
            password = st.text_input("Password", type="password", value="demo123")
            submit = st.form_submit_button("Sign In", use_container_width=True)

            if submit:
                user = authenticate_user(email, password)
                if user:
                    st.session_state["logged_in"] = True
                    st.session_state["user_id"] = user["user_id"]
                    st.session_state["user_email"] = email
                    st.session_state["role"] = demo_role
                    st.session_state["customer_id"] = "CUST-1001" if demo_role == "CUSTOMER" else None
                    
                    st.success("Login successful!")
                    st.rerun()
                else:
                    st.error("Invalid credentials. Try demo credentials.")