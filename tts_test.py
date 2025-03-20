from gtts import gTTS
from deep_translator import GoogleTranslator
import base64
from io import BytesIO

# ✅ Example Text
text = "Apple faces greater scrutiny."

# ✅ Translate to Hindi
translated_text = GoogleTranslator(source='en', target='hi').translate(text)
print(f"✅ Translated Text: {translated_text}")

# ✅ Convert to Speech
tts = gTTS(translated_text, lang='hi')
audio_fp = BytesIO()
tts.write_to_fp(audio_fp)
audio_fp.seek(0)

# ✅ Encode Audio to Base64
audio_base64 = base64.b64encode(audio_fp.read()).decode("utf-8")
print(f"✅ Audio Base64: {audio_base64[:100]}... (truncated)")
