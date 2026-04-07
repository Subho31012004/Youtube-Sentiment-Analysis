# YouTube Sentiment Analysis

🔍 **Analyze YouTube video sentiment in real-time** - Extract comments, perform sentiment analysis, and visualize audience reactions with a beautiful web interface.

[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![TextBlob](https://img.shields.io/badge/TextBlob-FF6B35?style=for-the-badge&logo=data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNTEyIiBoZWlnaHQ9IjUxMiIgdmlld0JveD0iMCAwIDUxMiA1MTIiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxwYXRoIGQ9Ik0yNTYgMEwyNTYgNTEyTDUxMiA1MTJMMzIwIDMyMEw1MTIgMzIwTDUxMiAwTDMyMCAwTDMyMCAzMjBMMjU2IDMyMFoiIGZpbGw9IiNGRjZIzMzkiLz4KPC9zdmc+Cg==)](https://textblob.readthedocs.io)

## ✨ Features

- **🎥 YouTube URL Parser** - Supports all YouTube URL formats (watch, embed, youtu.be)
- **💬 Comment Extraction** - Fetches real-time YouTube comments via YouTube Data API v3
- **🎭 Sentiment Analysis** - Powered by TextBlob (Positive/Negative/Neutral)
- **📊 Live Statistics** - Real-time sentiment breakdown with percentages
- **🎨 Modern UI** - Responsive HTML/CSS/JS frontend with smooth animations
- **⚡ FastAPI Backend** - High-performance Python API with Jinja2 templating
- **🔒 Error Handling** - Graceful error messages for invalid URLs/API issues

## 🛠 Tech Stack

Backend: FastAPI | Python 3.9+ | TextBlob | Google API Client
Frontend: HTML5 | CSS3 | JavaScript 
API: YouTube Data API v3


## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- [YouTube Data API Key](https://console.developers.google.com/)
- pip/pipenv/poetry

### 1. Clone & Install
```bash
git clone https://github.com/Subho31012004/Youtube-Sentiment-Analysis.git
cd Youtube-Sentiment-Analysis
pip install -r requirements.txt
```

### 2. Setup Environment
```bash
cp .env.example .env
```
Edit `.env`:
```env
YOUTUBE_API_KEY=your_youtube_api_key_here
```

### 3. Run Server
```bash
python main.py
# or
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 4. Open Browser
http://localhost:8000


## 🎯 How It Works
User enters YouTube URL

Extract video ID (regex patterns)


Fetch comments via YouTube API (max 20-100)


Analyze each comment sentiment (TextBlob)


Calculate stats & render results


Display interactive dashboard


## 📊 Sample Output
Total Comments: 50
✅ Positive: 32 (64%)
❌ Negative: 8 (16%)
⭕ Neutral: 10 (20%)
