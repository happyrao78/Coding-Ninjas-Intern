from googletrans import Translator

translator = Translator()

def translate_to_english(text):
    """Translate text to English"""
    try:
        translation = translator.translate(text, dest='en')
        return translation.text
    except Exception as e:
        print(f"Translation error: {e}")
        return f"{text} (translation failed)"
