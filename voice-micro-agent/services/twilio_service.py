from twilio.rest import Client
from config.settings import settings

# Initialize Twilio client
client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

def make_faq_outbound_call():
    """Make an outbound call using Twilio"""
    try:
        call = client.calls.create(
            to=settings.TO_NUMBER,
            from_=settings.TWILIO_PHONE_NUMBER,
            url=f"{settings.WEBHOOK_URL}/voice-faq"
        )
        return {"success": True, "sid": call.sid}
    except Exception as e:
        print(f"Error making call: {e}")
        return {"success": False, "error": str(e)}
    
def make_info_outbound_call():
    """Make an outbound call using Twilio"""
    try:
        call = client.calls.create(
            to=settings.TO_NUMBER,
            from_=settings.TWILIO_PHONE_NUMBER,
            url=f"{settings.WEBHOOK_URL}/voice-info"
        )
        return {"success": True, "sid": call.sid}
    except Exception as e:
        print(f"Error making call: {e}")
        return {"success": False, "error": str(e)}