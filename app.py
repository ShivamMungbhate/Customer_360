import streamlit as st
from utils.session_management import init_session_state

st.set_page_config(
    page_title="Insurance Customer 360 & NBA Engine",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state variables
init_session_state()

def main():
    # Define pages based on authentication state and role
    if not st.session_state.get("logged_in", False):
        # When logged out, ONLY show the login page
        pages = {
            "Authentication": [
                st.Page("pages/login.py", title="Sign In", icon="🔐", default=True)
            ]
        }
    else:
        role = st.session_state.get("role", "CUSTOMER")
        
        if role == "CUSTOMER":
            pages = {
                "Customer Hub": [
                    st.Page("pages/customer_portal.py", title="Customer Portal", icon="👤", default=True),
                    st.Page("pages/ai_assistant.py", title="Ask AI Assistant", icon="🤖"),
                ]
            }
        else:  # EMPLOYEE (Unified into a single, clean dictionary block)
            pages = {
                "Employee Dashboard": [
                    st.Page("pages/employee_dashboard.py", title="Dashboard", icon="📊", default=True),
                    st.Page("pages/customer_360.py", title="Customer 360 View", icon="🔍"),
                    st.Page("pages/interactions.py", title="Interactions & Transcripts", icon="💬"),
                    st.Page("pages/next_best_action.py", title="Next Best Actions", icon="⚡"),
                    st.Page("pages/action_history.py", title="Action History", icon="📋"),
                    st.Page("pages/ai_assistant.py", title="AI Assistant", icon="🤖"),
                    st.Page("pages/analytics.py", title="Analytics & Trends", icon="📈"),
                    st.Page("pages/system_health.py", title="System Health", icon="⚙️"),
                    st.Page("pages/settings.py", title="Settings", icon="🛠️"),
                ]
            }

    # Run navigation
    pg = st.navigation(pages)

    # Render a clean sidebar footer with user details and Log out button ONLY if logged in
    if st.session_state.get("logged_in", False):
        with st.sidebar:
            st.markdown("---")
            st.write(f"👤 **{st.session_state.get('user_email')}**")
            st.caption(f"Role: **{st.session_state.get('role')}**")
            
            if st.button("🚪 Log out", use_container_width=True, type="primary"):
                # Clear all session state variables to return to login state
                st.session_state.clear()
                st.rerun()

    pg.run()

if __name__ == "__main__":
    main()