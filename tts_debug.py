from gtts import gTTS
from deep_translator import GoogleTranslator
from io import BytesIO
import base64

def test_tts():
    text = "Apple faces greater scrutiny."  # Example text from API
    print("✅ Original Text:", text)

    try:
        translated_text = GoogleTranslator(source='en', target='hi').translate(text)
        print("✅ Translated Text:", translated_text)

        tts = gTTS(translated_text, lang='hi', slow=False)
        audio_fp = BytesIO()
        tts.write_to_fp(audio_fp)
        audio_fp.seek(0)

        audio_base64 = base64.b64encode(audio_fp.read()).decode("utf-8")
        print("✅ Audio Base64:", audio_base64[:100], "... (truncated)")
    except Exception as e:
        print("❌ TTS Failed:", str(e))

test_tts()
