import asyncio
from typing import Dict, Any, Optional

from app.config import settings
from app.clients.sheets_client import GoogleSheetsClient
from app.clients.whatsapp_client import WhatsAppClient
from app.clients.gemini_client import GeminiClient

class MessageService:
    """Service class to handle message processing business logic"""
    
    def __init__(self, sheets_client: GoogleSheetsClient, whatsapp_client: WhatsAppClient, gemini_client: GeminiClient):
        self.sheets_client = sheets_client
        self.whatsapp_client = whatsapp_client
        self.gemini_client = gemini_client
    
    async def process_contacts_from_sheets(self) -> None:
        """Process all contacts from Google Sheets"""
        # First, fetch contacts
        contacts = self.sheets_client.get_sheet_data()
        print(f"Found {len(contacts)} contacts to process")
        
        # Check if there are any contacts to process
        if not contacts:
            print("No contacts to process. Skipping WhatsApp initialization.")
            return
        
        # Only initialize WhatsApp if there are contacts to process
        if not self.whatsapp_client.is_initialized:
            await self.whatsapp_client.initialize()
            if not self.whatsapp_client.is_initialized:
                print("Failed to initialize WhatsApp client")
                return
        
        # Use our custom message instead of Gemini
        self.whatsapp_client.message_template = settings.custom_message
        
        for contact in contacts:
            ngo_name = contact.get("ngo_name", "")
            phone = contact.get("phone", "")
            row_index = contact.get("row_index")
            
            if not phone:
                continue
                
            try:
                # Send the message using the already initialized client
                result = await self.whatsapp_client.send_message(phone, ngo_name)
                
                # Update status in the sheet
                if result["success"]:
                    self.sheets_client.update_status(row_index, "Sent")
                else:
                    self.sheets_client.update_status(row_index, f"Failed: {result.get('reason', 'Unknown error')}")
                    
                # Wait a bit between messages to avoid rate limiting
                await asyncio.sleep(2)
            except Exception as e:
                print(f"Error processing contact {ngo_name} ({phone}): {e}")
                self.sheets_client.update_status(row_index, f"Error: {str(e)[:50]}")
    
    async def send_single_message(self, phone: str, ngo_name: str, custom_message: Optional[str] = None) -> Dict[str, Any]:
        """Send a single WhatsApp message"""
        # Use custom message if provided in request
        message_to_use = custom_message if custom_message else settings.custom_message
        original_template = self.whatsapp_client.message_template
        self.whatsapp_client.message_template = message_to_use
            
        try:
            result = await self.whatsapp_client.send_message(phone, ngo_name)
            return result
        except Exception as e:
            return {"success": False, "reason": str(e)}
        finally:
            # Restore original template
            self.whatsapp_client.message_template = original_template