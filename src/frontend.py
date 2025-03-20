import streamlit as st
import requests
import matplotlib.pyplot as plt
import pandas as pd
import time
from gtts import gTTS
import base64
from io import BytesIO
from googletrans import Translator  # Import Translator for translation

# API URL (Deployed on Render)
API_URL = "https://news-summarization-api.onrender.com/news/"

# Available companies with icons
COMPANIES = {
    "Apple": "🍏",
    "Microsoft": "💻",
    "Google": "🔍",
    "Amazon": "🛒",
    "Tesla": "🚗"
}

# Streamlit UI Configuration
st.set_page_config(page_title="News Analysis", page_icon="📰", layout="wide")

# Title with styling
st.markdown(
    "<h1 style='text-align: center; color: #0077cc;'>📰 News Summarization & Sentiment Analysis</h1>",
    unsafe_allow_html=True
)
st.write("### Select companies to fetch and compare sentiment analysis.")

# Multi-selection dropdown for companies
selected_companies = st.multiselect("🔎 Choose companies:", list(COMPANIES.keys()), default=["Apple"])

# Function to Convert Text to Speech in Hindi
def text_to_speech(text):
    try:
        translator = Translator()
        translated_text = translator.translate(text, src='en', dest='hi').text  # Translate to Hindi
        tts = gTTS(translated_text, lang='hi')  # Convert to Hindi speech
        audio_fp = BytesIO()
        tts.write_to_fp(audio_fp)
        audio_fp.seek(0)
        return audio_fp
    except Exception as e:
        st.error(f"⚠️ Error in Text-to-Speech: {e}")
        return None

# Fetch News Button
if st.button("🚀 Fetch News"):
    st.write(f"Fetching news for **{', '.join(selected_companies)}**...")

    # Show progress bar
    progress_bar = st.progress(0)
    for percent in range(0, 101, 20):
        time.sleep(0.2)
        progress_bar.progress(percent)

    all_sentiments = {}  # Store sentiment distributions

    # Fetch data for each selected company
    for company in selected_companies:
        try:
            response = requests.get(API_URL + company)
            response.raise_for_status()  # Raise error if request fails
            data = response.json()

            if "Articles" in data and data["Articles"]:
                sentiments = []

                for article in data["Articles"]:
                    st.subheader(f"{company} - {article['Title']}")
                    st.write(f"📝 **Summary:** {article['Summary']}")
                    sentiment = article["Sentiment"]
                    sentiments.append(sentiment)

                    sentiment_color_map = {
                        "Very Positive": "✅",
                        "Positive": "🙂",
                        "Neutral": "😐",
                        "Negative": "⚠️",
                        "Very Negative": "❌"
                    }
                    st.write(f"{sentiment_color_map.get(sentiment, '❓')} **Sentiment: {sentiment}**")

                    # Add Text-to-Speech Option
                    audio_fp = text_to_speech(article["Summary"])
                    if audio_fp:
                        audio_base64 = base64.b64encode(audio_fp.read()).decode("utf-8")
                        st.audio(f"data:audio/mp3;base64,{audio_base64}", format="audio/mp3")

                    st.markdown("---")

                # Store sentiment distribution
                sentiment_counts = pd.Series(sentiments).value_counts()
                all_sentiments[company] = sentiment_counts

                # Sentiment Visualization (Single Company)
                st.subheader(f"📊 Sentiment Distribution for {company}")

                col1, col2 = st.columns(2)
                with col1:
                    fig, ax = plt.subplots()
                    ax.pie(
                        sentiment_counts, 
                        labels=sentiment_counts.index, 
                        autopct='%1.1f%%',
                        colors=['green', 'blue', 'gray', 'orange', 'red']
                    )
                    ax.axis("equal")
                    st.pyplot(fig)

                with col2:
                    st.bar_chart(sentiment_counts)

            else:
                st.warning(f"⚠️ No news found for {company}.")

        except requests.exceptions.RequestException as e:
            st.error(f"❌ Failed to fetch news for {company}. API Error: {e}")

    # Comparative Sentiment Visualization
    if all_sentiments:
        st.subheader("📊 Comparative Sentiment Analysis")

        sentiment_df = pd.DataFrame(all_sentiments).fillna(0)
        sentiment_df.plot(kind="bar", figsize=(10, 5), colormap="coolwarm")
        st.pyplot(plt)
