from datetime import datetime
import streamlit as st
import features as ft

st.title("⏲ Time Tracker")

if st.sidebar.button("🚮 Reset Data"):
    ft.write_to(ft.DB["emp"], [])
    ft.write_to(ft.DB["time"], [])



selection = st.selectbox("What do you want to do?",
                         ["Show all Employees",
                          "Add new Employee",
                          "Show Times of Employee",
                          "Add new Time"])
st.write("---")

if selection == "Show all Employees":
    st.table(ft.get_all_employees())

elif selection == "Add new Employee":
    with st.form("add_emp", clear_on_submit=True):
        _first_name = st.text_input("First name:")
        _last_name = st.text_input("Last name:")
        _hours_per_week = st.number_input("Hours per Week:", min_value=1, value=40)

        if st.form_submit_button("Add"):
            if all([_first_name, _last_name, _hours_per_week]):
                ft.add_employee(_first_name, _last_name, _hours_per_week)
                st.success("Added new employee!")
            else:
                st.error("Please fill all information!")

elif selection == "Show Times of Employee":
    _emp = st.selectbox("Select Employee:",
                        ft.get_all_employees(),
                        format_func=lambda x: f"{x['first_name']} {x['last_name']} (emp_id = {x['emp_id']})")
    if _emp:

        for week in range(1, 53):
            _ = ft.get_times_by_week(_emp["emp_id"], week, get_sum=True)

        st.write("---")
        st.table(ft.get_times_by_emp_id(_emp["emp_id"]))

elif selection == "Add new Time":
    with st.form("add_time", clear_on_submit=True):
        col1, col2, col3 = st.columns([2, 1, 1])

        _emp = col1.selectbox("Select Employee:",
                        ft.get_all_employees(),
                        format_func=lambda x: f"{x['first_name']} {x['last_name']} (emp_id = {x['emp_id']})")
        _date = col2.date_input("Enter Date:")
        _hours = col3.number_input("How many hours?", min_value=1, max_value=24)
        _description = st.text_area("Describe what you have done:",
                                    max_chars=120)


        if st.form_submit_button("Add"):
            if all([_emp, _date, _hours, _description]):
                ft.add_time(_emp["emp_id"],
                            _date,
                            _hours,
                            _description)
                st.success("Added new time!")
            else:
                st.error("Please fill all information!")

