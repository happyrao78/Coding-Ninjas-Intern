import asyncio
from fastapi import FastAPI, BackgroundTasks, HTTPException

from app.config import settings
from app.clients.sheets_client import GoogleSheetsClient
from app.clients.whatsapp_client import WhatsAppClient
from app.clients.gemini_client import GeminiClient
from app.models.schemas import MessageRequest, BulkProcessRequest
from app.services.message_service import MessageService

app = FastAPI(title="WhatsApp Message Automation")

# Initialize clients
sheets_client = GoogleSheetsClient()
whatsapp_client = WhatsAppClient()
gemini_client = GeminiClient()

# Initialize service
message_service = MessageService(sheets_client, whatsapp_client, gemini_client)

# Flag to track if message processing is already running
is_processing = False

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
                    await message_service.process_contacts_from_sheets()
                except Exception as e:
                    print(f"Error in scheduled processing: {e}")
                finally:
                    is_processing = False
            else:
                print("No contacts to process in this cycle. Skipping.")
                
        # Wait for the next processing cycle
        await asyncio.sleep(settings.processing_interval)

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
    
    try:
        result = await message_service.send_single_message(
            request.phone, 
            request.ngo_name, 
            request.custom_message
        )
            
        if result["success"]:
            return {"status": "success", "message": "Message sent successfully"}
        else:
            return {"status": "error", "message": result.get("reason", "Failed to send message")}
    except Exception as e:
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
        await message_service.process_contacts_from_sheets()
    finally:
        is_processing = False

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)