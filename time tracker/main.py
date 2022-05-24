import features as ft

########################
add_employees = True
show_employees = False
add_time = True
show_times = True

########################

# Add employees
if add_employees:
    ft.add_employee("Kater", "Karlo", 40)
    ft.add_employee("Katzo", "Matzo", 30)

# Show Employees
if show_employees:
    print(ft.get_all_employees())
    print()
    print(ft.get_employee_by_id(1))
    print()
    print(ft.get_employee_by_name("Katzo", "Matzo"))

# Add time
if add_time:
    ft.add_time(emp_id=1,
                date="24.05.2022",
                hours=8,
                description="Dies und das.")

# Show Times (by Employee)
if show_times:
    print(ft.get_times_by_emp_id(1))