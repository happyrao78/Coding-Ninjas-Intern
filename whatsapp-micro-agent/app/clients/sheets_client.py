import gspread
from oauth2client.service_account import ServiceAccountCredentials

from app.config import settings

class GoogleSheetsClient:
    def __init__(self):
        self.creds_file = settings.google_sheets_credentials_file
        self.sheet_id = settings.google_sheet_id
        self.worksheet_name = settings.worksheet_name
        self.client = None
        self.sheet = None
    
    def authenticate(self):
        """Authenticate with Google Sheets API"""
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        credentials = ServiceAccountCredentials.from_json_keyfile_name(self.creds_file, scope)
        self.client = gspread.authorize(credentials)
        
    def get_sheet_data(self):
        """Fetch data from the Google Sheet"""
        if not self.client:
            self.authenticate()
         
        try:
            spreadsheet = self.client.open_by_key(self.sheet_id)
            all_worksheets = [sheet.title for sheet in spreadsheet.worksheets()]
            print(f"Available worksheets: {all_worksheets}")
            worksheet = spreadsheet.worksheet(self.worksheet_name)
            
            # Get all records
            records = worksheet.get_all_records()
            
            # Extract NGO name and phone number
            contacts = []
            for record in records:
                if "Client Name" in record and "Phone" in record:
                    ngo_name = record["Client Name"]
                    phone = record["Phone"]
                    status = record.get("Status", "")
                    
                    # Only include entries with valid phone numbers and not already processed
                    if phone and status != "Sent":
                        contacts.append({
                            "ngo_name": ngo_name,
                            "phone": phone,
                            "row_index": records.index(record) + 2  # +2 for header row and 0-indexing
                        })
             
            return contacts
        except Exception as e:
            print(f"Error fetching data from Google Sheets: {e}")
            return []
    
    def update_status(self, row_index, status="Sent"):
        """Update the status column for a processed contact"""
        if not self.client:
            self.authenticate()
            
        try:
            spreadsheet = self.client.open_by_key(self.sheet_id)
            worksheet = spreadsheet.worksheet(self.worksheet_name)
            
            # Find the column index for "Status"
            header_row = worksheet.row_values(1)
            status_col_idx = header_row.index("Status") + 1  # 1-indexed
            
            # Update the cell
            worksheet.update_cell(row_index, status_col_idx, status)
            return True
        except Exception as e:
            print(f"Error updating status in Google Sheets: {e}")
            return False