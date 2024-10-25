# CodeMatic | YouTube Data Processing Assessment

This project implements a simple Youtube API integration to fetch metadata and comments using FastAPI.

# Features

- Fetch video details (title, description, view count, like count) for a given YouTube video ID
- Load and display top-level comments for the video with pagination support
- Handle API rate limits and errors gracefully


## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.11 or later
- pip (latest version)
- poetry (latest version)
- A YouTube Data API key(Get it here)

## Setup

1. Ensure you have Python 3.11 installed on your system.

2. Clone this repository:
   ```
   git clone `https://github.com/PamilerinId/codematic-youtube-backennd.git`
   cd codematic-youtube-backennd
   ```

3. Install dependencies using Pipenv:
   ```
   pip install poetry
   poetry install
   ```

## Running the API

1. Activate the virtual environment:
   ```
   poetry shell
   ```

2. Update environment variables
   ```
   Rename .env.example to .env
   Update the YOUTUBE_API_KEY variable in .env with your actual API key
   ```

3. Start the FastAPI server:
   ```
   uvicorn app.main:app --port=8003 --reload 
   ```

   The API will be available at `http://localhost:8003/docs`.
   

## API Endpoints

- `GET /api/v1/video/{video_id}`: Fetch video details
  - Returns title, description, view count, and like count

- `GET /api/v1/comments/{video_id}`: Fetch video comments
  - Optional query parameter: `pageToken` for pagination
  - Returns a list of comments and a `nextPageToken` if more comments are available

## Error Handling

- The API handles YouTube API rate limits and returns appropriate error messages
- Logging is implemented for debugging purposes

## Running Tests

To run the tests, use the following command:
```
pytest test/test.py    --- All tests pass ✔️