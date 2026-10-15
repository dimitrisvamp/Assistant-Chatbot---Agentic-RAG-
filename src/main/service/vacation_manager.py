from openpyxl import Workbook, load_workbook 
from openpyxl.worksheet.worksheet import Worksheet
from collections import defaultdict

unsuccessful_requests = []
def save_vacation_request(month: str, employee_name: str, start_date: int, end_date: int) -> str:
    """Save the vacation request in the excel file

    Args:
        vacation_excel (_type_): vacation excel file
        month_sheet (_type_): month sheet in the excel file
        employee_name (_type_): name of the employee
        start_date (_type_): start date of the vacation
        end_date (_type_): end date of the vacation
    """
    vacation_excel, month_sheet = load_vacation_excel(month)
    availability = check_vacation_request_availability(month_sheet, employee_name, start_date, end_date)
    if availability:  
        for day in range(start_date, end_date + 1):
            excel_row_number, employee_row = find_employee_row(month_sheet, employee_name)
            month_sheet.cell(row=excel_row_number, column=day + 1, value="X")
        vacation_excel.save("main/resources/documents/Vacation Planner.xlsx")
        return f"{employee_name}, I have saved successfully your vacation request."
    else:
        
        return unsuccessful_requests[0]
        
def check_vacation_request_availability(month_sheet: Worksheet, employee_name: str, start_date: int, end_date: int) -> bool:
    """Check if the vacation request is available for the employee

    Args:
        vacation_excel (_type_): vacation excel file
    """
    excel_row_number, employee_row = find_employee_row(month_sheet, employee_name)
    availability = defaultdict(list)
    unsuccessful_requests.clear()
    if employee_row is None:
        unsuccessful_requests.append(f"Employee {employee_name} not found in the vacation excel file.")
        return False
    else:
        for row in month_sheet.iter_rows(min_row=2, values_only=True):
            for day in range(start_date, end_date + 1):
                excel_name = str(row[0]).strip().lower()
                if excel_name == employee_name.strip().lower() and row[day] == "X":
                    unsuccessful_requests.append(f"You have already requested vacation for {day} of {month_sheet.title}.")
                    return False
                else:
                    if row[day] == "X":
                        availability[day].append(row[0])
        for day,employees in availability.items():
            if len(availability[day]) >= 2:
                unsuccessful_requests.append(f"You cannot request vacation for {day} of {month_sheet.title} as there are already 2 employees on vacation.")
                return False
        return True
    
def find_employee_row(month_sheet, employee_name):
    """Find the row of the employee in the vacation excel file

    Args:
        vacation_excel (_type_): vacation excel file
        employee_name (_type_): name of the employee

    Returns:
        _type_: row of the employee in the vacation excel file
    """
    employee_name = employee_name.strip().lower()
    for row_number, row in enumerate(month_sheet.iter_rows(min_row=2, values_only=True), start=2):
        excel_name = str(row[0]).strip().lower()
        if excel_name == employee_name:
            return (row_number, row)
    return None, None

def load_vacation_excel(month: str) -> Workbook:
    """Load the vacation excel file
    """
    vacation_excel = load_workbook("main/resources/documents/Vacation Planner.xlsx")
    month_sheet = vacation_excel[month]
    return vacation_excel, month_sheet