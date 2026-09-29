import streamlit as st
import pandas as pd
from utils.security import enforce_employee_boundary

enforce_employee_boundary()

st.title("📈 Enterprise Analytics & Risk Intelligence")
st.write("Analyze high-risk customer growth trends, churn indicators, claim spikes, and platform data hygiene metrics.")

# 1. Data Hygiene & Anomalies Section (Moved here from System Health)
st.markdown("### 📊 Data Hygiene & Anomalies")

col1, col2, col3 = st.columns(3)
col1.metric("Missing Transcripts", "14", "-2 this week", delta_color="inverse")
col2.metric("Conflicting Signals", "3", "Requires Review", delta_color="off")
col3.metric("Human Review Required", "4", "Low confidence", delta_color="off")

col4, col5, _ = st.columns(3)
col4.metric("Unprocessed Calls", "7", "Pending queue", delta_color="off")
col5.metric("Failed Transcriptions", "1", "Audio error", delta_color="inverse")

st.markdown("---")

# 2. Visual Graphs & Trends
st.markdown("### 📉 High-Risk Customers & Churn Trend Analysis")

# Mock trend data for high risk cases over recent weeks
trend_data = pd.DataFrame({
    "Week": ["Week 1", "Week 2", "Week 3", "Week 4", "Week 5", "Week 6 (Current)"],
    "High Risk Cases": [42, 55, 68, 61, 79, 86],
    "Resolved Interventions": [30, 40, 52, 50, 65, 74]
})

st.line_chart(trend_data.set_index("Week"))
st.caption("Figure: Weekly progression of flagged high-risk customer accounts vs. successfully resolved RM interventions.")

st.markdown("---")

# 3. Claims & Renewal Risk Distribution
col_a, col_b = st.columns(2)

with col_a:
    st.markdown("##### ⚠️ Churn Triggers Breakdown")
    trigger_data = pd.DataFrame({
        "Trigger Factor": ["Premium Increase", "Pending Claim Delay", "Competitor Mention", "Poor Support Call"],
        "Percentage": [45, 25, 20, 10]
    })
    st.bar_chart(trigger_data.set_index("Trigger Factor"))

with col_b:
    st.markdown("##### 📑 Claims Status Distribution")
    claims_dist = pd.DataFrame({
        "Status": ["Approved", "In Progress", "Under Investigation", "Rejected"],
        "Count": [450, 120, 35, 15]
    })
    st.bar_chart(claims_dist.set_index("Status"))