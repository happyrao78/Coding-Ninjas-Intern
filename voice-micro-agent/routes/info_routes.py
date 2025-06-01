from fastapi import APIRouter, Request
from fastapi.responses import Response
from twilio.twiml.voice_response import VoiceResponse, Gather
import urllib.parse
from services.translation_service import translate_to_english
from services.data_service import save_user_data_to_csv, save_user_data_to_sheet
from utils.formatters import format_email, format_blood_group


voice_router = APIRouter()

@voice_router.post("/voice-info")
async def voice(request: Request):
    try:
        params = dict(request.query_params)
        attempt = int(params.get("attempt", 1))

        response = VoiceResponse()
        gather = Gather(
            input="speech",
            action=f"/handle-info-name?attempt={attempt}",
            method="POST",
            timeout=5,
            language="hi-IN"
        )
        gather.say(
            "<speak><prosody rate='fast'>नमस्ते! मैं sankalpiq फाउंडेशन से बात कर rahi हूँ। कृपया अपना नाम बताइए।</prosody></speak>",
            voice="Polly.Aditi",
            language="hi-IN",
            ssml=True
        )
        response.append(gather)

        # Fallback if no input is received after Gather
        response.redirect(f"/handle-info-name?attempt={attempt}")
        
        return Response(content=str(response), media_type="application/xml")
    except Exception as e:
        print(f"Error in voice endpoint: {e}")
        response = VoiceResponse()
        response.say("Sorry, there was an error with the application.")
        return Response(content=str(response), media_type="application/xml")

@voice_router.post("/handle-info-name")
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
            response.redirect(f"/voice-email?name={encoded_name}")
        elif attempt < 2:
            response.say(
                "<speak><prosody rate='fast'>माफ कीजिए, हमें आपकी आवाज़ सुनाई नहीं दी। एक बार फिर कोशिश करते हैं।</prosody></speak>",
                voice="Polly.Aditi",
                language="hi-IN",
                ssml=True
            )
            response.redirect(f"/voice-info?attempt={attempt + 1}")
        else:
            response.say(
                "<speak><prosody rate='fast'>हमें आपका नाम नहीं मिला। कॉल समाप्त की जा रही है। फाउंडेशन से संपर्क करने के लिए धन्यवाद।</prosody></speak>",
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

@voice_router.post("/voice-email")
async def voice_email(request: Request):
    try:
        name = request.query_params.get("name", "")
        name = urllib.parse.unquote(name)

        response = VoiceResponse()
        gather = Gather(
            input="speech",
            action=f"/handle-email?name={urllib.parse.quote(name)}",
            method="POST",
            timeout=5,
            language="hi-IN"
        )
        gather.say(
            f"<speak><prosody rate='fast'>धन्यवाद {name}। humari फाउंडेशन के साथ जुड़ने के लिए, कृपया अपना ईमेल पता बताइए।</prosody></speak>",
            voice="Polly.Aditi",
            language="hi-IN",
            ssml=True
        )
        response.append(gather)
        response.redirect(f"/handle-email?name={urllib.parse.quote(name)}")

        return Response(content=str(response), media_type="application/xml")
    except Exception as e:
        print(f"Error in voice-email endpoint: {e}")
        response = VoiceResponse()
        response.say("Sorry, there was an error with the application.")
        return Response(content=str(response), media_type="application/xml")

@voice_router.post("/handle-email")
async def handle_email(request: Request):
    try:
        form_data = await request.form()
        email = form_data.get("SpeechResult", "")
        name = urllib.parse.unquote(request.query_params.get("name", ""))

        response = VoiceResponse()

        if email:
             translated_email = translate_to_english(email)
             formatted_email = format_email(translated_email)
             print(f"User's email: {translated_email} (Original: {email})")
             print(f"Formatted email: {formatted_email}")
             response.redirect(f"/voice-blood?name={urllib.parse.quote(name)}&email={urllib.parse.quote(email)}")
        else:
            response.say(
                f"<speak><prosody rate='fast'>{name}, माफ कीजिए, ईमेल नहीं मिला। कॉल समाप्त की जा रही है। फाउंडेशन से संपर्क करने के लिए धन्यवाद।</prosody></speak>",
                voice="Polly.Aditi", language="hi-IN", ssml=True
            )
            response.hangup()

        return Response(content=str(response), media_type="application/xml")
    except Exception as e:
        print(f"Error in handle-email endpoint: {e}")
        response = VoiceResponse()
        response.say("Sorry, there was an error with the application.")
        return Response(content=str(response), media_type="application/xml")

@voice_router.post("/voice-blood")
async def voice_blood(request: Request):
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
            f"<speak><prosody rate='fast'>शुक्रिया {name}! कृपया अपना blood group बताइए। यह जानकारी फाउंडेशन के पास सुरक्षित रहेगी।</prosody></speak>",
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

@voice_router.post("/handle-blood")
async def handle_blood(request: Request):
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
                f"<speak><prosody rate='fast'>धन्यवाद {name}, आपकी जानकारी प्फाउंडेशन में सुरक्षित कर ली गई है। हमारी टीम जल्द ही आपसे संपर्क करेगी। आपके सहयोग के लिए हार्दिक आभार।</prosody></speak>",
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
                f"<speak><prosody rate='fast'>{name}, रक्त समूह प्राप्त नहीं हुआ, फिर भी आपकी जानकारी हमारे पास सुरक्षित है। प्रीरित फाउंडेशन से जुड़ने के लिए धन्यवाद।</prosody></speak>",
                voice="Polly.Aditi", language="hi-IN", ssml=True
            )
            response.hangup()

        return Response(content=str(response), media_type="application/xml")
    except Exception as e:
        print(f"Error in handle-blood endpoint: {e}")
        response = VoiceResponse()
        response.say("Sorry, there was an error with the application.")
        return Response(content=str(response), media_type="application/xml")



