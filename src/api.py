from fastapi import FastAPI
from src.utils import get_news_articles, text_to_speech

import os

app = FastAPI()

# Root Endpoint
@app.get("/")
def home():
    return {"message": "Welcome to the News Summarization API!"}

# Fetch News for a Given Company
@app.get("/news/{company}")
def fetch_news(company: str):
    articles = get_news_articles(company)
    if not articles:
        return {"error": "No news articles found"}

    return {"Company": company, "Articles": articles}

# Generate Speech from Summary
@app.post("/tts/")
def generate_tts(text: str):
    audio_path = text_to_speech(text)
    if not audio_path:
        return {"error": "No text provided for speech"}
    
    return {"message": "Speech generated", "file_path": audio_path}
