import asyncio
import time
from fastapi import FastAPI, BackgroundTasks, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional

from sheets_client import GoogleSheetsClient
from whatsapp_client import WhatsAppClient
from gemini_client import GeminiClient
from config import settings

app = FastAPI(title="WhatsApp Message Automation")

# Initialize clients
sheets_client = GoogleSheetsClient() 
whatsapp_client = WhatsAppClient() 
gemini_client = GeminiClient() 

# Flag to track if message processing is already running
is_processing = False

class MessageRequest(BaseModel): 
    phone: str
    ngo_name: str
    custom_message: Optional[str] = None 

class BulkProcessRequest(BaseModel): 
    force: bool = False

@app.on_event("startup")
async def startup_event():
    """Initialize services on startup"""
    sheets_client.authenticate()
    gemini_client.initialize()
    
    # Start automatic processing in background
    asyncio.create_task(scheduled_processing())

@app.on_event("shutdown")
async def shutdown_event():
    """Clean up on shutdown"""
    await whatsapp_client.disconnect()


async def scheduled_processing():
    """Periodically process contacts from Google Sheets"""
    global is_processing
    
    while True:
        if not is_processing:
            # Check if there are contacts to process before setting the flag
            contacts = sheets_client.get_sheet_data()
            if contacts:
                is_processing = True
                try:
                    await process_contacts_from_sheets()
                except Exception as e:
                    print(f"Error in scheduled processing: {e}")
                finally:
                    is_processing = False
            else:
                print("No contacts to process in this cycle. Skipping.")
                
        # Wait for the next processing cycle
        await asyncio.sleep(settings.processing_interval)

async def process_contacts_from_sheets():
    """Process all contacts from Google Sheets"""
    # First, fetch contacts
    contacts = sheets_client.get_sheet_data()
    print(f"Found {len(contacts)} contacts to process")
    
    # Check if there are any contacts to process
    if not contacts:
        print("No contacts to process. Skipping WhatsApp initialization.")
        return
    
    # Only initialize WhatsApp if there are contacts to process
    if not whatsapp_client.is_initialized:
        await whatsapp_client.initialize()
        if not whatsapp_client.is_initialized:
            print("Failed to initialize WhatsApp client")
            return
    
    # Use our custom message instead of Gemini
    whatsapp_client.message_template = settings.custom_message
    
    for contact in contacts:
        ngo_name = contact.get("ngo_name", "")
        phone = contact.get("phone", "")
        row_index = contact.get("row_index")
        
        if not phone:
            continue
            
        try:
            # Send the message using the already initialized client
            result = await whatsapp_client.send_message(phone, ngo_name)
            
            # Update status in the sheet
            if result["success"]:
                sheets_client.update_status(row_index, "Sent")
            else:
                sheets_client.update_status(row_index, f"Failed: {result.get('reason', 'Unknown error')}")
                
            # Wait a bit between messages to avoid rate limiting
            await asyncio.sleep(2)
        except Exception as e:
            print(f"Error processing contact {ngo_name} ({phone}): {e}")
            sheets_client.update_status(row_index, f"Error: {str(e)[:50]}")

@app.get("/")
def read_root():
    return {"status": "active", "message": "WhatsApp Message Automation API is running"}

@app.get("/status")
def get_status():
    return {
        "is_processing": is_processing,
        "whatsapp_initialized": whatsapp_client.is_initialized,
        "gemini_initialized": gemini_client.initialized
    }

@app.post("/send")
async def send_message(request: MessageRequest):
    """Send a WhatsApp message to a specific number"""
    if not whatsapp_client.is_initialized:
        await whatsapp_client.initialize()
        
    if not whatsapp_client.is_initialized:
        raise HTTPException(status_code=500, detail="WhatsApp client not initialized")
    
    # Use custom message if provided in request
    message_to_use = request.custom_message if request.custom_message else settings.custom_message
    original_template = whatsapp_client.message_template
    whatsapp_client.message_template = message_to_use
        
    try:
        result = await whatsapp_client.send_message(request.phone, request.ngo_name)
        
        # Restore original template
        whatsapp_client.message_template = original_template
            
        if result["success"]:
            return {"status": "success", "message": "Message sent successfully"}
        else:
            return {"status": "error", "message": result.get("reason", "Failed to send message")}
    except Exception as e:
        # Restore original template in case of error
        whatsapp_client.message_template = original_template
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/process")
async def process_contacts(background_tasks: BackgroundTasks, request: BulkProcessRequest = BulkProcessRequest()):
    """Manually trigger processing of contacts from Google Sheets"""
    global is_processing
    
    if is_processing and not request.force:
        return {"status": "busy", "message": "Processing is already running"}
    
    if request.force:
        is_processing = False
        
    background_tasks.add_task(process_contacts_background)
    return {"status": "started", "message": "Contact processing started in background"}

async def process_contacts_background():
    """Background task for processing contacts"""
    global is_processing
    
    if is_processing:
        return
        
    is_processing = True
    try:
        await process_contacts_from_sheets()
    finally:
        is_processing = False

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)