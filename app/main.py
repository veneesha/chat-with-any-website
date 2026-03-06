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


@app.get("/scrape")
def scrape(url: str = Query(...)):
    try:
        text = scrape_website(url)
        return {
            "url": url,
            "content_preview": text[:1000],
            "content_length": len(text)
        }
    except Exception as e:
        return {"error": str(e)}


@app.get("/chunk")
def chunk(url: str = Query(...)):
    try:
        text = scrape_website(url)
        chunks = chunk_text(text)

        return {
            "url": url,
            "total_chunks": len(chunks),
            "first_chunk": chunks[0] if chunks else "",
            "second_chunk": chunks[1] if len(chunks) > 1 else ""
        }
    except Exception as e:
        return {"error": str(e)}


@app.get("/search")
def search(url: str = Query(...), query: str = Query(...)):
    try:
        text = scrape_website(url)
        chunks = chunk_text(text)
        matches = search_chunks(chunks, query, top_k=1)

        return {
            "url": url,
            "query": query,
            "best_match": matches[0] if matches else "",
            "total_chunks": len(chunks)
        }
    except Exception as e:
        return {"error": str(e)}


@app.get("/ask")
def ask(url: str = Query(...), question: str = Query(...)):
    try:
        text = scrape_website(url)
        chunks = chunk_text(text)
        matches = search_chunks(chunks, question, top_k=1)
        context = matches[0] if matches else ""

        answer = context if context else "I could not find relevant information in the website content."

        return {
            "url": url,
            "question": question,
            "context": context,
            "answer": answer
        }
    except Exception as e:
        return {"error": str(e)}


@app.get("/chat", response_class=HTMLResponse)
def chat_page(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "answer": "",
            "url": "",
            "question": ""
        }
    )


@app.post("/chat", response_class=HTMLResponse)
def chat_submit(request: Request, url: str = Form(...), question: str = Form(...)):
    try:
        text = scrape_website(url)
        chunks = chunk_text(text)
        matches = search_chunks(chunks, question, top_k=1)
        context = matches[0] if matches else ""
        answer = context if context else "I could not find relevant information in the website content."

        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "answer": answer,
                "url": url,
                "question": question
            }
        )
    except Exception as e:
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "answer": f"Error: {str(e)}",
                "url": url,
                "question": question
            }
        )
