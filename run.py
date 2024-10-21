import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('workday-pay-sheet')


def get_colleague_sheet():
    """
    Gets the sheet for a specific colleague from user input.
    Validates if the sheet exists.
    """
    while True:  # Loop until valid input is provided
        print("Please enter colleague's name or sheet required: ")
        colleague = input("Name: \n").capitalize()

        try:
            # Try to access the worksheet by name
            sheet = SHEET.worksheet(colleague)
            print(f"Successfully loaded sheet for '{colleague}'.")
            return sheet

        except gspread.exceptions.WorksheetNotFound:
            print(f"Error: '{colleague}'s sheet  not found. Please try again")
        except Exception as e:
            print(f"An unexpected error occurred: {str(e)}")


def add_hours():
    """
    Adds hours worked for a colleague for a specific week.
    If the week number doesn't exist, it appends the new week with the hours.
    """
    sheet = get_colleague_sheet()
    week_num = input("Enter the week number you want to update: \n")

    try:
        week_num = int(week_num)
    except ValueError:
        print("Invalid week number. Please enter a valid number.")
        return

    print("Please enter the hours worked for each day, separated by commas.")
    hours_input = input("Enter hours (e.g., 8,8,8,8,8,0,0): \n")
    hours = hours_input.split(",")

    # Validate that exactly 7 values are provided
    if len(hours) != 7:
        print(f"Error: You must provide exactly 7 values. {len(hours)} given")
        return

    # Convert hours to floats and validate that they are numerical
    try:
        hours = [float(hour.strip()) for hour in hours]
    except ValueError:
        print("Error: Please ensure all entered hours are valid numbers.")
        return
    data = sheet.get_all_values()
    week_found = False

    for row_id, row in enumerate(data):
        if row[0] == str(week_num):
            print(f"Week number {week_num} for {sheet.title} already exists")
            week_found = True
            break

    if not week_found:
        total_hours = calculate_total_hours(hours)
        net_pay = calculate_pay(total_hours)
        new_row = [week_num] + hours + [total_hours, net_pay]
        sheet.append_row(new_row)
        print(f"Week {week_num} successfully added to the sheet {sheet.title}")
        print(f"Total hours worked: {total_hours}")
        print(f"Net pay for the week: €{net_pay}\n")


def calculate_total_hours(hours):
    """
    Calculates total hours worked for the week for a colleague.
    """
    total = 0
    for hour in hours:
        total += float(hour)
    return total


def calculate_pay(total_hours):
    """
    automatically totals net pay when new hours added
    """
    pay = total_hours * 13.8
    return round(pay, 2)


def main_menu():
    """
    Displays the main menu and handles user input to either
    call a function or exit the program.
    """
    while True:
        print("\n--- Workday Pay Management System ---")
        print("1. Add hours for a colleague")
        print("2. Get data for collegue")
        print("3. Exit")

        choice = input("Enter your choice: \n")

        if choice == '1':
            add_hours()
        elif choice == '2':
            sheet_info = get_colleague_sheet()
            print(sheet_info.get_all_values())
        elif choice == '3':
            print("Thanks for using Workday Pay Management System")
            break
        else:
            print("Invalid choice. Please enter a number from the menu")


if __name__ == "__main__":
    main_menu()
