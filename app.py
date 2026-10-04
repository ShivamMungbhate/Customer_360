# import streamlit as st


# from utils.session_management import init_session_state

# st.set_page_config(
#     page_title="Insurance Customer 360 & NBA Engine",
#     page_icon="🛡️",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )


# init_session_state()


# def render_sidebar():
#     """Render authenticated user's sidebar information and logout."""

#     with st.sidebar:
#         st.markdown("---")

#         user_email = st.session_state.get("user_email", "Unknown User")
#         role = str(
#             st.session_state.get("role", "CUSTOMER")
#         ).upper()

#         customer_id = st.session_state.get("customer_id")

#         st.markdown("### 👤 User")

#         st.write(f"**{user_email}**")

#         if role == "CUSTOMER":
#             st.caption("Role: CUSTOMER")

#             if customer_id:
#                 st.caption(f"Customer ID: `{customer_id}`")

#         elif role == "EMPLOYEE":
#             st.caption("Role: EMPLOYEE")

#         st.markdown("---")

#         if st.button(
#             "🚪 Log out",
#             use_container_width=True,
#             type="primary"
#         ):
#             st.session_state.clear()
#             init_session_state()
#             st.rerun()

# def get_navigation():
#     """
#     Build navigation based on authentication state and role.
#     """


#     if not st.session_state.get("logged_in", False):

#         return {
#             "Authentication": [
#                 st.Page(
#                     "pages/login.py",
#                     title="Sign In",
#                     icon="🔐",
#                     default=True
#                 )
#             ]
#         }


#     role = str(
#         st.session_state.get("role", "CUSTOMER")
#     ).upper()


#     if role == "CUSTOMER":

#         return {
#             "Customer Hub": [
#                 st.Page(
#                     "pages/customer_portal.py",
#                     title="Customer Portal",
#                     icon="👤",
#                     default=True
#                 ),

#                 st.Page(
#                     "pages/offers.py",
#                     title="Available Offers",
#                     icon="🎁"
#                 ),

#                 st.Page(
#                     "pages/ai_assistant.py",
#                     title="Ask AI Assistant",
#                     icon="🤖"
#                 ),

#                 st.Page(
#                     "pages/settings.py",
#                     title="Settings",
#                     icon="🛠️"
#                 ),
#             ]
#         }


#     elif role == "EMPLOYEE":

#         return {
#             "Employee Dashboard": [

#                 st.Page(
#                     "pages/employee_dashboard.py",
#                     title="Dashboard",
#                     icon="📊",
#                     default=True
#                 ),

#                 st.Page(
#                     "pages/customer_360.py",
#                     title="Customer 360 View",
#                     icon="🔍"
#                 ),

#                 st.Page(
#                     "pages/interactions.py",
#                     title="Interactions & Transcripts",
#                     icon="💬"
#                 ),

#                 st.Page(
#                     "pages/next_best_action.py",
#                     title="Next Best Actions",
#                     icon="⚡"
#                 ),

#                 st.Page(
#                     "pages/action_history.py",
#                     title="Action History",
#                     icon="📋"
#                 ),

#                 st.Page(
#                     "pages/ai_assistant.py",
#                     title="AI Assistant",
#                     icon="🤖"
#                 ),

#                 st.Page(
#                     "pages/analytics.py",
#                     title="Analytics & Trends",
#                     icon="📈"
#                 ),

#                 st.Page(
#                     "pages/system_health.py",
#                     title="System Health",
#                     icon="⚙️"
#                 ),

#                 st.Page(
#                     "pages/settings.py",
#                     title="Settings",
#                     icon="🛠️"
#                 ),
#             ]
#         }


#     else:

#         st.error(
#             "Invalid user role. Please sign in again."
#         )

#         st.session_state.clear()

#         init_session_state()

#         st.rerun()


# def main():

#     pages = get_navigation()

    
#     pg = st.navigation(pages)

#     if st.session_state.get("logged_in", False):
#         render_sidebar()

   
#     pg.run()


# if __name__ == "__main__":
#     main()
import streamlit as st


from utils.session_management import init_session_state


st.set_page_config(
    page_title="Insurance Customer 360 & NBA Engine",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# PREMIUM DARK UI STYLING
# ============================================================

st.markdown("""
<style>

/* ============================================================
   GLOBAL APP
   ============================================================ */

.stApp {
    background:
        radial-gradient(
            circle at 10% 0%,
            rgba(37, 99, 235, 0.12),
            transparent 35%
        ),
        radial-gradient(
            circle at 90% 10%,
            rgba(124, 58, 237, 0.10),
            transparent 35%
        ),
        #080d1a !important;

    color: #e5e7eb !important;
}


/* ============================================================
   TOP STREAMLIT HEADER
   ============================================================ */

header[data-testid="stHeader"] {
    background: #080d1a !important;
    border-bottom: 1px solid rgba(96, 165, 250, 0.10) !important;
}

header[data-testid="stHeader"] [data-testid="stToolbar"] {
    background: transparent !important;
}

header[data-testid="stHeader"] button {
    color: #94a3b8 !important;
}


/* ============================================================
   MAIN CONTENT AREA
   ============================================================ */

[data-testid="stMainBlockContainer"] {
    padding-top: 2rem;
    padding-bottom: 3rem;
}


/* ============================================================
   SIDEBAR
   ============================================================ */

section[data-testid="stSidebar"] {
    background:
        linear-gradient(
            180deg,
            #0a1220 0%,
            #0d1728 45%,
            #101827 100%
        ) !important;

    border-right: 1px solid rgba(96, 165, 250, 0.16) !important;

    box-shadow:
        8px 0 30px rgba(0, 0, 0, 0.18);
}


/* Sidebar main inner container */

section[data-testid="stSidebar"] > div {
    background: transparent !important;
}


/* Sidebar content */

section[data-testid="stSidebar"]
[data-testid="stSidebarContent"] {
    background: transparent !important;
}


/* ============================================================
   SIDEBAR TEXT
   ============================================================ */

section[data-testid="stSidebar"] p {
    color: #94a3b8 !important;
}

section[data-testid="stSidebar"] span {
    color: #94a3b8 !important;
}

section[data-testid="stSidebar"] label {
    color: #94a3b8 !important;
}


/* Sidebar headings */

section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
    color: #f8fafc !important;
    font-weight: 700 !important;
}


/* ============================================================
   NAVIGATION MENU
   ============================================================ */


/* Navigation links */

section[data-testid="stSidebar"] a {
    color: #94a3b8 !important;

    border-radius: 9px !important;

    transition:
        background 0.2s ease,
        color 0.2s ease,
        transform 0.2s ease;
}


/* Navigation hover */

section[data-testid="stSidebar"] a:hover {
    color: #ffffff !important;

    background:
        linear-gradient(
            90deg,
            rgba(59, 130, 246, 0.16),
            rgba(99, 102, 241, 0.10)
        ) !important;

    transform: translateX(2px);
}


/* Active navigation page */

section[data-testid="stSidebar"]
a[aria-current="page"] {

    color: #ffffff !important;

    background:
        linear-gradient(
            90deg,
            rgba(59, 130, 246, 0.28),
            rgba(99, 102, 241, 0.18)
        ) !important;

    border-left: 3px solid #60a5fa !important;

    box-shadow:
        inset 0 0 20px rgba(59, 130, 246, 0.05),
        0 4px 14px rgba(0, 0, 0, 0.12);
}


/* Active navigation text */

section[data-testid="stSidebar"]
a[aria-current="page"] span {
    color: #ffffff !important;
    font-weight: 600 !important;
}


/* ============================================================
   SIDEBAR DIVIDERS
   ============================================================ */

section[data-testid="stSidebar"] hr {
    border: none !important;

    border-top:
        1px solid rgba(148, 163, 184, 0.15) !important;

    margin-top: 16px !important;
    margin-bottom: 16px !important;
}


/* ============================================================
   USER SECTION
   ============================================================ */

section[data-testid="stSidebar"] strong {
    color: #e2e8f0 !important;
}


/* User email */

section[data-testid="stSidebar"] a[href^="mailto"] {
    color: #93c5fd !important;

    font-weight: 600 !important;

    text-decoration: none !important;
}


/* User email hover */

section[data-testid="stSidebar"] a[href^="mailto"]:hover {
    color: #bfdbfe !important;

    text-decoration: underline !important;
}


/* ============================================================
   LOGOUT BUTTON
   ============================================================ */

section[data-testid="stSidebar"] .stButton > button {

    width: 100% !important;

    background:
        linear-gradient(
            100deg,
            #4f46e5 0%,
            #6366f1 50%,
            #7c3aed 100%
        ) !important;

    color: #ffffff !important;

    border: 1px solid
        rgba(165, 180, 252, 0.25) !important;

    border-radius: 10px !important;

    min-height: 42px !important;

    font-weight: 600 !important;

    box-shadow:
        0 6px 20px rgba(79, 70, 229, 0.25) !important;

    transition:
        transform 0.2s ease,
        box-shadow 0.2s ease,
        background 0.2s ease !important;
}


/* Logout hover */

section[data-testid="stSidebar"]
.stButton > button:hover {

    background:
        linear-gradient(
            100deg,
            #6366f1 0%,
            #7c3aed 50%,
            #8b5cf6 100%
        ) !important;

    color: #ffffff !important;

    border-color:
        rgba(196, 181, 253, 0.5) !important;

    box-shadow:
        0 8px 25px rgba(99, 102, 241, 0.40) !important;

    transform: translateY(-2px);
}


/* ============================================================
   GENERAL BUTTONS
   ============================================================ */

.stButton > button {

    border-radius: 10px !important;

    font-weight: 600 !important;

    transition:
        transform 0.2s ease,
        box-shadow 0.2s ease !important;
}


.stButton > button:hover {
    transform: translateY(-1px);
}


/* ============================================================
   INPUTS
   ============================================================ */

.stTextInput input,
.stTextArea textarea {

    background: #111b2e !important;

    color: #f8fafc !important;

    border:
        1px solid #334155 !important;

    border-radius: 10px !important;
}


.stTextInput input:focus,
.stTextArea textarea:focus {

    border-color:
        #60a5fa !important;

    box-shadow:
        0 0 0 2px
        rgba(59, 130, 246, 0.15) !important;
}


.stTextInput input::placeholder,
.stTextArea textarea::placeholder {
    color: #64748b !important;
}


/* ============================================================
   SELECT BOX
   ============================================================ */

[data-baseweb="select"] > div {

    background: #111b2e !important;

    color: #e2e8f0 !important;

    border:
        1px solid #334155 !important;

    border-radius: 10px !important;
}


/* ============================================================
   EXPANDERS
   ============================================================ */

[data-testid="stExpander"] {

    background:
        rgba(15, 23, 42, 0.75) !important;

    border:
        1px solid rgba(71, 85, 105, 0.55) !important;

    border-radius: 12px !important;
}


[data-testid="stExpander"] summary {
    color: #e2e8f0 !important;

    font-weight: 600 !important;
}


/* ============================================================
   ALERTS
   ============================================================ */

[data-testid="stAlert"] {

    border-radius: 11px !important;

    border:
        1px solid rgba(148, 163, 184, 0.20) !important;
}


/* ============================================================
   CODE / CUSTOMER ID
   ============================================================ */

[data-testid="stCode"] {

    background: #0f1a2d !important;

    border:
        1px solid rgba(96, 165, 250, 0.20) !important;

    border-radius: 9px !important;
}


code {
    color: #93c5fd !important;
}


/* ============================================================
   SCROLLBAR
   ============================================================ */

::-webkit-scrollbar {
    width: 8px;
    height: 8px;
}


::-webkit-scrollbar-track {
    background: #080d1a;
}


::-webkit-scrollbar-thumb {

    background:
        linear-gradient(
            180deg,
            #334155,
            #475569
        );

    border-radius: 10px;
}


::-webkit-scrollbar-thumb:hover {
    background: #64748b;
}


/* ============================================================
   MOBILE
   ============================================================ */

@media (max-width: 768px) {

    [data-testid="stMainBlockContainer"] {
        padding-left: 1rem;
        padding-right: 1rem;
    }

    section[data-testid="stSidebar"] {
        border-right: none !important;
    }

}


/* ============================================================
   REDUCED MOTION
   ============================================================ */

@media (prefers-reduced-motion: reduce) {

    *,
    *::before,
    *::after {
        transition: none !important;
        animation: none !important;
    }

}

</style>
""", unsafe_allow_html=True)


# ============================================================
# SESSION STATE
# ============================================================

init_session_state()


def render_sidebar():
    """Render authenticated user's sidebar information and logout."""

    with st.sidebar:
        st.markdown("---")

        user_email = st.session_state.get(
            "user_email",
            "Unknown User"
        )

        role = str(
            st.session_state.get(
                "role",
                "CUSTOMER"
            )
        ).upper()

        customer_id = st.session_state.get(
            "customer_id"
        )

        st.markdown("### 👤 User")

        st.write(f"**{user_email}**")

        if role == "CUSTOMER":

            st.caption("Role: CUSTOMER")

            if customer_id:
                st.caption(
                    f"Customer ID: `{customer_id}`"
                )

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

    if not st.session_state.get(
        "logged_in",
        False
    ):

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
        st.session_state.get(
            "role",
            "CUSTOMER"
        )
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

    if st.session_state.get(
        "logged_in",
        False
    ):

        render_sidebar()

    pg.run()


if __name__ == "__main__":
    main()