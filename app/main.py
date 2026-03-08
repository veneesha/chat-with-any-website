from fastapi import FastAPI, Query, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.scraper import scrape_website, chunk_text
from app.search import search_chunks

app = FastAPI()
templates = Jinja2Templates(directory="templates")


@app.get("/")
def home():
    return {"message": "AI Website Chatbot API running"}


@app.head("/")
def home_head():
    return HTMLResponse(status_code=200)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.head("/health")
def health_head():
    return HTMLResponse(status_code=200)
