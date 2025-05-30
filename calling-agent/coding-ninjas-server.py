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
        return {"message": "Coding ninjas agent !!Call initiated to Happy Yadav!", "sid": call.sid}
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
            "<speak><prosody rate='fast'>नमस्ते! मैं Coding Ninjas से Happy Yadav baat kr rha hu। कृपया अपना नाम बताइए।</prosody></speak>",
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
            response.redirect(f"/voice-coding-ninjas?name={encoded_name}")
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
                "<speak><prosody rate='fast'>हमें आपका नाम नहीं मिला। कॉल समाप्त की जा रही है। प्रीरित फाउंडेशन से संपर्क करने के लिए धन्यवाद।</prosody></speak>",
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



    try:
        name = urllib.parse.unquote(request.query_params.get("name", ""))
        email = urllib.parse.unquote(request.query_params.get("email", ""))

        response = VoiceResponse()
        gather = Gather(
            input="speech",
            action=f"/handle-blood?name={urllib.parse.quote(name)}&email={urllib.parse.quote(email)}",
            method="POST",
            timeout=5,
            language="hi-IN"
        )
        gather.say(
            f"<speak><prosody rate='fast'>शुक्रिया {name} अब आपकी सुरक्षा के लिए, कृपया अपना blood group बताइए यह जानकारी प्रीरित फाउंडेशन के पास सुरक्षित रहेगी।</prosody></speak>",
            voice="Polly.Aditi",
            language="hi-IN",
            ssml=True
        )
        response.append(gather)
        response.redirect(f"/handle-blood?name={urllib.parse.quote(name)}&email={urllib.parse.quote(email)}")

        return Response(content=str(response), media_type="application/xml")
    except Exception as e:
        print(f"Error in voice-blood endpoint: {e}")
        response = VoiceResponse()
        response.say("Sorry, there was an error with the application.")
        return Response(content=str(response), media_type="application/xml")


    try:
        form_data = await request.form()
        blood_group = form_data.get("SpeechResult", "")
        name = urllib.parse.unquote(request.query_params.get("name", ""))
        email = urllib.parse.unquote(request.query_params.get("email", ""))

        response = VoiceResponse()

        if blood_group:
            translated_name = translate_to_english(name)
            translated_email = translate_to_english(email)
            translated_blood = translate_to_english(blood_group)

            formatted_email = format_email(translated_email)
            formatted_blood = format_blood_group(blood_group)

            print("🧑‍🤝‍🧑 User information:")
            print(f"Name: {translated_name} (Original: {name})")
            print(f"Email: {translated_email} (Original: {email})")
            print(f"Blood Group: {translated_blood} (Original: {blood_group})")
            print(f"Formatted Email: {formatted_email}")
            print(f"Formatted Blood Group: {formatted_blood}")

            # Save user data to CSV - use formatted data
            save_user_data_to_csv(translated_name, formatted_email, formatted_blood)
            save_user_data_to_sheet(translated_name, formatted_email, formatted_blood)

            response.say(
                f"<speak><prosody rate='fast'>धन्यवाद! {name} आपकी जानकारी प्रीरित फाउंडेशन में सुरक्षित कर ली गई है। हैप्पी यादव और हमारी टीम जल्द ही आपसे संपर्क करेगी। आपके सहयोग के लिए हार्दिक आभार।</prosody></speak>",
                voice="Polly.Aditi", language="hi-IN", ssml=True
            )
            response.hangup()
        else:
            # Even if blood group is not provided, save the available data
            translated_name = translate_to_english(name)
            translated_email = translate_to_english(email)
            formatted_email = format_email(translated_email)
            
            # Save user data to CSV with empty blood group
            save_user_data_to_csv(translated_name, formatted_email, "")
            save_user_data_to_sheet(translated_name, formatted_email, "")

            response.say(
                f"<speak><prosody rate='fast'>{name} जी, रक्त समूह प्राप्त नहीं हुआ, फिर भी आपकी जानकारी हमारे पास सुरक्षित है। प्रीरित फाउंडेशन से जुड़ने के लिए धन्यवाद।</prosody></speak>",
                voice="Polly.Aditi", language="hi-IN", ssml=True
            )
            response.hangup()

        return Response(content=str(response), media_type="application/xml")
    except Exception as e:
        print(f"Error in handle-blood endpoint: {e}")
        response = VoiceResponse()
        response.say("Sorry, there was an error with the application.")
        return Response(content=str(response), media_type="application/xml")


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

@app.post("/voice-coding-ninjas")
async def voice_coding_ninjas(request: Request):
    """Endpoint for introducing the Coding Ninjas bot and gathering user query"""
    try:
        name = urllib.parse.unquote(request.query_params.get("name", ""))
        email = urllib.parse.unquote(request.query_params.get("email", ""))
        blood_group = urllib.parse.unquote(request.query_params.get("blood_group", ""))

        response = VoiceResponse()
        gather = Gather(
            input="speech",
            action=f"/handle-coding-question?name={urllib.parse.quote(name)}&email={urllib.parse.quote(email)}&blood_group={urllib.parse.quote(blood_group)}",
            method="POST",
            timeout=10,
            language="hi-IN"
        )
        gather.say(
            f"<speak><prosody rate='fast'>नमस्ते {name} मैं निनजा बॉट बोल RAHI हूँ। मुझे हैप्पी यादव ने बनाया है। आप कोडिंग निंजास क्लब के बारे में क्या जानना चाहते हैं?</prosody></speak>",
            voice="Polly.Aditi",
            language="hi-IN",
            ssml=True
        )
        response.append(gather)
        # If no input is received after Gather, go to thank you and end call
        response.redirect(f"/thank-you?name={urllib.parse.quote(name)}")

        return Response(content=str(response), media_type="application/xml")
    except Exception as e:
        print(f"Error in voice-coding-ninjas endpoint: {e}")
        response = VoiceResponse()
        response.say("Sorry, there was an error with the application.")
        return Response(content=str(response), media_type="application/xml")

# New handler for coding questions
@app.post("/handle-coding-question")
async def handle_coding_question(request: Request):
    """Handler for user queries about Coding Ninjas"""
    try:
        form_data = await request.form()
        question = form_data.get("SpeechResult", "")
        name = urllib.parse.unquote(request.query_params.get("name", ""))
        
        response = VoiceResponse()

        if question:
            translated_question = translate_to_english(question)
            print(f"User's question: {translated_question} (Original: {question})")
            
            # Get answer from Gemini using knowledge base
            answer = await get_knowledge_base_response(translated_question)
            translated_response = translate_to_english(answer)
            print(f"Knowledge base AI response: {translated_response}")
            
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
                action=f"/handle-more-coding-questions?name={urllib.parse.quote(name)}",
                method="POST",
                timeout=5,
                language="hi-IN"
            )
            gather.say(
                f"<speak><prosody rate='fast'>क्या आप कोडिंग निंजास के बारे में कोई और सवाल पूछना चाहते हैं, ha ya na?</prosody></speak>",
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
        print(f"Error in handle-coding-question endpoint: {e}")
        response = VoiceResponse()
        response.say("Sorry, there was an error with the application.")
        return Response(content=str(response), media_type="application/xml")

# New handler for follow-up coding questions
@app.post("/handle-more-coding-questions")
async def handle_more_coding_questions(request: Request):
    """Handler for follow-up questions about Coding Ninjas"""
    try:
        form_data = await request.form()
        answer = form_data.get("SpeechResult", "").lower()
        name = urllib.parse.unquote(request.query_params.get("name", ""))
        
        response = VoiceResponse()
         
        # Check if user wants to ask more questions
        if answer and ("हां" in answer or "yes" in answer or "ha" in answer):
            response.redirect(f"/voice-coding-ninjas?name={urllib.parse.quote(name)}")
        else:
            response.redirect(f"/thank-you?name={urllib.parse.quote(name)}")
            
        return Response(content=str(response), media_type="application/xml")
    except Exception as e:
        print(f"Error in handle-more-coding-questions endpoint: {e}")
        response = VoiceResponse()
        response.say("Sorry, there was an error with the application.")
        return Response(content=str(response), media_type="application/xml")

# New endpoint for thank you message
@app.post("/thank-you")
async def thank_you(request: Request):
    try:
        name = urllib.parse.unquote(request.query_params.get("name", ""))
        
        response = VoiceResponse()
        response.say(
            f"<speak><prosody rate='fast'>{name}आपका समय देने के लिए धन्यवाद। हैप्पी यादव जल्द ही आपसे संपर्क karege। Bolo जय जय कोडिंग निंजास</prosody></speak>", 
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