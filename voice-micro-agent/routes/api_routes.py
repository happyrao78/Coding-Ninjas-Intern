from fastapi import APIRouter
from services.twilio_service import make_faq_outbound_call , make_info_outbound_call

api_router = APIRouter()

@api_router.get("/make-faq-call")
def trigger_faq_call():
    """Triggers an outbound call"""
    result = make_faq_outbound_call()
    if result["success"]:
        return {"message": "Faq Call initiated successfully!", "sid": result["sid"]}
    else:
        return {"message": "Error making faq call", "error": result["error"]}
    
@api_router.get("/make-info-call")
def trigger_info_call():
    """Triggers an outbound call"""
    result = make_info_outbound_call()
    if result["success"]:
        return {"message": "Info Call initiated successfully!", "sid": result["sid"]}
    else:
        return {"message": "Error making info call", "error": result["error"]}