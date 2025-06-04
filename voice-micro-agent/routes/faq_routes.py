from fastapi import APIRouter, Request
from fastapi.responses import Response
from twilio.twiml.voice_response import VoiceResponse, Gather
import urllib.parse
from services.translation_service import translate_to_english
from services.gemini_service import get_knowledge_base_response


voice_router = APIRouter()


@voice_router.post("/voice-faq")
async def voice(request: Request):
    """Initial voice endpoint"""
    try:
        params = dict(request.query_params)
        attempt = int(params.get("attempt", 1))

        response = VoiceResponse()
        gather = Gather(
            input="speech",
            action=f"/handle-name?attempt={attempt}",
            method="POST",
            timeout=5,
            language="hi-IN",
        )
        gather.say(
            "<speak><prosody rate='fast'>नमस्ते! मैं Sankalpiq Foundation से Aditi बात कर रही हूँ यह कॉल आपकी सहायता और मार्गदर्शन के लिए है कृपया अपना नाम बताइए।</prosody></speak>",
            voice="Polly.Aditi",
            language="hi-IN",
            ssml=True,
        )
        response.append(gather)
        response.redirect(f"/handle-name?attempt={attempt}")

        return Response(content=str(response), media_type="application/xml")
    except Exception as e:
        print(f"Error in voice endpoint: {e}")
        response = VoiceResponse()
        response.say("Sorry, there was an error with the application.")
        return Response(content=str(response), media_type="application/xml")


@voice_router.post("/handle-name")
async def handle_name(request: Request):
    """Handle name input"""
    try:
        form_data = await request.form()
        speech_result = form_data.get("SpeechResult", "")
        attempt = int(request.query_params.get("attempt", 1))

        response = VoiceResponse()

        if speech_result:
            translated_name = translate_to_english(speech_result)
            print(f"User's name: {translated_name} (Original: {speech_result})")

            encoded_name = urllib.parse.quote(speech_result)
            response.redirect(f"/voice-ngo?name={encoded_name}")
        elif attempt < 2:
            response.say(
                "<speak><prosody rate='fast'>माफ कीजिए, हमें आपकी आवाज़ स्पष्ट रूप से सुनाई नहीं दी एक बार फिर कोशिश करते हैं कृपया अपना नाम बताएं।</prosody></speak>",
                voice="Polly.Aditi",
                language="hi-IN",
                ssml=True,
            )
            response.redirect(f"/voice-faq?attempt={attempt + 1}")
        else:
            response.say(
                "<speak><prosody rate='fast'>हमें आपका नाम नहीं मिला। कोई बात नहीं, हम बाद में फिर से प्रयास करेंगे कॉल समाप्त की जा रही है।</prosody></speak>",
                voice="Polly.Aditi",
                language="hi-IN",
                ssml=True,
            )
            response.hangup()

        return Response(content=str(response), media_type="application/xml")
    except Exception as e:
        print(f"Error in handle-name endpoint: {e}")
        response = VoiceResponse()
        response.say("Sorry, there was an error with the application.")
        return Response(content=str(response), media_type="application/xml")


@voice_router.post("/voice-ngo")
async def voice_coding_ninjas(request: Request):
    """Coding Ninjas bot introduction"""
    try:
        name = urllib.parse.unquote(request.query_params.get("name", ""))

        response = VoiceResponse()
        gather = Gather(
            input="speech",
            action=f"/handle-faq?name={urllib.parse.quote(name)}",
            method="POST",
            timeout=10,
            language="hi-IN",
        )
        gather.say(
            f"<speak><prosody rate='fast'>नमस्ते {name} Sankalpiq Foundation एक सामाजिक संस्था है जो शिक्षा, स्वास्थ्य और महिला सशक्तिकरण के क्षेत्र में काम करती है| आप हमारे कार्यों के बारे में क्या जानना चाहेंगे?</prosody></speak>",
            voice="Polly.Aditi",
            language="hi-IN",
            ssml=True,
        )
        response.append(gather)
        response.redirect(f"/thank-you?name={urllib.parse.quote(name)}")

        return Response(content=str(response), media_type="application/xml")
    except Exception as e:
        print(f"Error in voice-coding-ninjas endpoint: {e}")
        response = VoiceResponse()
        response.say("Sorry, there was an error with the application.")
        return Response(content=str(response), media_type="application/xml")


@voice_router.post("/handle-faq")
async def handle_coding_question(request: Request):
    """Handle coding questions"""
    try:
        form_data = await request.form()
        question = form_data.get("SpeechResult", "")
        name = urllib.parse.unquote(request.query_params.get("name", ""))

        response = VoiceResponse()

        if question:
            translated_question = translate_to_english(question)
            print(f"User's question: {translated_question} (Original: {question})")

            answer = await get_knowledge_base_response(translated_question)
            print(f"AI response: {answer}")

            response.say(
                f"<speak><prosody rate='fast'>{answer}</prosody></speak>",
                voice="Polly.Aditi",
                language="hi-IN",
                ssml=True,
            )

            gather = Gather(
                input="speech",
                action=f"/handle-more-faq?name={urllib.parse.quote(name)}",
                method="POST",
                timeout=5,
                language="hi-IN",
            )
            gather.say(
                "<speak><prosody rate='fast'>क्या आप Sankalpiq Foundation के किसी अन्य कार्यक्रम के बारे में जानना चाहते हैं? कृपया हाँ या ना कहें।</prosody></speak>",
                voice="Polly.Aditi",
                language="hi-IN",
                ssml=True,
            )
            response.append(gather)
            response.redirect(f"/thank-you?name={urllib.parse.quote(name)}")
        else:
            response.redirect(f"/thank-you?name={urllib.parse.quote(name)}")

        return Response(content=str(response), media_type="application/xml")
    except Exception as e:
        print(f"Error in handle-coding-question endpoint: {e}")
        response = VoiceResponse()
        response.say("Sorry, there was an error with the application.")
        return Response(content=str(response), media_type="application/xml")


@voice_router.post("/handle-more-faq")
async def handle_more_coding_questions(request: Request):
    """Handle follow-up questions"""
    try:
        form_data = await request.form()
        answer = form_data.get("SpeechResult", "").lower()
        name = urllib.parse.unquote(request.query_params.get("name", ""))

        response = VoiceResponse()

        if answer and ("हां" in answer or "yes" in answer or "ha" in answer):
            response.redirect(f"/voice-ngo?name={urllib.parse.quote(name)}")
        else:
            response.redirect(f"/thank-you?name={urllib.parse.quote(name)}")

        return Response(content=str(response), media_type="application/xml")
    except Exception as e:
        print(f"Error in handle-more-coding-questions endpoint: {e}")
        response = VoiceResponse()
        response.say("Sorry, there was an error with the application.")
        return Response(content=str(response), media_type="application/xml")


@voice_router.post("/thank-you")
async def thank_you(request: Request):
    """Thank you and goodbye"""
    try:

        response = VoiceResponse()
        response.say(
            "<speak><prosody rate='fast'>Sankalpiq Foundation की ओर से आपका समय देने के लिए धन्यवाद</prosody></speak>",
            voice="Polly.Aditi",
            language="hi-IN",
            ssml=True,
        )
        response.hangup()

        return Response(content=str(response), media_type="application/xml")
    except Exception as e:
        print(f"Error in thank-you endpoint: {e}")
        response = VoiceResponse()
        response.say("Sorry, there was an error with the application.")
        return Response(content=str(response), media_type="application/xml")
