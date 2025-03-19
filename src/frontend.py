import streamlit as st
import requests
import matplotlib.pyplot as plt
import pandas as pd
import time

# API URL
API_URL = "http://127.0.0.1:8000/news/"

# Available companies with logos
COMPANIES = {
    "Apple": "🍏",
    "Microsoft": "💻",
    "Google": "🔍",
    "Amazon": "🛒",
    "Tesla": "🚗"
}

# Streamlit UI
st.set_page_config(page_title="News Analysis", page_icon="📰", layout="wide")

# Title with formatting
st.markdown("<h1 style='text-align: center; color: #0077cc;'>📰 News Summarization & Sentiment Analysis</h1>", unsafe_allow_html=True)

st.write("### Select a company to fetch the latest news and sentiment analysis.")

# Dropdown to select a company
selected_company = st.selectbox("🔎 Choose a company:", list(COMPANIES.keys()))

if st.button("🚀 Fetch News"):
    st.write(f"Fetching news for **{selected_company} {COMPANIES[selected_company]}**...")

    # Show progress bar
    progress_bar = st.progress(0)
    for percent in range(0, 101, 20):
        time.sleep(0.2)
        progress_bar.progress(percent)

    # API Request
    response = requests.get(API_URL + selected_company)
    
    if response.status_code == 200:
        data = response.json()
        articles = data.get("Articles", [])

        if not articles:
            st.warning("⚠️ No news found for this company.")
        else:
            sentiments = []

            for article in articles:
                st.subheader(article["Title"])
                st.write(f"📝 **Summary:** {article['Summary']}")
                sentiment = article["Sentiment"]
                sentiments.append(sentiment)

                # Sentiment color-coding
                if sentiment == "Very Positive":
                    st.success(f"✅ Sentiment: {sentiment}")
                elif sentiment == "Positive":
                    st.info(f"🙂 Sentiment: {sentiment}")
                elif sentiment == "Neutral":
                    st.warning(f"😐 Sentiment: {sentiment}")
                elif sentiment == "Negative":
                    st.error(f"⚠️ Sentiment: {sentiment}")
                else:
                    st.error(f"❌ Sentiment: {sentiment}")

                st.markdown("---")

            # Sentiment Visualization
            st.subheader("📊 Sentiment Distribution")
            sentiment_counts = pd.Series(sentiments).value_counts()

            col1, col2 = st.columns(2)

            with col1:
                fig, ax = plt.subplots()
                ax.pie(sentiment_counts, labels=sentiment_counts.index, autopct='%1.1f%%', colors=['green', 'blue', 'gray', 'orange', 'red'])
                ax.axis("equal")
                st.pyplot(fig)

            with col2:
                st.bar_chart(sentiment_counts)

    else:
        st.error("❌ Failed to fetch news. Please check API connection.")
