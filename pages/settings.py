
import streamlit as st

from utils.security import enforce_employee_boundary

st.markdown(
    """
    <style>

    /* =====================================================
       GLOBAL PAGE
       ===================================================== */

    .stApp {
        background:
            radial-gradient(
                circle at 85% 5%,
                rgba(37, 99, 235, 0.12),
                transparent 28%
            ),
            radial-gradient(
                circle at 10% 20%,
                rgba(20, 184, 166, 0.08),
                transparent 25%
            ),
            #07111f;

        color: #e5edf7;
    }

    .block-container {
        max-width: 1450px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }


    /* =====================================================
       HEADINGS
       ===================================================== */

    h1,
    h2,
    h3,
    h4 {
        color: #f8fafc !important;
        letter-spacing: -0.02em;
    }

    h1 {
        font-size: 2.15rem !important;
        font-weight: 750 !important;
    }

    h2,
    h3 {
        font-weight: 700 !important;
    }

    p,
    label,
    .stCaption {
        color: #aebed0 !important;
    }


    /* =====================================================
       TABS
       ===================================================== */

    button[data-baseweb="tab"] {
        color: #8fa4bb !important;
        font-weight: 650 !important;
        font-size: 0.95rem !important;
    }

    button[data-baseweb="tab"]:hover {
        color: #67e8f9 !important;
    }

    button[data-baseweb="tab"][aria-selected="true"] {
        color: #67e8f9 !important;
    }

    div[data-baseweb="tab-highlight"] {
        background-color: #14b8a6 !important;
        height: 3px !important;
    }


    /* =====================================================
       CONTAINERS / CARDS
       ===================================================== */

    div[data-testid="stVerticalBlockBorderWrapper"] {
        background:
            linear-gradient(
                145deg,
                rgba(15, 31, 52, 0.94),
                rgba(8, 22, 38, 0.94)
            );

        border: 1px solid
            rgba(71, 102, 138, 0.30) !important;

        border-radius: 16px !important;

        box-shadow:
            0 10px 28px rgba(0, 0, 0, 0.20);

        padding: 5px;
        margin-bottom: 14px;

        transition:
            border-color 0.18s ease,
            transform 0.18s ease,
            box-shadow 0.18s ease;
    }

    div[data-testid="stVerticalBlockBorderWrapper"]:hover {
        border-color:
            rgba(45, 212, 191, 0.38) !important;

        box-shadow:
            0 14px 35px rgba(0, 0, 0, 0.28),
            0 0 20px rgba(20, 184, 166, 0.05);

        transform: translateY(-1px);
    }


    /* =====================================================
       METRIC CARDS
       ===================================================== */

    [data-testid="stMetric"] {
        background:
            linear-gradient(
                145deg,
                rgba(15, 31, 52, 0.95),
                rgba(9, 23, 40, 0.92)
            );

        border: 1px solid
            rgba(71, 102, 138, 0.30);

        border-radius: 16px;

        padding: 18px 20px;

        min-height: 105px;

        box-shadow:
            0 10px 30px rgba(0, 0, 0, 0.22),
            inset 0 1px 0
            rgba(255, 255, 255, 0.035);

        transition:
            transform 0.18s ease,
            border-color 0.18s ease,
            box-shadow 0.18s ease;
    }

    [data-testid="stMetric"]:hover {
        transform: translateY(-3px);

        border-color:
            rgba(45, 212, 191, 0.55);

        box-shadow:
            0 14px 35px rgba(0, 0, 0, 0.30),
            0 0 20px rgba(20, 184, 166, 0.08);
    }

    [data-testid="stMetricLabel"] {
        color: #8fa4bb !important;
        font-size: 0.82rem !important;
        font-weight: 600 !important;
    }

    [data-testid="stMetricValue"] {
        color: #f8fafc !important;
        font-size: 1.65rem !important;
        font-weight: 750 !important;
    }


    /* =====================================================
       INPUTS
       ===================================================== */

    div[data-baseweb="input"] {
        background:
            rgba(11, 27, 45, 0.92) !important;

        border: 1px solid
            rgba(71, 102, 138, 0.42) !important;

        border-radius: 10px !important;

        transition:
            border-color 0.18s ease,
            box-shadow 0.18s ease;
    }

    div[data-baseweb="input"]:focus-within {
        border-color:
            rgba(45, 212, 191, 0.75) !important;

        box-shadow:
            0 0 0 2px
            rgba(20, 184, 166, 0.10) !important;
    }

    div[data-baseweb="input"] input {
        color: #e5edf7 !important;
    }

    div[data-baseweb="input"] input::placeholder {
        color: #64748b !important;
    }


    /* =====================================================
       SELECTBOX
       ===================================================== */

    div[data-baseweb="select"] > div {
        background:
            rgba(11, 27, 45, 0.92) !important;

        border-color:
            rgba(71, 102, 138, 0.42) !important;

        border-radius: 10px !important;
    }

    div[data-baseweb="select"] span {
        color: #dbeafe !important;
    }


    /* =====================================================
       RADIO BUTTONS
       ===================================================== */

    div[data-testid="stRadio"] label {
        color: #cbd5e1 !important;
    }

    div[data-testid="stRadio"] label:hover {
        color: #67e8f9 !important;
    }


    /* =====================================================
       CHECKBOX
       ===================================================== */

    div[data-testid="stCheckbox"] label {
        color: #cbd5e1 !important;
    }

    div[data-testid="stCheckbox"] label:hover {
        color: #67e8f9 !important;
    }


    /* =====================================================
       BUTTONS
       ===================================================== */

    .stButton > button {
        background:
            linear-gradient(
                135deg,
                #0f766e,
                #0891b2
            ) !important;

        color: #ffffff !important;

        border: 1px solid
            rgba(103, 232, 249, 0.20) !important;

        border-radius: 9px !important;

        font-weight: 650 !important;

        min-height: 42px;

        box-shadow:
            0 7px 18px
            rgba(8, 145, 178, 0.16);

        transition:
            transform 0.18s ease,
            box-shadow 0.18s ease,
            filter 0.18s ease;
    }

    .stButton > button:hover {
        filter: brightness(1.08);

        transform: translateY(-1px);

        box-shadow:
            0 10px 24px
            rgba(8, 145, 178, 0.25);
    }

    .stButton > button:active {
        transform: translateY(0);
    }


    /* =====================================================
       PRIMARY BUTTON
       ===================================================== */

    button[kind="primary"] {
        background:
            linear-gradient(
                135deg,
                #0f766e,
                #0891b2
            ) !important;

        color: #ffffff !important;

        border: none !important;
    }


    /* =====================================================
       ALERTS
       ===================================================== */

    div[data-testid="stAlert"] {
        border-radius: 12px !important;

        border: 1px solid
            rgba(71, 102, 138, 0.30) !important;

        background:
            rgba(12, 29, 48, 0.90) !important;
    }

    div[data-testid="stAlert"] p {
        color: #d8e5f2 !important;
    }


    /* =====================================================
       DIVIDERS
       ===================================================== */

    hr {
        border: none !important;

        height: 1px !important;

        background:
            linear-gradient(
                90deg,
                transparent,
                rgba(71, 102, 138, 0.55),
                transparent
            ) !important;

        margin: 28px 0 !important;
    }


    /* =====================================================
       CODE BLOCK
       ===================================================== */

    code {
        color: #67e8f9 !important;

        background:
            rgba(8, 47, 73, 0.55) !important;

        border: 1px solid
            rgba(34, 211, 238, 0.15);

        border-radius: 6px;

        padding: 2px 7px;
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
            padding-left: 1rem;
            padding-right: 1rem;
        }

        h1 {
            font-size: 1.75rem !important;
        }

    }

    </style>
    """,
    unsafe_allow_html=True,
)


st.title("⚙️ Application Settings & Preferences")

st.caption(
    "Manage your application preferences and review "
    "your current access scope."
)


role = str(
    st.session_state.get(
        "role",
        "CUSTOMER"
    )
).upper()


tab1, tab2, tab3, tab4 = st.tabs(
    [
        "👤 Profile",
        "🔔 Notifications",
        "🔒 Security & Access",
        "🎨 Display",
    ]
)

with tab1:

    st.subheader("User Profile")

    current_email = st.session_state.get(
        "user_email",
        "user@insurance.com"
    )

    default_display = st.session_state.get(
        "display_name"
    )

    if not default_display:

        default_display = (
            current_email
            .split("@")[0]
            .capitalize()
        )

    new_display_name = st.text_input(
        "Display Name",
        value=default_display,
        help=(
            "This name is used for display purposes "
            "inside the application."
        ),
    )

    if st.button(
        "Update Display Name",
        type="primary",
    ):

        cleaned_name = (
            new_display_name
            .strip()
        )

        if cleaned_name:

            st.session_state[
                "display_name"
            ] = cleaned_name

            st.success(
                f"Display name updated to **{cleaned_name}**."
            )

        else:

            st.warning(
                "Display name cannot be empty."
            )

    st.markdown("---")

    st.markdown("#### Account Information")

    col1, col2 = st.columns(2)

    with col1:

        st.markdown("**Email**")

        st.write(current_email)

    with col2:

        st.markdown("**Role**")

        st.write(role)

    if role == "CUSTOMER":

        customer_id = st.session_state.get(
            "customer_id"
        )

        if customer_id:

            st.markdown("**Customer ID**")

            st.code(
                str(customer_id).upper()
            )

    st.caption(
        "Account credentials and authentication settings "
        "will be managed through the Snowflake-backed "
        "authentication layer."
    )


with tab2:

    st.subheader(
        "Notification Preferences"
    )

    st.caption(
        "These preferences currently apply to the "
        "application session."
    )

    renewal_notifications = st.checkbox(
        "🔄 Renewal reminders",
        value=st.session_state.get(
            "notif_renewal",
            True
        ),
    )

    claim_notifications = st.checkbox(
        "📑 Pending claim updates",
        value=st.session_state.get(
            "notif_claims",
            True
        ),
    )

    offer_notifications = st.checkbox(
        "🎁 Personalized offers",
        value=st.session_state.get(
            "notif_offers",
            True
        ),
    )

    st.session_state[
        "notif_renewal"
    ] = renewal_notifications

    st.session_state[
        "notif_claims"
    ] = claim_notifications

    st.session_state[
        "notif_offers"
    ] = offer_notifications

    st.markdown("---")

    if st.button(
        "Save Notification Preferences",
        type="primary",
    ):

        st.success(
            "Notification preferences saved for this session."
        )

with tab3:

    st.subheader(
        "Security & Access"
    )

    st.info(
        f"Current application role: **{role}**"
    )

    if role == "CUSTOMER":

        st.markdown(
            "##### Customer Access Scope"
        )

        st.markdown(
            """
            - ✔️ Own customer profile
            - ✔️ Own policies
            - ✔️ Own claims
            - ✔️ Own payment information
            - ✔️ Own interactions
            - ✔️ Personalized offers
            - ✔️ Customer AI assistant
            """
        )

        st.warning(
            "Customer access is restricted to the "
            "authenticated customer's data."
        )

    elif role == "EMPLOYEE":

        enforce_employee_boundary()

        st.markdown(
            "##### Relationship Manager Access Scope"
        )

        st.markdown(
            """
            - ✔️ Customer search
            - ✔️ Customer 360
            - ✔️ Policies and claims
            - ✔️ Customer interactions
            - ✔️ AI insights when available
            - ✔️ Next Best Actions
            - ✔️ Action history
            - ✔️ Analytics
            - ✔️ System health
            """
        )

        st.warning(
            "Employee access is intended for authorized "
            "relationship-management workflows."
        )

    else:

        st.error(
            "Unknown application role."
        )


with tab4:

    st.subheader(
        "Display Preferences"
    )

    col1, col2 = st.columns(2)

    with col1:

        current_theme = st.session_state.get(
            "theme",
            "Dark"
        )

        theme_choice = st.radio(
            "Theme Preference",
            [
                "Light",
                "Dark",
            ],
            index=(
                1
                if current_theme == "Dark"
                else 0
            ),
        )

        st.session_state[
            "theme"
        ] = theme_choice

    with col2:

        current_language = st.session_state.get(
            "language",
            "English"
        )

        languages = [
            "English",
            "Hindi",
            "Marathi",
            "Bengali",
        ]

        language = st.selectbox(
            "Language",
            languages,
            index=(
                languages.index(current_language)
                if current_language in languages
                else 0
            ),
        )

        st.session_state[
            "language"
        ] = language

    st.markdown("---")

    st.caption(
        "Theme and language preferences are currently "
        "stored in the application session."
    )

st.markdown("---")

st.subheader(
    "ℹ️ Application Status"
)

col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        "Role",
        role
    )

with col2:

    st.metric(
        "Theme",
        st.session_state.get(
            "theme",
            "Dark"
        )
    )

with col3:

    st.metric(
        "Language",
        st.session_state.get(
            "language",
            "English"
        )
    )
