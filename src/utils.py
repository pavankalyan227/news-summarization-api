import requests
from bs4 import BeautifulSoup
from textblob import TextBlob
from gtts import gTTS
import os

# Function for sentiment analysis (Move this ABOVE get_news_articles)
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()

def analyze_sentiment(text):
    score = analyzer.polarity_scores(text)["compound"]
    return "Positive" if score > 0.05 else "Negative" if score < -0.05 else "Neutral"

# Function to fetch news articles using Google News RSS
def get_news_articles(company_name):
    url = f"https://news.google.com/rss/search?q={company_name}&hl=en-US&gl=US&ceid=US:en"
    
    response = requests.get(url)
    if response.status_code != 200:
        return [{"Title": "Error", "Summary": "Failed to fetch news"}]

    soup = BeautifulSoup(response.content, "xml")  # Parse as XML
    articles = []

    for item in soup.find_all("item")[:10]:  # Get first 10 articles
        title = item.title.text.strip()
        summary_html = item.find("description").text.strip()
        cleaned_summary = BeautifulSoup(summary_html, "html.parser").get_text(separator=" ")

        # Remove title from summary if it's repeated
        summary = cleaned_summary.replace(title, "").strip()
        if not summary or summary.lower() == title.lower():
            summary = "No summary available."

        sentiment = analyze_sentiment(summary)

        articles.append({"Title": title, "Summary": summary, "Sentiment": sentiment})

    return articles


# Function to generate Hindi text-to-speech
def text_to_speech(text, filename="summary.mp3"):
    if not text.strip():
        return None  # Prevent empty speech files
    
    tts = gTTS(text=text, lang="hi")
    filepath = os.path.join("data", filename)
    
    # Ensure "data" folder exists
    if not os.path.exists("data"):
        os.makedirs("data")

    tts.save(filepath)
    return filepath
