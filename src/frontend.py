import streamlit as st
import requests
import matplotlib.pyplot as plt
import pandas as pd
import time
from gtts import gTTS
import base64
from io import BytesIO
from deep_translator import GoogleTranslator  # ✅ Fixed Translator

# ✅ API URLs
API_URL = "https://news-summarization-api.onrender.com/news"
COMPARE_SENTIMENT_URL = "https://news-summarization-api.onrender.com/compare_sentiment"

# ✅ Available Companies
COMPANIES = {
    "Apple": "🍏",
    "Microsoft": "💻",
    "Google": "🔍",
    "Amazon": "🛒",
    "Tesla": "🚗"
}

# ✅ Streamlit UI Config
st.set_page_config(page_title="News Analysis", page_icon="📰", layout="wide")

# ✅ Title & Selection
st.markdown("<h1 style='text-align: center; color: #0077cc;'>📰 News Summarization & Sentiment Analysis</h1>", unsafe_allow_html=True)
st.write("### Select companies to fetch and compare sentiment analysis.")
selected_companies = st.multiselect("🔎 Choose companies:", list(COMPANIES.keys()), default=["Apple"])

# ✅ Function: Convert Text to Speech (Hindi)
def text_to_speech(text):
    """Converts English text to Hindi and generates speech."""
    try:
        # ✅ Translate text to Hindi using DeepTranslator
        translated_text = GoogleTranslator(source='en', target='hi').translate(text)
        
        # ✅ Convert to Speech (Add `slow=False`)
        tts = gTTS(translated_text, lang='hi', slow=False)  
        audio_fp = BytesIO()
        tts.write_to_fp(audio_fp)
        audio_fp.seek(0)

        return audio_fp
    except Exception as e:
        st.error(f"⚠️ Error in Text-to-Speech: {e}")
        return None


# ✅ Fetch News & Sentiment Analysis
if st.button("🚀 Fetch News"):
    st.write(f"Fetching news for **{', '.join(selected_companies)}**...")

    # ✅ Show Progress Bar
    progress_bar = st.progress(0)
    for percent in range(0, 101, 20):
        time.sleep(0.2)
        progress_bar.progress(percent)

    # ✅ API Request
    all_sentiments = {}
    for company in selected_companies:
        try:
            response = requests.get(f"{API_URL}/{company}")
            response.raise_for_status()
            data = response.json()

            # ✅ Display News
            if "Articles" in data and data["Articles"]:
                st.subheader(f"📢 News for {company}")
                sentiments = []

                for article in data["Articles"]:
                    st.write(f"**{article['Title']}**")
                    st.write(f"📜 {article['Summary']}")
                    sentiment = article["Sentiment"]
                    sentiments.append(sentiment)
                    st.write(f"🟢 Sentiment: **{sentiment}**")

                    # ✅ Text-to-Speech
                    # ✅ Text-to-Speech Debugging
                    audio_fp = text_to_speech(article["Summary"])
                    if audio_fp:
                        audio_bytes = audio_fp.read()
    
                        # Debugging: Save file locally to verify
                        with open("test_audio.mp3", "wb") as f:
                             f.write(audio_bytes)
    
                        audio_base64 = base64.b64encode(audio_bytes).decode("utf-8")

                        

                        # ✅ Play Audio
                        st.audio(audio_bytes, format="audio/mp3")

                    else:
                        st.warning(f"⚠️ Failed to generate TTS for: {article['Title']}")


                    st.markdown("---")

                # ✅ Extracted Topics
                st.subheader(f"🔍 Extracted Topics for {company}")
                if "Topics" in data and data["Topics"]:
                    st.write(", ".join(data["Topics"]))
                else:
                    st.warning("⚠️ No topics found.")

                # ✅ Sentiment Distribution (Single Company)
                sentiment_counts = pd.Series(sentiments).value_counts()
                all_sentiments[company] = sentiment_counts
                st.subheader(f"📊 Sentiment Distribution for {company}")
                
                fig, ax = plt.subplots(1, 2, figsize=(12, 5))
                sentiment_counts.plot(kind="bar", ax=ax[0], color="skyblue", edgecolor="black")
                ax[0].set_title("Bar Chart")
                sentiment_counts.plot(kind="pie", ax=ax[1], autopct='%1.1f%%', startangle=90, colors=['green', 'blue', 'gray', 'orange', 'red'])
                ax[1].set_ylabel("")
                ax[1].set_title("Pie Chart")
                st.pyplot(fig)

            else:
                st.warning(f"⚠️ No news found for {company}.")

        except requests.exceptions.RequestException as e:
            st.error(f"❌ Failed to fetch news for {company}. API Error: {e}")

    # ✅ Comparative Sentiment Analysis (Multiple Companies)
    if len(selected_companies) > 1:
        st.subheader("📊 Comparative Sentiment Analysis")
        sentiment_df = pd.DataFrame(all_sentiments).fillna(0)
        sentiment_df.plot(kind="bar", figsize=(10, 5), colormap="coolwarm")
        st.pyplot(plt)
