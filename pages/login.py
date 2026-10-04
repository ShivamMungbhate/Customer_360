
import streamlit as st
from services.authentication_service import authenticate_user


st.markdown("""
<style>

    /* =====================================================
       GLOBAL PAGE
       ===================================================== */

    html, body, [data-testid="stAppViewContainer"] {
        background:
            radial-gradient(
                circle at 50% 0%,
                rgba(37, 99, 235, 0.16),
                transparent 32%
            ),
            radial-gradient(
                circle at 10% 80%,
                rgba(20, 184, 166, 0.08),
                transparent 28%
            ),
            radial-gradient(
                circle at 90% 70%,
                rgba(6, 182, 212, 0.06),
                transparent 25%
            ),
            #07111f !important;
    }

    [data-testid="stAppViewContainer"] {
        color: #e5edf7 !important;
    }

    [data-testid="stHeader"] {
        background: transparent !important;
    }

    [data-testid="stToolbar"] {
        background: transparent !important;
    }


    /* =====================================================
       MAIN CONTENT
       ===================================================== */

    .block-container {
        max-width: 1100px !important;

        padding-top: 2rem !important;
        padding-bottom: 4rem !important;

        padding-left: 1.5rem !important;
        padding-right: 1.5rem !important;
    }


    /* =====================================================
       MAIN BRAND TITLE
       ===================================================== */

    h1 {
        font-size: 2.55rem !important;

        font-weight: 800 !important;

        letter-spacing: -0.04em !important;

        margin-bottom: 0.35rem !important;

        background:
            linear-gradient(
                90deg,
                #ffffff 0%,
                #dbeafe 40%,
                #67e8f9 100%
            );

        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;

        text-shadow:
            0 0 30px rgba(103, 232, 249, 0.08);
    }


    /* =====================================================
       SUBTITLE
       ===================================================== */

    .block-container > div > div > div p {
        color: #8fa4bb !important;
        font-size: 0.98rem !important;
        letter-spacing: 0.02em;
    }


    /* =====================================================
       LOGIN CARD
       ===================================================== */

    [data-testid="stVerticalBlockBorderWrapper"] {
        background:
            linear-gradient(
                145deg,
                rgba(15, 31, 52, 0.96),
                rgba(7, 20, 35, 0.98)
            ) !important;

        border:
            1px solid rgba(71, 102, 138, 0.38) !important;

        border-radius: 22px !important;

        padding: 12px !important;

        box-shadow:
            0 25px 70px rgba(0, 0, 0, 0.38),
            0 0 40px rgba(20, 184, 166, 0.035),
            inset 0 1px 0 rgba(255, 255, 255, 0.045) !important;

        backdrop-filter: blur(16px);

        transition:
            border-color 0.25s ease,
            box-shadow 0.25s ease !important;
    }

    [data-testid="stVerticalBlockBorderWrapper"]:hover {
        border-color:
            rgba(45, 212, 191, 0.48) !important;

        box-shadow:
            0 28px 75px rgba(0, 0, 0, 0.44),
            0 0 35px rgba(20, 184, 166, 0.08),
            inset 0 1px 0 rgba(255, 255, 255, 0.05) !important;
    }


    /* =====================================================
       LOGIN HEADING
       ===================================================== */

    h2, h3 {
        color: #f8fafc !important;

        font-weight: 750 !important;

        letter-spacing: -0.02em !important;
    }

    h3 {
        font-size: 1.35rem !important;

        margin-bottom: 1.2rem !important;
    }


    /* =====================================================
       LABELS
       ===================================================== */

    label {
        color: #aebed0 !important;

        font-size: 0.88rem !important;

        font-weight: 600 !important;
    }


    /* =====================================================
       RADIO BUTTON
       ===================================================== */

    [data-testid="stRadio"] {
        background:
            rgba(8, 22, 38, 0.70) !important;

        border:
            1px solid rgba(71, 102, 138, 0.28) !important;

        border-radius: 12px !important;

        padding: 10px 14px !important;

        margin-bottom: 15px !important;
    }

    [data-testid="stRadio"] label {
        color: #cbd8e6 !important;
    }

    [data-testid="stRadio"] label:hover {
        color: #67e8f9 !important;
    }


    /* =====================================================
       TEXT INPUTS
       ===================================================== */

    div[data-baseweb="input"] {
        background:
            rgba(8, 22, 38, 0.92) !important;

        border:
            1px solid rgba(71, 102, 138, 0.42) !important;

        border-radius: 11px !important;

        min-height: 46px !important;

        transition:
            border-color 0.2s ease,
            box-shadow 0.2s ease,
            background 0.2s ease !important;
    }

    div[data-baseweb="input"]:focus-within {
        background:
            rgba(9, 28, 45, 0.98) !important;

        border-color:
            rgba(45, 212, 191, 0.78) !important;

        box-shadow:
            0 0 0 2px rgba(20, 184, 166, 0.10),
            0 0 20px rgba(20, 184, 166, 0.05) !important;
    }

    div[data-baseweb="input"] input {
        color: #edf6ff !important;

        background: transparent !important;

        font-size: 0.95rem !important;
    }

    div[data-baseweb="input"] input::placeholder {
        color: #53677d !important;
    }


    /* =====================================================
       SIGN IN BUTTON
       ===================================================== */

    [data-testid="stFormSubmitButton"] button {
        width: 100% !important;

        min-height: 47px !important;

        margin-top: 8px !important;

        background:
            linear-gradient(
                135deg,
                #0f766e 0%,
                #0891b2 100%
            ) !important;

        color: #ffffff !important;

        border:
            1px solid rgba(103, 232, 249, 0.22) !important;

        border-radius: 11px !important;

        font-size: 0.96rem !important;

        font-weight: 750 !important;

        letter-spacing: 0.01em !important;

        box-shadow:
            0 8px 22px rgba(8, 145, 178, 0.20) !important;

        transition:
            transform 0.18s ease,
            box-shadow 0.18s ease,
            filter 0.18s ease !important;
    }

    [data-testid="stFormSubmitButton"] button:hover {
        filter: brightness(1.10) !important;

        transform: translateY(-2px) !important;

        box-shadow:
            0 13px 30px rgba(8, 145, 178, 0.32) !important;
    }

    [data-testid="stFormSubmitButton"] button:active {
        transform: translateY(0) !important;
    }


    /* =====================================================
       DEMO LOGIN EXPANDER
       ===================================================== */

    [data-testid="stExpander"] {
        background:
            rgba(8, 22, 38, 0.78) !important;

        border:
            1px solid rgba(71, 102, 138, 0.30) !important;

        border-radius: 13px !important;

        margin-top: 18px !important;

        overflow: hidden !important;

        transition:
            border-color 0.2s ease,
            background 0.2s ease !important;
    }

    [data-testid="stExpander"]:hover {
        border-color:
            rgba(45, 212, 191, 0.42) !important;

        background:
            rgba(10, 28, 47, 0.90) !important;
    }

    [data-testid="stExpander"] summary {
        color: #dce8f5 !important;

        font-weight: 650 !important;
    }

    [data-testid="stExpander"] p {
        color: #9fb1c4 !important;
    }

    [data-testid="stExpander"] strong {
        color: #e8f1fb !important;
    }

    [data-testid="stExpander"] code {
        color: #67e8f9 !important;

        background:
            rgba(8, 47, 73, 0.65) !important;

        border:
            1px solid rgba(34, 211, 238, 0.16) !important;

        border-radius: 6px !important;

        padding: 3px 7px !important;
    }


    /* =====================================================
       ALERTS
       ===================================================== */

    [data-testid="stAlert"] {
        border-radius: 11px !important;

        border:
            1px solid rgba(71, 102, 138, 0.35) !important;

        background:
            rgba(10, 28, 47, 0.92) !important;
    }

    [data-testid="stAlert"] p {
        color: #dce8f5 !important;
    }


    /* =====================================================
       FORM CONTAINER
       ===================================================== */

    [data-testid="stForm"] {
        border: none !important;

        background: transparent !important;
    }


    /* =====================================================
       SPACING
       ===================================================== */

    [data-testid="stForm"] > div {
        gap: 0.65rem !important;
    }


    /* =====================================================
       SIDEBAR HIDDEN / CLEAN LOGIN
       ===================================================== */

    [data-testid="stSidebar"] {
        display: none !important;
    }


    /* =====================================================
       SCROLLBAR
       ===================================================== */

    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }

    ::-webkit-scrollbar-track {
        background: #07111f;
    }

    ::-webkit-scrollbar-thumb {
        background: #263b52;
        border-radius: 999px;
    }

    ::-webkit-scrollbar-thumb:hover {
        background: #36536f;
    }


    /* =====================================================
       RESPONSIVE
       ===================================================== */

    @media (max-width: 900px) {

        .block-container {
            padding-left: 1rem !important;
            padding-right: 1rem !important;
        }

        h1 {
            font-size: 1.9rem !important;
        }

        [data-testid="stVerticalBlockBorderWrapper"] {
            border-radius: 17px !important;
        }
    }

</style>
""", unsafe_allow_html=True)


st.markdown("<br><br>", unsafe_allow_html=True)

st.markdown(
    "<h1 style='text-align: center;'>🛡️ Enterprise Insurance Hub</h1>",
    unsafe_allow_html=True
)

st.markdown(
    "<p style='text-align: center; color: gray;'>"
    "Customer 360 & Next Best Action Engine"
    "</p>",
    unsafe_allow_html=True
)

st.markdown("<br>", unsafe_allow_html=True)


col1, col2, col3 = st.columns([1, 1.2, 1])

with col2:

    with st.container(border=True):

        st.subheader("Secure Sign In")

        login_role = st.radio(
            "I am logging in as:",
            ["CUSTOMER", "EMPLOYEE"],
            horizontal=True
        )

        with st.form("login_form"):

            email = st.text_input(
                "Email Address",
                placeholder="Enter your registered email"
            )

            password = st.text_input(
                "Password",
                type="password",
                placeholder="Enter password"
            )

            submit = st.form_submit_button(
                "Sign In",
                use_container_width=True
            )

            if submit:

                if not email.strip() or not password:

                    st.error(
                        "Please enter both email and password."
                    )

                else:

                    user, error_msg = authenticate_user(
                        email.strip(),
                        password,
                        login_role
                    )

                    if user:

                        st.session_state["logged_in"] = True
                        st.session_state["user_id"] = user["user_id"]
                        st.session_state["user_email"] = user["email"]
                        st.session_state["role"] = user["role"]
                        st.session_state["customer_id"] = user["customer_id"]

                        st.success(
                            "Authentication successful! Redirecting..."
                        )

                        st.rerun()

                    else:

                        st.error(error_msg)

        with st.expander("💡 Demo Login Information"):

            st.markdown("""
            ### Demo Password

            **Password for all existing users:** `1234`

            ### Employee Users

            - `employee1@customer360.demo`
            - `employee2@customer360.demo`

            ### Customer Users

            - `rahul@customer360.demo`
            - `priya@customer360.demo`
            - `amit@customer360.demo`

            Only users already present in the Snowflake `USERS` table
            can sign in. New accounts are not automatically created.
            """)
