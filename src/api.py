from fastapi import FastAPI
from typing import List, Dict
from collections import Counter
import yake
from pydantic import BaseModel

app = FastAPI(
    title="News Summarization API",
    description="API for fetching news, performing sentiment analysis, and topic extraction",
    version="1.3",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Sample News Database
NEWS_DB = {
    "Apple": [
        {"Title": "Apple loses German antitrust fight", "Summary": "Apple faces greater scrutiny.", "Sentiment": "Negative"},
        {"Title": "Apple iPhone 17 Leaks", "Summary": "New design features for iPhone 17 Air.", "Sentiment": "Neutral"},
        {"Title": "Best Apple Watch 2025", "Summary": "Top-rated Apple Watch models.", "Sentiment": "Positive"},
    ],
    "Microsoft": [
        {"Title": "Microsoft AI Advances", "Summary": "New AI features in Microsoft Copilot.", "Sentiment": "Positive"},
        {"Title": "Windows Update Issues", "Summary": "Users report problems with recent update.", "Sentiment": "Negative"},
    ]
}

# Pydantic Models
class NewsRequest(BaseModel):
    companies: List[str]

class SentimentComparisonResponse(BaseModel):
    Sentiment_Comparison: Dict[str, Dict[str, int]]

# Function to Extract Topics Using YAKE
def extract_topics(summaries: List[str], num_topics: int = 5) -> List[str]:
    kw_extractor = yake.KeywordExtractor()
    keywords = []
    for summary in summaries:
        keywords.extend([kw for kw, _ in kw_extractor.extract_keywords(summary)])
    return list(Counter(keywords).keys())[:num_topics]

# Home Endpoint
@app.get("/")
def home():
    return {"message": "Welcome to the News Summarization API!"}

# Fetch News for a Given Company
@app.get("/news/{company}")
def get_news(company: str):
    if company in NEWS_DB:
        summaries = [article["Summary"] for article in NEWS_DB[company]]
        topics = extract_topics(summaries)
        return {"Company": company, "Articles": NEWS_DB[company], "Topics": topics}
    return {"Company": company, "Articles": [], "Topics": []}

# Fetch News for Multiple Companies
@app.post("/news_batch")
def get_news_batch(request: NewsRequest):
    results = {}
    for company in request.companies:
        if company in NEWS_DB:
            summaries = [article["Summary"] for article in NEWS_DB[company]]
            topics = extract_topics(summaries)
            results[company] = {"Articles": NEWS_DB[company], "Topics": topics}
        else:
            results[company] = {"Articles": [], "Topics": []}
    return results

# Compare Sentiments Across Multiple Companies
@app.post("/compare_sentiment", response_model=SentimentComparisonResponse)
def compare_sentiment(request: NewsRequest):
    sentiment_counts = {}
    all_possible_sentiments = ["Very Positive", "Positive", "Neutral", "Negative", "Very Negative"]

    for company in request.companies:
        if company in NEWS_DB:
            sentiments = [article["Sentiment"] for article in NEWS_DB[company]]
            counts = Counter(sentiments)
            sentiment_counts[company] = {sent: counts.get(sent, 0) for sent in all_possible_sentiments}
        else:
            sentiment_counts[company] = {sent: 0 for sent in all_possible_sentiments}

    return {"Sentiment_Comparison": sentiment_counts}
