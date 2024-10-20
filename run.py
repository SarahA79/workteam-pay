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

eddie = SHEET.worksheet('Eddie')
data = eddie.get_all_values()
print(data)


def get_colleague_sheet():
    """
    Gets the sheet for a specific colleague from user input.
    Validates if the sheet exists.
    """
    while True: 
        print("Please enter colleague's name: ")
        colleague = input("Name: ").capitalize()

        try:
            # Try to access the worksheet by name
            sheet = SHEET.worksheet(colleague)
            data = sheet.get_all_values()
            print(data)
            break  # Exit the loop once a valid sheet is found
        
        except gspread.exceptions.WorksheetNotFound:
            # If the worksheet is not found, prompt user again
            print(f"Error: Sheet for '{colleague}' not found. Please check your spelling and try again.")
        except Exception as e:
            #catch other errors as encountered
            print(f"An unexpected error occurred: {str(e)}")

get_colleague_sheet()