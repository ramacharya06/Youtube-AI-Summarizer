import os
import requests
import streamlit as st
from video_id_extractor import get_video_id

def get_transcript(video_url):
    video_id = get_video_id(video_url)
    
    # Try to load API key from Streamlit secrets, then local environment variables
    try:
        api_key = st.secrets["RAPID_API_KEY"]
    except Exception:
        api_key = os.environ.get("RAPID_API_KEY", "")
        
    if not api_key:
        raise ValueError("RAPID_API_KEY is missing! Please add it to your .env file or Streamlit Secrets.")

    url = "https://youtube-transcript3.p.rapidapi.com/api/transcript"
    querystring = {"videoId": video_id}

    headers = {
        "x-rapidapi-key": api_key,
        "x-rapidapi-host": "youtube-transcript3.p.rapidapi.com",
        "Content-Type": "application/json"
    }

    response = requests.get(url, headers=headers, params=querystring)
    response.raise_for_status()
    data = response.json()
    
    if not data.get("success"):
        raise Exception(f"RapidAPI failed to fetch transcript: {data}")
        
    # Extract the text from the JSON array
    transcript_data = data.get("transcript", [])
    transcript = " ".join([entry["text"] for entry in transcript_data])
    
    return transcript

if __name__ == "__main__":
    print(get_transcript("https://www.youtube.com/watch?v=gzt52Trk9w0"))

