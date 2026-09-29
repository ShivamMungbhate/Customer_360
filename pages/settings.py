import streamlit as st
from utils.security import enforce_employee_boundary


st.title("⚙️ Application Settings & Preferences")
st.write("Customize your dashboard behavior, background AI models, notification preferences, and data access views.")


tab1, tab2, tab3, tab4 = st.tabs(["🤖 AI & Models", "🔔 Notifications", "🔒 Security & Access", "🎨 Display & Theme"])

with tab1:
    st.subheader("Background AI Model Configuration")
    st.write("Select the local Ollama model to run background insight extraction and natural language processing.")
    
   
    current_model = st.session_state.get("bg_llm_model", "llama3")
    selected_model = st.selectbox(
        "Active Background LLM (Ollama)",
        ["llama3", "mistral", "gemma", "phi3"],
        index=["llama3", "mistral", "gemma", "phi3"].index(current_model) if current_model in ["llama3", "mistral", "gemma", "phi3"] else 0
    )
    st.session_state["bg_llm_model"] = selected_model
    st.success(f"Background AI tasks will use: **{selected_model}**")

with tab2:
    st.subheader("Notification Preferences")
    st.write("Configure which operational alerts you want to receive in real-time.")
    
    st.session_state["notif_churn"] = st.checkbox("High churn-risk alerts", value=st.session_state.get("notif_churn", True))
    st.session_state["notif_renewal"] = st.checkbox("Renewal reminders", value=st.session_state.get("notif_renewal", True))
    st.session_state["notif_claims"] = st.checkbox("Pending claim alerts", value=st.session_state.get("notif_claims", True))
    st.session_state["notif_daily_ai"] = st.checkbox("Daily AI summary", value=st.session_state.get("notif_daily_ai", False))
    st.session_state["notif_nba"] = st.checkbox("Next Best Action notifications", value=st.session_state.get("notif_nba", True))

with tab3:
    st.subheader("Security & Access Permissions")
    role = st.session_state.get("role", "EMPLOYEE")
    st.info(f"Current Active Role: **{role}**")
    
    if role == "EMPLOYEE":
        st.markdown("##### Relationship Manager Data Access Permissions:")
        st.markdown("""
        * ✔️ Customer profiles
        * ✔️ Policies
        * ✔️ Claims
        * ✔️ Payments
        * ✔️ Interactions
        * ✔️ AI Insights
        * ✔️ Next Best Actions
        """)
        
        st.markdown("##### Restricted Access:")
        st.markdown("""
        * ❌ Other employees' settings
        * ❌ System administration
        """)
    else:
        st.markdown("##### Customer Portal Data Access:")
        st.markdown("""
        * ✔️ Own Profile & Active Policies
        * ✔️ Own Claims & Payment History
        * ✔️ Secure AI Assistant
        """)

with tab4:
    st.subheader("Application Services & Layout")
    
    col_a, col_b = st.columns(2)
    with col_a:
        theme_choice = st.radio("Theme", ["Light", "Dark"], index=1 if st.session_state.get("theme", "Dark") == "Dark" else 0)
        st.session_state["theme"] = theme_choice
        
        default_dash = st.selectbox("Default Dashboard", ["Employee Dashboard", "Customer Portal"], index=0)
        st.session_state["default_dash"] = default_dash

    with col_b:
        default_view = st.selectbox("Default Customer View", ["Customer 360", "Summary View"], index=0)
        st.session_state["default_view"] = default_view
        
        rows_per_page = st.selectbox("Rows per page", [10, 25, 50, 100], index=1)
        st.session_state["rows_per_page"] = rows_per_page

    language = st.selectbox("Language", ["English", "Spanish", "French", "German"], index=0)
    st.session_state["language"] = language

st.markdown("---")
if st.button("Save Preferences", type="primary"):
    st.success("Your preferences have been successfully updated across the session!")