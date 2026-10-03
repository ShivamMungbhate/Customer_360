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