import streamlit as st

st.title("⚙️ Application Settings & Preferences")
st.write("Customize your profile display name, background AI models, notification preferences, and data access views.")


tab1, tab2, tab3, tab4 = st.tabs(["👤 Profile & AI", "🔔 Notifications", "🔒 Security & Access", "🎨 Display & Theme"])

with tab1:
    st.subheader("User Profile Configuration")
    current_email = st.session_state.get("user_email", "user@insurance.com")
    default_display = st.session_state.get("display_name", current_email.split("@")[0].capitalize())
    
    new_display_name = st.text_input("Display Name", value=default_display, help="This name will appear across your dashboards.")
    st.session_state["display_name"] = new_display_name
    
    role = st.session_state.get("role", "CUSTOMER")
    if role == "EMPLOYEE":
        st.markdown("---")
        st.subheader("Background AI Model Configuration")
        current_model = st.session_state.get("bg_llm_model", "llama3")
        selected_model = st.selectbox(
            "Active Background LLM (Ollama)",
            ["llama3", "mistral", "gemma", "phi3"],
            index=["llama3", "mistral", "gemma", "phi3"].index(current_model) if current_model in ["llama3", "mistral", "gemma", "phi3"] else 0
        )
        st.session_state["bg_llm_model"] = selected_model

with tab2:
    st.subheader("Notification Preferences")
    st.session_state["notif_renewal"] = st.checkbox("Renewal reminders", value=st.session_state.get("notif_renewal", True))
    st.session_state["notif_claims"] = st.checkbox("Pending claim updates", value=st.session_state.get("notif_claims", True))
    st.session_state["notif_offers"] = st.checkbox("Exclusive discount offers", value=st.session_state.get("notif_offers", True))

with tab3:
    st.subheader("Security & Access Permissions")
    role = st.session_state.get("role", "CUSTOMER")
    st.info(f"Current Active Role: **{role}**")
    
    if role == "CUSTOMER":
        st.markdown("##### Customer Portal Data Access:")
        st.markdown("* ✔️ Own Profile & Active Policies\n* ✔️ Own Claims & Payment History\n* ✔️️ Secure AI Assistant\n* ✔️ Personalized Offers")
    else:
        st.markdown("##### Relationship Manager Data Access Permissions:")
        st.markdown("* ✔️ Full Customer Profiles, Policies, Claims, Interventions & AI Insights")

with tab4:
    st.subheader("Application Services & Layout")
    col_a, col_b = st.columns(2)
    with col_a:
        theme_choice = st.radio("Theme", ["Light", "Dark"], index=1 if st.session_state.get("theme", "Dark") == "Dark" else 0)
        st.session_state["theme"] = theme_choice
    with col_b:
        language = st.selectbox("Language", ["English", "Spanish", "French", "German"], index=0)
        st.session_state["language"] = language

st.markdown("---")
if st.button("Save Preferences", type="primary"):
    st.success(f"Preferences saved successfully! Display name updated to **{st.session_state.get('display_name')}**.")