import streamlit as st
import pandas as pd
from utils.security import enforce_employee_boundary

enforce_employee_boundary()

st.title("⚙️ System & Data Quality Health Dashboard")
st.write("Monitor core platform infrastructure, database connectivity, and automated ingestion pipelines.")


st.markdown("### 🖥️ Core System Status")
col_s1, col_s2, col_s3 = st.columns(3)
col_s1.metric("Database Connection", "Healthy", "🟢 Connected")
col_s2.metric("Customer Data", "1,248 records", "🟢 Synchronized")
col_s3.metric("Interaction Data", "4,821 records", "🟢 Live Feed")

col_s4, col_s5, col_s6 = st.columns(3)
col_s4.metric("Transcription Pipeline", "Healthy", "🟢 Operational")
col_s5.metric("AI Insight Pipeline", "Healthy", "🟢 Operational")
col_s6.metric("NBA Engine", "Healthy", "🟢 Ready")

st.markdown("---")


st.markdown("### 🔍 Drill-Down Inspection Reports")
view_option = st.selectbox(
    "Select data quality category to inspect:",
    [
        "Select a category...",
        "Missing Transcripts List", 
        "Conflicting Signals List",
        "Unprocessed Calls List",
        "Failed Transcriptions List",
        "Human Review Required List"
    ]
)

# 3. Dynamic Inspection Data Tables Based on Selection
if view_option == "Missing Transcripts List":
    st.warning("⚠️ Showing customers who have recent interactions logged, but whose call transcripts are missing (Evaluated as UNKNOWN).")
    missing_data_df = pd.DataFrame([
        {"customer_id": "CUST-1042", "name": "Sarah Jenkins", "last_interaction_date": "2026-03-12", "interaction_type": "Phone Call", "status": "Missing Transcript"},
        {"customer_id": "CUST-1089", "name": "Michael Chang", "last_interaction_date": "2026-03-10", "interaction_type": "Support Ticket", "status": "Missing Transcript"},
        {"customer_id": "CUST-1150", "name": "Elena Rostova", "last_interaction_date": "2026-03-08", "interaction_type": "Live Chat", "status": "Missing Transcript"},
    ])
    st.dataframe(missing_data_df, use_container_width=True)
    
    selected_cust = st.selectbox("Select Customer to Investigate", missing_data_df["customer_id"].tolist())
    if st.button("Inspect Customer Profile"):
        st.session_state["selected_customer_id"] = selected_cust
        st.switch_page("pages/customer_360.py")

elif view_option == "Conflicting Signals List":
    st.error("🚨 Showing customers with contradictory indicators (e.g., negative call transcript sentiment vs. positive CSAT survey).")
    conflict_data_df = pd.DataFrame([
        {"customer_id": "CUST-1005", "name": "David Smith", "call_sentiment": "Negative", "survey_sentiment": "Positive", "confidence": "Low (42%)", "action": "Human Review Recommended"},
        {"customer_id": "CUST-1077", "name": "Amanda White", "call_sentiment": "Negative", "survey_sentiment": "Positive", "confidence": "Low (38%)", "action": "Human Review Recommended"},
        {"customer_id": "CUST-1123", "name": "Robert Taylor", "call_sentiment": "Neutral", "survey_sentiment": "Positive", "confidence": "Low (51%)", "action": "Human Review Recommended"},
    ])
    st.dataframe(conflict_data_df, use_container_width=True)

elif view_option == "Unprocessed Calls List":
    st.info("📞 Showing audio recordings queued for background LLM and pipeline ingestion.")
    unprocessed_df = pd.DataFrame([
        {"call_id": "CALL-9011", "customer_id": "CUST-1201", "duration": "4m 12s", "queued_at": "2026-06-08 14:20", "status": "Pending Queue"},
        {"call_id": "CALL-9012", "customer_id": "CUST-1345", "duration": "2m 45s", "queued_at": "2026-06-08 15:01", "status": "Pending Queue"},
        {"call_id": "CALL-9013", "customer_id": "CUST-1410", "duration": "6m 02s", "queued_at": "2026-06-08 16:15", "status": "Pending Queue"},
    ])
    st.dataframe(unprocessed_df, use_container_width=True)
    if st.button("Process Queue Now"):
        st.success("Triggered background pipeline sync successfully!")

elif view_option == "Failed Transcriptions List":
    st.error("❌ Showing interaction files that failed Speech-to-Text conversion due to audio corruption or timeout.")
    failed_df = pd.DataFrame([
        {"call_id": "CALL-8802", "customer_id": "CUST-1099", "error_type": "Audio Corrupted / Static", "timestamp": "2026-06-07 11:45", "action": "Manual Audio Review Required"},
    ])
    st.dataframe(failed_df, use_container_width=True)

elif view_option == "Human Review Required List":
    st.warning("👤 Showing cases where AI confidence was below threshold or flags crossed safety boundaries.")
    review_df = pd.DataFrame([
        {"review_id": "REV-301", "customer_id": "CUST-1002", "reason": "Low AI Confidence (31%) on Churn Prediction", "assigned_rm": "RM-James"},
        {"review_id": "REV-302", "customer_id": "CUST-1044", "reason": "Conflicting Legal/Policy Complaint Signal", "assigned_rm": "RM-Sarah"},
        {"review_id": "REV-303", "customer_id": "CUST-1102", "reason": "Potential Fraud Keyword Detected in Call", "assigned_rm": "RM-Alex"},
        {"review_id": "REV-304", "customer_id": "CUST-1250", "reason": "Extreme Negative Sentiment Spike", "assigned_rm": "RM-David"},
    ])
    st.dataframe(review_df, use_container_width=True)

else:
    st.success("✅ System operational. Choose an anomaly category from the dropdown above to audit specific system records.")