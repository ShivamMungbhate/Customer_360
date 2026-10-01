import streamlit as st

from utils.session_management import init_session_state

st.set_page_config(
    page_title="Insurance Customer 360 & NBA Engine",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)
init_session_state()


def render_sidebar():
    """Render authenticated user's sidebar information and logout."""

    with st.sidebar:
        st.markdown("---")

        user_email = st.session_state.get("user_email", "Unknown User")
        role = str(
            st.session_state.get("role", "CUSTOMER")
        ).upper()

        customer_id = st.session_state.get("customer_id")

        st.markdown("### 👤 User")

        st.write(f"**{user_email}**")

        if role == "CUSTOMER":
            st.caption("Role: CUSTOMER")

            if customer_id:
                st.caption(f"Customer ID: `{customer_id}`")

        elif role == "EMPLOYEE":
            st.caption("Role: EMPLOYEE")

        st.markdown("---")

        if st.button(
            "🚪 Log out",
            use_container_width=True,
            type="primary"
        ):
            st.session_state.clear()
            init_session_state()
            st.rerun()

def get_navigation():
    """
    Build navigation based on authentication state and role.
    """


    if not st.session_state.get("logged_in", False):

        return {
            "Authentication": [
                st.Page(
                    "pages/login.py",
                    title="Sign In",
                    icon="🔐",
                    default=True
                )
            ]
        }


    role = str(
        st.session_state.get("role", "CUSTOMER")
    ).upper()


    if role == "CUSTOMER":

        return {
            "Customer Hub": [
                st.Page(
                    "pages/customer_portal.py",
                    title="Customer Portal",
                    icon="👤",
                    default=True
                ),

                st.Page(
                    "pages/offers.py",
                    title="Available Offers",
                    icon="🎁"
                ),

                st.Page(
                    "pages/ai_assistant.py",
                    title="Ask AI Assistant",
                    icon="🤖"
                ),

                st.Page(
                    "pages/settings.py",
                    title="Settings",
                    icon="🛠️"
                ),
            ]
        }


    elif role == "EMPLOYEE":

        return {
            "Employee Dashboard": [

                st.Page(
                    "pages/employee_dashboard.py",
                    title="Dashboard",
                    icon="📊",
                    default=True
                ),

                st.Page(
                    "pages/customer_360.py",
                    title="Customer 360 View",
                    icon="🔍"
                ),

                st.Page(
                    "pages/interactions.py",
                    title="Interactions & Transcripts",
                    icon="💬"
                ),

                st.Page(
                    "pages/next_best_action.py",
                    title="Next Best Actions",
                    icon="⚡"
                ),

                st.Page(
                    "pages/action_history.py",
                    title="Action History",
                    icon="📋"
                ),

                st.Page(
                    "pages/ai_assistant.py",
                    title="AI Assistant",
                    icon="🤖"
                ),

                st.Page(
                    "pages/analytics.py",
                    title="Analytics & Trends",
                    icon="📈"
                ),

                st.Page(
                    "pages/system_health.py",
                    title="System Health",
                    icon="⚙️"
                ),

                st.Page(
                    "pages/settings.py",
                    title="Settings",
                    icon="🛠️"
                ),
            ]
        }


    else:

        st.error(
            "Invalid user role. Please sign in again."
        )

        st.session_state.clear()

        init_session_state()

        st.rerun()


def main():

    pages = get_navigation()

    
    pg = st.navigation(pages)

    if st.session_state.get("logged_in", False):
        render_sidebar()

   
    pg.run()


if __name__ == "__main__":
    main()