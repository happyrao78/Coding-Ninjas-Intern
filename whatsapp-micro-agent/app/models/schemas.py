from pydantic import BaseModel
from typing import Optional

class MessageRequest(BaseModel):
    """Request model for sending individual messages"""
    phone: str
    ngo_name: str
    custom_message: Optional[str] = None

class BulkProcessRequest(BaseModel):
    """Request model for bulk processing"""
    force: bool = False

class MessageResponse(BaseModel):
    """Response model for message operations"""
    success: bool
    reason: Optional[str] = None

class StatusResponse(BaseModel):
    """Response model for system status"""
    is_processing: bool
    whatsapp_initialized: bool
    gemini_initialized: bool

class ContactData(BaseModel):
    """Model for contact information from sheets"""
    ngo_name: str
    phone: str
    row_index: int