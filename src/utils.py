import requests
from bs4 import BeautifulSoup
from textblob import TextBlob
from gtts import gTTS
import os

# Function for sentiment analysis (Move this ABOVE get_news_articles)
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()
def analyze_sentiment(text):
    # VADER Sentiment
    analyzer = SentimentIntensityAnalyzer()
    vader_score = analyzer.polarity_scores(text)['compound']

    # TextBlob Sentiment
    textblob_score = TextBlob(text).sentiment.polarity

    # Averaging both scores for better accuracy
    final_score = (vader_score + textblob_score) / 2  

    # Define sentiment categories
    if final_score >= 0.5:
        return "Very Positive"
    elif final_score >= 0.1:
        return "Positive"
    elif final_score <= -0.5:
        return "Very Negative"
    elif final_score <= -0.1:
        return "Negative"
    else:
        return "Neutral"

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

    tts = gTTS(text=text, lang="en")  # Change lang="hi" for Hindi
    filepath = os.path.join("data", filename)

    if not os.path.exists("data"):
        os.makedirs("data")

    tts.save(filepath)
    return filepath
