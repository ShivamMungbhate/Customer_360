import streamlit as st
from utils.security import enforce_employee_boundary

enforce_employee_boundary()

user_email = st.session_state.get("user_email", "RM User")

rm_name = user_email.split("@")[0].capitalize()

st.markdown(f"### Good morning, {rm_name}")
st.caption("Relationship Manager Command Center")
st.markdown("---")


col1, col2, col3 = st.columns(3)
col1.metric("Total Customers", "1,248")
col2.metric("At Risk", "86", delta="-4 vs last week", delta_color="inverse")
col3.metric("Renewals <30 days", "32", delta="Action Required", delta_color="off")

st.markdown("---")


st.markdown("#### 🔴 High Risk Customers Needing Attention")


with st.container(border=True):
    col_info, col_action = st.columns([3, 1])
    
    with col_info:
        st.markdown("##### Rahul Sharma &nbsp;&nbsp;&nbsp; `CUST-1001`")
        st.markdown("**Renewal:** 12 days &nbsp;|&nbsp; ⚠️ **Negative sentiment** &nbsp;|&nbsp; 🔄 **Switching intent detected**")
        st.caption("Customer complained about premium increase and mentioned competitor rates during last call transcript.")
        
    with col_action:
        st.write("") 
        if st.button("View Customer 360", key="btn_rahul", use_container_width=True, type="primary"):
            st.session_state["selected_customer_id"] = "CUST-1001"
            st.switch_page("pages/customer_360.py")


with st.container(border=True):
    col_info, col_action = st.columns([3, 1])
    
    with col_info:
        st.markdown("##### Ananya Singh &nbsp;&nbsp;&nbsp; `CUST-1045`")
        st.markdown("**Pending Claim** &nbsp;|&nbsp; 💬 **4 support interactions** this week")
        st.caption("Claim status is delayed under review; customer has repeatedly contacted support expressing frustration.")
        
    with col_action:
        st.write("")
        if st.button("View Customer 360", key="btn_ananya", use_container_width=True, type="primary"):
            st.session_state["selected_customer_id"] = "CUST-1045"
            st.switch_page("pages/customer_360.py")


st.markdown("---")
st.subheader("🔍 Quick Search Registry")
search_query = st.text_input("Search by customer name, ID, or city...")
if search_query:
    st.info(f"Searching database records for: **{search_query}**")
    
# For snowflake live data 

#import streamlit as st
#from services.snowflake_service import get_snowflake_connection

#st.title("📊 Employee Dashboard & Risk Command Center")




#total_attention = 12       # Replace with live count query
#upcoming_renewals = 28     # Replace with SQL result
#high_churn = 5             # Replace with SQL result
#pending_claims = 8         # Replace with SQL result

#col1, col2, col3, col4 = st.columns(4)
#col1.metric("Customers Needing Attention", total_attention, "+2 today")
#col2.metric("Upcoming Renewals (30d)", upcoming_renewals, "-4 vs avg")
#col3.metric("High Churn Risk", high_churn, "Action Required")
#col4.metric("Pending Claims", pending_claims, "Avg 2.4 days")'''