import os
from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, HTTPException
import requests
import logging

app = FastAPI(
    title="CodeMatic | YouTube Data Processing Assessment",
    description="A Youtube API integration to fetch metadata and comments",
    version="1.0.0",
)

YOUTUBE_API_KEY = os.environ.get('YOUTUBE_API_KEY')
YOUTUBE_API_URL = os.environ.get('YOUTUBE_API_URL')

logging.basicConfig(level=logging.INFO)


@app.get("/api/v1/video/{video_id}")
def get_video_details(video_id: str):
    url = f"{YOUTUBE_API_URL}/videos?part=snippet,statistics&id={video_id}&key={YOUTUBE_API_KEY}"
    response = requests.get(url)

    if response.status_code != 200:
        logging.info(response.json())
        raise HTTPException(status_code=response.status_code, detail="Failed to fetch video details")

    data = response.json()
    if not data['items']:
        raise HTTPException(status_code=404, detail="Video not found")

    video_info = data['items'][0]
    snippet = video_info['snippet']
    statistics = video_info['statistics']

    return {
        'message': 'Video details fetched successfully',
        'data': {
            'title': snippet['title'],
            'description': snippet['description'],
            'view_count': statistics['viewCount'],
            'like_count': statistics['likeCount']
        }
    }


@app.get("/api/v1/comments/{video_id}")
def get_comments(video_id: str, page_token: str = None):
    url = f"{YOUTUBE_API_URL}/commentThreads?part=snippet&videoId={video_id}&maxResults=100&key={YOUTUBE_API_KEY}"
    if page_token:
        url += f"&pageToken={page_token}"

    response = requests.get(url)

    if response.status_code == 403:
        logging.warning("Rate limit reached. Retry later.")
        raise HTTPException(status_code=403, detail="Rate limit exceeded. Please try again later.")
    elif response.status_code != 200:
        logging.info(response.json())
        raise HTTPException(status_code=response.status_code, detail="Failed to fetch comments")

    data = response.json()

    comments = []
    for item in data['items']:
        comment = item['snippet']['topLevelComment']['snippet']
        comments.append({
            'author': comment['authorDisplayName'],
            'text': comment['textDisplay'],
            'like_count': comment['likeCount']
        })

    return {
        'message': 'Comments fetched successfully',
        'data': {
            'comments': comments,
            'nextPageToken': data.get('nextPageToken')
        }
    }
