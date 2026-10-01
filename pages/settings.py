import streamlit as st

from utils.security import enforce_employee_boundary


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

        language = st.selectbox(
            "Language",
            [
                "English",
                "Hindi",
                "Marathi",
                "Bengali",
            ],
            index=(
                [
                    "English",
                    "Hindi",
                    "Marathi",
                    "Bengali",
                ].index(current_language)
                if current_language
                in [
                    "English",
                    "Hindi",
                    "Marathi",
                    "Bengali",
                ]
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