from google.oauth2.service_account import Credentials
import gspread
from datetime import datetime
import os

def initialize_sheets():
    try:
        # Define the scope
        scope = ['https://spreadsheets.google.com/feeds',
                'https://www.googleapis.com/auth/drive']

        # Path to your credentials file - replace with your actual filename
        json_file = os.path.join(os.path.dirname(__file__), 'lofty-seer-457323-p7-99057e124a49.json')
        
        # Authorize using the credentials
        credentials = Credentials.from_service_account_file(json_file, scopes=scope)
        client = gspread.authorize(credentials)
        
        # Return the client for later use
        return client
    except Exception as e:
        print(f"Error initializing Google Sheets: {e}")
        return None

def save_user_data_to_sheet(name, email, blood_group):
    try:
        # Initialize the sheets client
        client = initialize_sheets()
        if not client:
            print("Failed to initialize Google Sheets client")
            return False
            
        # Open the spreadsheet by title - replace with your sheet name
        sheet_name = "User data"
        try:
            spreadsheet = client.open(sheet_name)
        except gspread.exceptions.SpreadsheetNotFound:
            print(f"Spreadsheet '{sheet_name}' not found")
            return False
        
        # Select the first worksheet
        worksheet = spreadsheet.sheet1
        
        # Add the new user data
        current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        worksheet.append_row([name, email, blood_group, current_datetime])
        
        print(f"User data saved to Google Sheet: {name}, {email}, {blood_group}")
        return True
    except Exception as e:
        print(f"Error saving user data to Google Sheet: {e}")
        return False