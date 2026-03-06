# Chat With Any Website

Chat With Any Website is a FastAPI-based web application that lets users enter a website URL, scrape its content, retrieve relevant sections using TF-IDF, and ask questions through a chat interface.

## Features
- Scrapes website content
- Cleans and preprocesses text
- Chunks text into smaller sections
- Uses TF-IDF to retrieve relevant chunks
- Displays answers in a chat UI

## Tech Stack
- FastAPI
- Jinja2
- BeautifulSoup
- Requests
- scikit-learn
- HTML/CSS

## Project Structure
app/main.py  
app/scraper.py  
app/search.py  
templates/index.html  

## Run Locally
```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
