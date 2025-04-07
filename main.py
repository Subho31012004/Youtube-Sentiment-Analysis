from fastapi import FastAPI, HTTPException, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from textblob import TextBlob
import googleapiclient.discovery
import os
from dotenv import load_dotenv
from typing import List
import re

# Load environment variables
load_dotenv()
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

# Initialize FastAPI app
app = FastAPI()

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Initialize templates
templates = Jinja2Templates(directory="templates")

def extract_video_id(url: str) -> str:
    # Handle different YouTube URL formats
    patterns = [
        r'(?:v=|\/)([0-9A-Za-z_-]{11}).*',
        r'(?:embed\/)([0-9A-Za-z_-]{11})',
        r'(?:youtu\.be\/)([0-9A-Za-z_-]{11})'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None

def analyze_sentiment(text: str) -> str:
    analysis = TextBlob(text)
    # Get the polarity score (-1 to 1)
    polarity = analysis.sentiment.polarity
    
    # Convert polarity to sentiment category
    if polarity > 0.1:
        return "positive"
    elif polarity < -0.1:
        return "negative"
    else:
        return "neutral"

def fetch_youtube_comments(video_id: str, max_comments: int) -> List[str]:
    if not YOUTUBE_API_KEY:
        raise HTTPException(status_code=500, detail="YouTube API key not found")

    try:
        youtube = googleapiclient.discovery.build(
            "youtube", 
            "v3", 
            developerKey=YOUTUBE_API_KEY
        )

        request = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            maxResults=max_comments,
            textFormat="plainText"
        )
        
        response = request.execute()
        
        comments = []
        for item in response.get("items", []):
            comment = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
            comments.append(comment)
        
        return comments

    except Exception as e:
        print(f"YouTube API Error: {str(e)}")  # Debug print
        raise HTTPException(status_code=500, detail=f"YouTube API Error: {str(e)}")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "results": None})

@app.post("/", response_class=HTMLResponse)
async def analyze(request: Request, video_url: str = Form(...), max_comments: int = Form(20)):
    try:
        video_id = extract_video_id(video_url)
        if not video_id:
            return templates.TemplateResponse(
                "index.html",
                {"request": request, "error": "Invalid YouTube URL", "results": None}
            )

        comments = fetch_youtube_comments(video_id, max_comments)
        
        if not comments:
            return templates.TemplateResponse(
                "index.html",
                {"request": request, "error": "No comments found for this video", "results": None}
            )

        sentiment_results = [
            {
                "comment": comment,
                "sentiment": analyze_sentiment(comment)
            }
            for comment in comments
        ]

        # Calculate sentiment statistics
        total_comments = len(sentiment_results)
        positive = sum(1 for r in sentiment_results if r["sentiment"] == "positive")
        negative = sum(1 for r in sentiment_results if r["sentiment"] == "negative")
        neutral = sum(1 for r in sentiment_results if r["sentiment"] == "neutral")

        stats = {
            "total": total_comments,
            "positive": positive,
            "negative": negative,
            "neutral": neutral,
            "positive_percent": (positive/total_comments) * 100,
            "negative_percent": (negative/total_comments) * 100,
            "neutral_percent": (neutral/total_comments) * 100
        }

        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "results": sentiment_results,
                "stats": stats,
                "video_url": video_url
            }
        )

    except Exception as e:
        return templates.TemplateResponse(
            "index.html",
            {"request": request, "error": str(e), "results": None}
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
