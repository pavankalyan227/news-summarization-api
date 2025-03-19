from fastapi import FastAPI, HTTPException
from src.utils import get_news_articles

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Welcome to the News Summarization API!"}

@app.get("/news/{company}")
def fetch_news(company: str):
    articles = get_news_articles(company)
    if not articles:
        raise HTTPException(status_code=404, detail="No news found!")
    return {"Company": company, "Articles": articles}
