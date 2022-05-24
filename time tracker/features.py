import json
from datetime import datetime

DB = {"emp": "db/employees.json", "time": "db/times.json"}
DATE_FORMAT = "%Y/%m/%d"

def read_from(db_name:str) -> list[dict]:
    with open(db_name, "r", encoding="utf-8") as file:
        return json.load(file)

def write_to(db_name:str, changed_db:list[str]) -> None:
    with open(db_name, "w", encoding="utf-8") as file:
        json.dump(changed_db, file, indent=4, default=str)
"""
EMPLOYEE FUNCTIONS
"""

def add_employee(first_name:str, last_name:str, hours_per_week:int):
    data = read_from(DB["emp"])
    emp_id = 1 if not data else data[-1]["emp_id"] + 1
    data.append({"emp_id": emp_id,
                 "first_name": first_name, 
                 "last_name": last_name, 
                 "hours_per_week": hours_per_week})
    write_to(DB["emp"], data)

def get_all_employees() -> list[dict]:
    return read_from(DB["emp"])    

def get_employee_by_id(emp_id:int) -> dict:
    data = read_from(DB["emp"])
    for elem in data:
        if elem["emp_id"] == emp_id:
            return elem

def get_employee_by_name(first_name:str, last_name:str) -> dict:
    data = read_from(DB["emp"])
    emp = {}
    for elem in data:
        if elem["first_name"] == first_name and elem["last_name"] == last_name:
            if emp:
                raise Exception(f"Found multiple employees with last_name={last_name} and first_name={first_name}!")
            emp = elem

    return emp


"""
TIME FUNCTIONS
"""

def add_time(emp_id:int, date:tuple, hours:int, description:str, date_format:str=DATE_FORMAT):
    # date = (YYYY, MM, DD)
    date = date_format.replace("%Y", str(date[0])).replace("%m", str(date[1])).replace("%d", str(date[2]))

    data = read_from(DB["time"])
    data.append({"emp_id": emp_id,
                 "date": date,
                 "hours": hours,
                 "description": description})
    write_to(DB["time"], data)

def get_times_by_emp_id(emp_id:int) -> list[dict]:
    return [i for i in read_from(DB["time"]) if i["emp_id"] == emp_id]

def get_times_by_date(date:tuple) -> list[dict]:
    return [i for i in read_from(DB["time"]) if i["date"] == date]
    
