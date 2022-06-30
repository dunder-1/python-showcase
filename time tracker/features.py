import json
from datetime import datetime, date

DB = {"emp": "db/employees.json", "time": "db/times.json"}
DATE_FORMAT = "%Y/%m/%d"

def read_from(db_name:str, format_func=None) -> list[dict]:
    data = []
    with open(db_name, "r", encoding="utf-8") as file:
        for elem in json.load(file):
            if format_func:
                elem = format_func(elem)
            data.append(elem)
    return data

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

def add_time(emp_id:int, date:date, hours:int, description:str, date_format:str=DATE_FORMAT):
    data = read_from(DB["time"])
    data.append({"emp_id": emp_id,
                 "date": date.isoformat(),
                 "hours": hours,
                 "description": description})
    write_to(DB["time"], data)

def str_to_date(elem:dict) -> date:
    elem["date"] = date.fromisoformat(elem["date"])
    return elem

def get_times_by_emp_id(emp_id:int) -> list[dict]:
    return [i for i in read_from(DB["time"], format_func=str_to_date) if i["emp_id"] == emp_id]

def get_times_by_date(date:tuple) -> list[dict]:
    return [i for i in read_from(DB["time"], format_func=str_to_date) if i["date"] == date]
    
def get_times_by_week(emp_id:int, week:int, get_sum=False) -> list[dict]:
    data = []
    for elem in read_from(DB["time"], format_func=str_to_date):
        if elem["emp_id"] == emp_id and elem["date"].strftime("%W") == str(week):
            data.append(elem)
    return data