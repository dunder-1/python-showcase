import os
import features as ft

def clear():
    os.system("cls")

def print_options():
    print("##################")
    print("[1] Show Employees")
    print("[2] Add new Employee")
    print("[3] Show Times")
    print("[4] Add new Time")

    print("[9] Exit")
    print("##################")

def safe_input(prompt:str, valid_options:list):
    _in = input(prompt)
    while _in not in valid_options:
        print("I dont understand!")
        _in = input(prompt)

    return _in

def print_employees():
    for emp in ft.get_all_employees():
        print(f"[{emp['emp_id']}]", emp["first_name"], emp["last_name"])


while True:
    clear()
    print("What do you want to do?")
    print_options()
    selection = safe_input("Please choose: ", ["1", "2", "3", "4", "9"])

    if selection == "1":
        clear()
        print("All Employees:")
        for elem in ft.get_all_employees():
            print(elem)
        selection = safe_input("Back to main menu? (y) ", ["y"])
    
    elif selection == "2":
        clear()
        print("Add new Employee:")
        _first_name = input("Please add first name: ")
        _last_name = input("Please add last name: ")
        _hours_per_week = input("Please add hours per week: ")

        confirm = safe_input("Is this ok? (y/n) ", ["y", "n"])
        if confirm == "y":
            print("Thank you!")
            ft.add_employee(_first_name, _last_name, int(_hours_per_week))
        else:
            print("...ok")

    elif selection == "3":
        clear()
        print("Show times of employee:")
        print("Please choose one of these employees:")
        print_employees()

        _emp_id = safe_input("Enter number: ", [str(i["emp_id"]) for i in ft.get_all_employees()])
        for elem in ft.get_times_by_emp_id(int(_emp_id)):
            print(elem)
        selection = safe_input("Back to main menu? (y) ", ["y"])

    elif selection == "4":
        clear()
        print("Add new Time:")
        print("Please choose one of these employees:")
        print_employees()
        _emp_id = safe_input("Enter number: ", [str(i["emp_id"]) for i in ft.get_all_employees()])
        _date = input("Enter date: (format = YYYY/MM/DD) ")
        _date = [int(i) for i in _date.split("/")]
        _hours = safe_input("Enter hours: ", [str(i) for i in range(0, 25)])
        _description = input("Enter description: ")

        confirm = safe_input("Is this ok? (y/n) ", ["y", "n"])
        if confirm == "y":
            print("Thank you!")
            ft.add_time(int(_emp_id), _date, int(_hours), _description)
        else:
            print("...ok")

    elif selection == "9":
        clear()
        print("Goodbye...")
        break
