import streamlit as st
import requests
import matplotlib.pyplot as plt
import pandas as pd
import time
from gtts import gTTS
import base64
from io import BytesIO
from googletrans import Translator

# API URLs
API_URL = "https://news-summarization-api.onrender.com/news/"
COMPARE_SENTIMENT_URL = "https://news-summarization-api.onrender.com/compare_sentiment"

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
            response.raise_for_status()
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

                # **🔍 Extracted Topics**
                st.subheader(f"🔍 Extracted Topics for {company}")

# Ensure "Topics" is in response and not empty
                topics = data.get("Topics", [])
                if topics:
                    st.write(", ".join(topics))
                



                # Store sentiment distribution
                sentiment_counts = pd.Series(sentiments).value_counts().sort_index()
                all_sentiments[company] = sentiment_counts

                # **📊 Sentiment Visualization for Single Company**
                if not sentiment_counts.empty:
                    st.subheader(f"📊 Sentiment Distribution for {company}")

                    col1, col2 = st.columns(2)

                    with col1:
                        st.bar_chart(sentiment_counts)  # 📊 Bar Chart

                    with col2:
                        fig, ax = plt.subplots(figsize=(5, 5))
                        sentiment_counts.plot(kind="pie", autopct='%1.1f%%', ax=ax)
                        ax.set_ylabel("")  
                        ax.axis("equal")  
                        st.pyplot(fig)  # 🥧 Pie Chart

            

        except requests.exceptions.RequestException as e:
            st.error(f"❌ Failed to fetch news for {company}. API Error: {e}")

    # **📊 Sentiment Comparison for Multiple Companies**
    if len(selected_companies) > 1 and all_sentiments:
        st.subheader("📊 Comparative Sentiment Analysis Across Companies")

        sentiment_df = pd.DataFrame(all_sentiments).fillna(0)
        st.bar_chart(sentiment_df)  # 📊 Bar Chart
        fig, ax = plt.subplots(figsize=(6, 6))
        sentiment_df.sum(axis=1).plot(kind="pie", labels=sentiment_df.index, autopct='%1.1f%%', ax=ax)
        ax.set_ylabel("")
        ax.axis("equal")
        st.pyplot(fig)
