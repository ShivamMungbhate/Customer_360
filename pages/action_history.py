import streamlit as st
import pandas as pd
from datetime import datetime

from utils.security import enforce_employee_boundary
from services.snowflake_service import (
    get_all_action_history,
    create_action_history,
    update_action_status,
    update_action_employee,
    get_action_by_id,
)

enforce_employee_boundary()
st.markdown("""
<style>

/* Import modern font */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

/* Global theme */
.stApp {
    background:
        radial-gradient(ellipse at 10% 0%, rgba(37, 99, 235, 0.16), transparent 40%),
        radial-gradient(ellipse at 90% 10%, rgba(124, 58, 237, 0.12), transparent 35%),
        #080d1a;
    color: #e5eaf5;
    font-family: 'Inter', sans-serif;
}

[data-testid="stHeader"] {
    background: rgba(8, 13, 26, 0.75);
}

[data-testid="stMainBlockContainer"] {
    padding-top: 2.4rem;
    padding-bottom: 3rem;
    max-width: 1500px;
}

/* Main headings */
h1 {
    font-size: clamp(1.8rem, 3vw, 2.6rem) !important;
    font-weight: 800 !important;
    letter-spacing: -1.2px;
    line-height: 1.3 !important;
    color: #f8fafc !important;
    background: linear-gradient(100deg, #ffffff 15%, #93c5fd 60%, #c4b5fd 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    padding-bottom: 8px;
}

h2, h3 {
    color: #f1f5f9 !important;
    font-weight: 700 !important;
    letter-spacing: -0.4px;
}

h4, h5, h6 {
    color: #dbeafe !important;
}

p, label, li {
    color: #cbd5e1;
}

[data-testid="stCaptionContainer"] {
    color: #94a3b8;
    font-size: 0.82rem;
}

/* Metric cards */
[data-testid="stMetric"] {
    background: linear-gradient(
        145deg,
        rgba(23, 35, 60, 0.96),
        rgba(15, 23, 42, 0.96)
    );
    border: 1px solid rgba(96, 165, 250, 0.22);
    border-radius: 18px;
    padding: 22px 20px;
    box-shadow: 0 8px 30px rgba(0, 0, 0, 0.16);
    transition: transform 0.2s ease, border-color 0.2s ease;
}

[data-testid="stMetric"]:hover {
    transform: translateY(-3px);
    border-color: rgba(96, 165, 250, 0.65);
}

[data-testid="stMetricLabel"] {
    color: #a5b4fc !important;
    font-weight: 600;
    font-size: 0.9rem;
}

[data-testid="stMetricValue"] {
    color: #f8fafc !important;
    font-size: clamp(1.5rem, 2.5vw, 2.2rem);
    font-weight: 800;
}

/* Action record bordered containers */
[data-testid="stVerticalBlockBorderWrapper"] {
    background: linear-gradient(
        145deg,
        rgba(17, 27, 48, 0.96),
        rgba(12, 19, 35, 0.96)
    );
    border: 1px solid rgba(71, 85, 105, 0.55) !important;
    border-radius: 18px !important;
    padding: 18px 20px;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
    transition: border-color 0.2s ease, box-shadow 0.2s ease;
}

[data-testid="stVerticalBlockBorderWrapper"]:hover {
    border-color: rgba(96, 165, 250, 0.48) !important;
    box-shadow: 0 12px 30px rgba(0, 0, 0, 0.2);
}

/* Primary and secondary buttons */
.stButton > button {
    background: linear-gradient(110deg, #2563eb, #4f46e5);
    color: #ffffff !important;
    border: 1px solid rgba(147, 197, 253, 0.25);
    border-radius: 11px;
    padding: 0.62rem 1rem;
    font-weight: 600;
    letter-spacing: 0.1px;
    min-height: 42px;
    box-shadow: 0 4px 14px rgba(37, 99, 235, 0.18);
    transition: all 0.2s ease;
}

.stButton > button:hover {
    background: linear-gradient(110deg, #3b82f6, #6366f1);
    border-color: #93c5fd;
    box-shadow: 0 6px 20px rgba(59, 130, 246, 0.3);
    transform: translateY(-1px);
}

.stButton > button:focus-visible {
    outline: 2px solid #93c5fd;
    outline-offset: 3px;
}

.stButton > button:active {
    transform: scale(0.98);
}

/* Text inputs and dropdowns */
.stTextInput input,
.stTextArea textarea,
.stNumberInput input {
    background: #111b30 !important;
    color: #f1f5f9 !important;
    border: 1px solid #334155 !important;
    border-radius: 10px !important;
    min-height: 42px;
}

.stTextInput input:focus,
.stTextArea textarea:focus,
.stNumberInput input:focus {
    border-color: #60a5fa !important;
    box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.16) !important;
}

.stTextInput input::placeholder,
.stTextArea textarea::placeholder {
    color: #64748b !important;
}

/* Select boxes */
[data-testid="stSelectbox"] [data-baseweb="select"] > div,
[data-testid="stMultiSelect"] [data-baseweb="select"] > div {
    background: #111b30;
    border-color: #334155;
    border-radius: 10px;
    color: #e2e8f0;
}

[data-baseweb="popover"],
[data-baseweb="menu"] {
    background: #111b30;
    border: 1px solid #334155;
    border-radius: 10px;
}

[data-baseweb="menu"] * {
    color: #e2e8f0;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #101a30 0%, #0b1120 100%);
    border-right: 1px solid rgba(96, 165, 250, 0.18);
}

[data-testid="stSidebar"] > div:first-child {
    background: transparent;
}

[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: #f8fafc !important;
}

/* Success, info, warning and error messages */
[data-testid="stAlert"] {
    border-radius: 12px;
    border: 1px solid rgba(148, 163, 184, 0.2);
    padding: 12px 16px;
}

/* Code blocks and customer IDs */
[data-testid="stCode"] {
    border: 1px solid rgba(96, 165, 250, 0.2);
    border-radius: 10px;
    overflow: hidden;
}

code {
    color: #93c5fd !important;
}

/* Expanders */
[data-testid="stExpander"] {
    background: rgba(17, 27, 48, 0.7);
    border: 1px solid #334155;
    border-radius: 14px;
    overflow: hidden;
}

[data-testid="stExpander"] summary {
    color: #e2e8f0;
    font-weight: 600;
}

[data-testid="stExpander"] summary:hover {
    color: #93c5fd;
}

/* Data table */
[data-testid="stDataFrame"] {
    border: 1px solid #334155;
    border-radius: 12px;
    overflow: hidden;
}

/* Dividers */
hr {
    border-color: rgba(100, 116, 139, 0.28) !important;
    margin-top: 1.5rem;
    margin-bottom: 1.5rem;
}

/* Workflow columns and general spacing */
[data-testid="stHorizontalBlock"] {
    gap: 1rem;
}

/* Responsive layout */
@media (max-width: 768px) {
    [data-testid="stMainBlockContainer"] {
        padding: 1.2rem 1rem 2rem;
    }

    [data-testid="stMetric"] {
        padding: 14px 12px;
        border-radius: 13px;
    }

    [data-testid="stVerticalBlockBorderWrapper"] {
        padding: 12px;
        border-radius: 14px !important;
    }

    h1 {
        letter-spacing: -0.6px;
    }
}

/* Reduced motion accessibility */
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

st.title("📋 Employee Action History & Execution Tracker")

st.write(
    "Track customer actions created from the Next Best Action engine, "
    "including ownership, status, timestamps, and completion."
)

employee_id = str(
    st.session_state.get("employee_id", "Enter Employee ID")
).strip()

st.caption(f"Employee: `{employee_id}`")

actions_df = get_all_action_history()

total_actions = len(actions_df)
open_actions = 0
in_progress_actions = 0
completed_actions = 0

if not actions_df.empty and "STATUS" in actions_df.columns:
    status_series = (
        actions_df["STATUS"]
        .fillna("UNKNOWN")
        .astype(str)
        .str.upper()
        .str.replace("_", " ", regex=False)
    )

    open_actions = int(status_series.eq("OPEN").sum())
    in_progress_actions = int(status_series.eq("IN PROGRESS").sum())
    completed_actions = int(
        status_series.isin(["COMPLETED", "DONE", "CLOSED"]).sum()
    )

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Actions", total_actions)

with col2:
    st.metric("Open", open_actions)

with col3:
    st.metric("In Progress", in_progress_actions)

with col4:
    st.metric("Completed", completed_actions)

st.markdown("---")

st.subheader("⚡ Create Action from NBA")

selected_nba = st.session_state.get("selected_nba")

if selected_nba:

    customer_id = str(
        selected_nba.get("customer_id", "")
    ).strip().upper()

    action = str(
        selected_nba.get("action", "Customer Follow-up")
    ).strip()

    reason = str(
        selected_nba.get("reason", "")
    ).strip()

    priority = str(
        selected_nba.get("priority", "MEDIUM")
    ).strip().upper()

    st.success(
        "A recommendation is currently selected from the NBA Engine."
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("**Customer**")
        st.code(customer_id or "Unknown")

    with col2:
        st.markdown("**Recommended Action**")
        st.write(action)

    with col3:
        st.markdown("**Priority**")
        st.write(priority)

    if reason:
        st.markdown("**Reason**")
        st.info(reason)

    if not customer_id:
        st.error("Customer ID is missing from the selected NBA.")
    else:

        action_details = (
            f"Priority: {priority}. Reason: {reason}"
        )

        generated_action_id = (
            f"ACT-{datetime.now().strftime('%Y%m%d%H%M%S%f')}"
        )

        st.caption(
            f"New Action ID: `{generated_action_id}`"
        )

        if st.button(
            "➕ Create Action",
            key="create_nba_action",
            use_container_width=True
        ):

            existing_action = get_action_by_id(
                generated_action_id
            )

            if not existing_action.empty:

                st.error(
                    "Generated Action ID already exists. Please try again."
                )

            else:

                success = create_action_history(
                    action_id=generated_action_id,
                    customer_id=customer_id,
                    employee_id=employee_id,
                    action_type=action,
                    action_details=action_details,
                    status="OPEN",
                )

                if success:

                    st.success(
                        f"Action `{generated_action_id}` created successfully."
                    )

                    st.session_state.pop(
                        "selected_nba",
                        None
                    )

                    st.rerun()

                else:

                    st.error(
                        "Action could not be created in Snowflake."
                    )

else:

    st.info(
        "No NBA action is currently selected. "
        "Go to **Next Best Action** and select an action first."
    )

st.markdown("---")

st.subheader("🔎 Action Explorer")

filter_col1, filter_col2, filter_col3 = st.columns(3)

with filter_col1:
    customer_filter = st.text_input(
        "Customer ID",
        placeholder="Example: C001"
    )

with filter_col2:
    status_filter = st.selectbox(
        "Status",
        [
            "All",
            "OPEN",
            "IN_PROGRESS",
            "COMPLETED",
        ]
    )

with filter_col3:
    action_type_filter = st.text_input(
        "Action Type",
        placeholder="Example: RETENTION"
    )

filtered_df = actions_df.copy()

if (
    customer_filter
    and not filtered_df.empty
    and "CUSTOMER_ID" in filtered_df.columns
):

    filtered_df = filtered_df[
        filtered_df["CUSTOMER_ID"]
        .astype(str)
        .str.upper()
        .str.contains(
            customer_filter.strip().upper(),
            na=False
        )
    ]

if (
    status_filter != "All"
    and not filtered_df.empty
    and "STATUS" in filtered_df.columns
):

    normalized_status = (
        filtered_df["STATUS"]
        .fillna("UNKNOWN")
        .astype(str)
        .str.upper()
        .str.replace("_", " ", regex=False)
    )

    filtered_df = filtered_df[
        normalized_status.eq(
            status_filter.replace("_", " ")
        )
    ]

if (
    action_type_filter
    and not filtered_df.empty
    and "ACTION_TYPE" in filtered_df.columns
):

    filtered_df = filtered_df[
        filtered_df["ACTION_TYPE"]
        .astype(str)
        .str.upper()
        .str.contains(
            action_type_filter.strip().upper(),
            na=False
        )
    ]

st.caption(
    f"Showing {len(filtered_df)} action(s)"
)

st.markdown("### 📋 Action Records")

if filtered_df.empty:

    st.info("No action history records found.")

else:

    for index, action_record in filtered_df.iterrows():

        action_id = str(
            action_record.get(
                "ACTION_ID",
                index
            )
        ).strip()

        customer_id = str(
            action_record.get(
                "CUSTOMER_ID",
                "UNKNOWN"
            )
        ).strip()

        action_type = str(
            action_record.get(
                "ACTION_TYPE",
                "Action"
            )
        ).strip()

        status = str(
            action_record.get(
                "STATUS",
                "UNKNOWN"
            )
        ).upper().strip()

        action_details = action_record.get(
            "ACTION_DETAILS",
            ""
        )

        created_at = action_record.get(
            "CREATED_AT",
            "Not available"
        )

        completed_at = action_record.get(
            "COMPLETED_AT",
            None
        )

        assigned_employee = action_record.get(
            "EMPLOYEE_ID",
            "Unassigned"
        )

        if (
            pd.isna(assigned_employee)
            or str(assigned_employee).strip() == ""
        ):
            assigned_employee = "Unassigned"

        with st.container(border=True):

            col1, col2, col3 = st.columns(
                [2, 4, 1]
            )

            with col1:

                st.markdown(
                    f"**Customer:** `{customer_id}`"
                )

                st.caption(
                    f"Action ID: `{action_id}`"
                )

            with col2:

                st.markdown(
                    f"**{action_type}**"
                )

                if (
                    pd.notna(action_details)
                    and str(action_details).strip()
                ):

                    st.write(
                        str(action_details)
                    )

            with col3:

                st.metric(
                    "Status",
                    status
                )

            st.caption(
                f"Created: {created_at}"
            )

            st.caption(
                f"Assigned Employee: {assigned_employee}"
            )

            if (
                pd.notna(completed_at)
                and str(completed_at)
                not in ["", "None", "NaT"]
            ):

                st.caption(
                    f"Completed: {completed_at}"
                )

            st.markdown("")

            control_col1, control_col2, control_col3 = st.columns(
                [2, 2, 2]
            )

            with control_col1:

                status_options = [
                    "OPEN",
                    "IN_PROGRESS",
                    "COMPLETED",
                ]

                current_status = status.upper().strip()

                if current_status not in status_options:
                    current_index = 0
                else:
                    current_index = status_options.index(
                        current_status
                    )

                selected_status = st.selectbox(
                    "Update Status",
                    status_options,
                    index=current_index,
                    key=f"status_{action_id}"
                )

            with control_col2:

                if st.button(
                    "💾 Update Status",
                    key=f"update_{action_id}",
                    use_container_width=True
                ):

                    selected_status = str(
                        selected_status
                    ).strip().upper()

                    current_status = str(
                        status
                    ).strip().upper()

                    if selected_status == current_status:

                        st.info(
                            "Action already has this status."
                        )

                    else:

                        with st.spinner(
                            "Updating action status..."
                        ):

                            success = update_action_status(
                                action_id=action_id,
                                status=selected_status
                            )

                        if success:

                            st.success(
                                f"Action `{action_id}` updated to "
                                f"`{selected_status}`."
                            )

                            st.rerun()

                        else:

                            st.error(
                                "Action status update failed. "
                                "Check the Snowflake error above."
                            )

            with control_col3:

                employee_input = st.text_input(
                    "Assign Employee",
                    value=(
                        ""
                        if assigned_employee == "Unassigned"
                        else str(assigned_employee)
                    ),
                    key=f"employee_{action_id}"
                )

                if st.button(
                    "👤 Assign",
                    key=f"assign_{action_id}",
                    use_container_width=True
                ):

                    if not employee_input.strip():

                        st.warning(
                            "Please enter an employee ID."
                        )

                    else:

                        success = update_action_employee(
                            action_id=action_id,
                            employee_id=employee_input.strip()
                        )

                        if success:

                            st.success(
                                "Employee assignment updated."
                            )

                            st.rerun()

st.markdown("---")

with st.expander(
    "📊 View Complete Action History"
):

    if actions_df.empty:

        st.info(
            "ACTION_HISTORY is currently empty."
        )

    else:

        display_columns = [
            "ACTION_ID",
            "CUSTOMER_ID",
            "EMPLOYEE_ID",
            "ACTION_TYPE",
            "ACTION_DETAILS",
            "CREATED_AT",
            "STATUS",
            "COMPLETED_AT",
        ]

        available_columns = [
            column
            for column in display_columns
            if column in actions_df.columns
        ]

        st.dataframe(
            actions_df[available_columns],
            use_container_width=True,
            hide_index=True
        )

st.markdown("---")

st.subheader("🔄 Action Execution Workflow")

workflow_col1, workflow_col2, workflow_col3, workflow_col4 = st.columns(4)

with workflow_col1:

    st.markdown("### 1️⃣ NBA")

    st.caption(
        "Recommendation is generated from customer signals."
    )

with workflow_col2:

    st.markdown("### 2️⃣ Create")

    st.caption(
        "Employee converts the recommendation into an action."
    )

with workflow_col3:

    st.markdown("### 3️⃣ Execute")

    st.caption(
        "Action moves from OPEN to IN_PROGRESS."
    )

with workflow_col4:

    st.markdown("### 4️⃣ Complete")

    st.caption(
        "Completed action is timestamped in Snowflake."
    )