import csv
from datetime import datetime
from google.oauth2.service_account import Credentials
import gspread
import os
from config.settings import settings
from services.email_service import send_thank_you_email

def save_user_data_to_csv(name, email, blood_group):
    """Save user data to CSV file"""
    try:
        file_exists = os.path.exists(settings.USER_DATA_CSV)
        
        with open(settings.USER_DATA_CSV, "a", newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            
            if not file_exists:
                writer.writerow(["Name", "Email", "Blood Group", "Registration Date"])
            
            current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            writer.writerow([name, email, blood_group, current_datetime])
            
        print(f"User data saved to CSV: {name}, {email}, {blood_group}")
        
        # Send thank you email
        if '@' in email:
            send_thank_you_email(name, email, blood_group)
        
        return True
    except Exception as e:
        print(f"Error saving user data to CSV: {e}")
        return False

def initialize_google_sheets():
    """Initialize Google Sheets client"""
    try:
        scope = ['https://spreadsheets.google.com/feeds',
                'https://www.googleapis.com/auth/drive']
        
        credentials = Credentials.from_service_account_file(
            settings.GOOGLE_CREDENTIALS_FILE, 
            scopes=scope
        )
        client = gspread.authorize(credentials)
        return client
    except Exception as e:
        print(f"Error initializing Google Sheets: {e}")
        return None

def save_user_data_to_sheet(name, email, blood_group):
    """Save user data to Google Sheets"""
    try:
        client = initialize_google_sheets()
        if not client:
            return False
            
        sheet_name = "User data"
        spreadsheet = client.open(sheet_name)
        worksheet = spreadsheet.sheet1
        
        current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        worksheet.append_row([name, email, blood_group, current_datetime])
        
        print(f"User data saved to Google Sheet: {name}, {email}, {blood_group}")
        return True
    except Exception as e:
        print(f"Error saving user data to Google Sheet: {e}")
        return False