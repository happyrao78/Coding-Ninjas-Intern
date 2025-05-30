from fastapi import FastAPI, Request
from fastapi.responses import Response
from twilio.twiml.voice_response import VoiceResponse, Gather
import urllib.parse
import sys
from dotenv import load_dotenv
import os
from sheets_integration import *
from agent import *

# Set console encoding to UTF-8 to properly display Hindi characters
sys.stdout.reconfigure(encoding='utf-8')
 
load_dotenv()
app = FastAPI()

# Get Twilio numbers from environment variables
from_number = os.getenv("TWILIO_PHONE_NUMBER")
to_number = os.getenv("TO_NUMBER")

# Define your webhook URL (will need to be updated when deployed)
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

@app.get("/")
def read_root():
    return {"status": "Calling agent server is running"}

@app.get("/make-call")
def make_call():
    """Triggers a call from Twilio number to your number"""
    try: 
        call = client.calls.create(
            to=to_number,
            from_=from_number,
            url=f"{WEBHOOK_URL}/voice"
        )
        return {"message": "llm-server Call initiated to Happy Yadav!", "sid": call.sid}
    except Exception as e:
        print(f"Error making call: {e}")
        return {"message": "Error making call", "error": str(e)}

@app.post("/voice")
async def voice(request: Request):
    try:
        params = dict(request.query_params)
        attempt = int(params.get("attempt", 1))

        response = VoiceResponse()
        gather = Gather(
            input="speech",
            action=f"/handle-name?attempt={attempt}",
            method="POST",
            timeout=5,
            language="hi-IN"
        )
        gather.say(
            "<speak><prosody rate='fast'>नमस्ते! मैं Happy Yadav baat kr rha hu। कृपया अपना नाम बताइए।</prosody></speak>",
            voice="Polly.Aditi",
            language="hi-IN",
            ssml=True
        )
        response.append(gather)

        # Fallback if no input is received after Gather
        response.redirect(f"/handle-name?attempt={attempt}")
        
        return Response(content=str(response), media_type="application/xml")
    except Exception as e:
        print(f"Error in voice endpoint: {e}")
        response = VoiceResponse()
        response.say("Sorry, there was an error with the application.")
        return Response(content=str(response), media_type="application/xml")

@app.post("/handle-name")
async def handle_name(request: Request):
    try:
        form_data = await request.form()
        speech_result = form_data.get("SpeechResult", "")
        attempt = int(request.query_params.get("attempt", 1))

        response = VoiceResponse()

        if speech_result:
            translated_name = translate_to_english(speech_result)
            print(f"User's name: {translated_name} (Original: {speech_result})")
            
            # URL encode the name to avoid issues with special characters
            encoded_name = urllib.parse.quote(speech_result)
            response.redirect(f"/voice-question?name={encoded_name}")
        elif attempt < 2:
            response.say(
                "<speak><prosody rate='fast'>माफ कीजिए, हमें आपकी आवाज़ सुनाई नहीं दी। एक बार फिर कोशिश करते हैं।</prosody></speak>",
                voice="Polly.Aditi",
                language="hi-IN",
                ssml=True
            )
            response.redirect(f"/voice?attempt={attempt + 1}")
        else:
            response.say(
                "<speak><prosody rate='fast'>हमें आपका नाम नहीं मिला। कॉल समाप्त की जा रही है।संपर्क करने के लिए धन्यवाद।</prosody></speak>",
                voice="Polly.Aditi",
                language="hi-IN",
                ssml=True
            )
            response.hangup()

        return Response(content=str(response), media_type="application/xml")
    except Exception as e:
        print(f"Error in handle-name endpoint: {e}")
        response = VoiceResponse()
        response.say("Sorry, there was an error with the application.")
        return Response(content=str(response), media_type="application/xml")

@app.post("/voice-question")
async def voice_question(request: Request):
    try:
        name = urllib.parse.unquote(request.query_params.get("name", ""))
        email = urllib.parse.unquote(request.query_params.get("email", ""))
        blood_group = urllib.parse.unquote(request.query_params.get("blood_group", ""))

        response = VoiceResponse()
        gather = Gather(
            input="speech",
            action=f"/handle-question?name={urllib.parse.quote(name)}&email={urllib.parse.quote(email)}&blood_group={urllib.parse.quote(blood_group)}",
            method="POST",
            timeout=10,
            language="hi-IN"
        )
        gather.say(
            f"<speak><prosody rate='fast'>{name}, अब आप कोई भी जानकारी के लिए अपना सवाल पूछ सकते हैं। मैं आपकी मदद करने की कोशिश करूंगा।</prosody></speak>",
            voice="Polly.Aditi",
            language="hi-IN",
            ssml=True
        )
        response.append(gather)
        # If no input is received after Gather, go to thank you and end call
        response.redirect(f"/thank-you?name={urllib.parse.quote(name)}")

        return Response(content=str(response), media_type="application/xml")
    except Exception as e:
        print(f"Error in voice-question endpoint: {e}")
        response = VoiceResponse()
        response.say("Sorry, there was an error with the application.")
        return Response(content=str(response), media_type="application/xml")

@app.post("/handle-question")
async def handle_question(request: Request):
    try:
        form_data = await request.form()
        question = form_data.get("SpeechResult", "")
        name = urllib.parse.unquote(request.query_params.get("name", ""))
        
        response = VoiceResponse()

        if question:
            translated_question = translate_to_english(question)
            print(f"User's question: {translated_question} (Original: {question})")
            
            # Get answer from Gemini
            answer = await get_gemini_response(translated_question)
            translated_response = translate_to_english(answer)
            print(f"AI response: {translated_response}")
            
            # Answer the question
            response.say(
                f"<speak><prosody rate='fast'>{answer}</prosody></speak>",
                voice="Polly.Aditi",
                language="hi-IN",
                ssml=True
            )
            
            # Ask if they have another question
            gather = Gather(
                input="speech",
                action=f"/handle-more-questions?name={urllib.parse.quote(name)}",
                method="POST",
                timeout=5,
                language="hi-IN"
            )
            gather.say(
                f"<speak><prosody rate='fast'>क्या आप कोई और सवाल पूछना चाहते हैं? हां या ना में जवाब दें।</prosody></speak>",
                voice="Polly.Aditi",
                language="hi-IN",
                ssml=True
            )
            response.append(gather)
            # If no input is received after Gather, go to thank you
            response.redirect(f"/thank-you?name={urllib.parse.quote(name)}")
        else:
            response.redirect(f"/thank-you?name={urllib.parse.quote(name)}")

        return Response(content=str(response), media_type="application/xml")
    except Exception as e:
        print(f"Error in handle-question endpoint: {e}")
        response = VoiceResponse()
        response.say("Sorry, there was an error with the application.")
        return Response(content=str(response), media_type="application/xml")

@app.post("/handle-more-questions")
async def handle_more_questions(request: Request):
    try:
        form_data = await request.form()
        answer = form_data.get("SpeechResult", "").lower()
        name = urllib.parse.unquote(request.query_params.get("name", ""))
        
        response = VoiceResponse()
        
        # Check if user wants to ask more questions
        if answer and ("हां" in answer or "yes" in answer or "ha" in answer):
            response.redirect(f"/voice-question?name={urllib.parse.quote(name)}")
        else:
            response.redirect(f"/thank-you?name={urllib.parse.quote(name)}")
            
        return Response(content=str(response), media_type="application/xml")
    except Exception as e:
        print(f"Error in handle-more-questions endpoint: {e}")
        response = VoiceResponse()
        response.say("Sorry, there was an error with the application.")
        return Response(content=str(response), media_type="application/xml")

@app.post("/thank-you")
async def thank_you(request: Request):
    try:
        name = urllib.parse.unquote(request.query_params.get("name", ""))
        
        response = VoiceResponse()
        response.say(
            f"<speak><prosody rate='fast'>{name}आपका समय देने के लिए धन्यवाद। हैप्पी यादव जल्द ही आपसे संपर्क करेगी। Bolo जय जय कोडिंग निंजास</prosody></speak>", 
            voice="Polly.Aditi",
            language="hi-IN",
            ssml=True 
        ) 
        response.hangup()
        
        return Response(content=str(response), media_type="application/xml")
    except Exception as e:
        print(f"Error in thank-you endpoint: {e}")
        response = VoiceResponse()
        response.say("Sorry, there was an error with the application.")
        return Response(content=str(response), media_type="application/xml")

@app.get("/healthcheck")
def healthcheck():
    """Simple endpoint to check if the server is running"""
    return {"status": "healthy", "message": "Prerit Foundation Call Agent is operational"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("app:app", host="0.0.0.0", port=port, reload=True)