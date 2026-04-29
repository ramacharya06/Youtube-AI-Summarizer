import http.cookiejar
import tempfile
import os
import requests
import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
from video_id_extractor import get_video_id

def get_transcript(video_url):
    session = requests.Session()
    
    # Load cookies into the session manually
    try:
        cookie_jar = http.cookiejar.MozillaCookieJar('cookies.txt')
        if os.path.exists('cookies.txt'):
            cookie_jar.load(ignore_discard=True, ignore_expires=True)
            session.cookies.update(cookie_jar)
        elif "YOUTUBE_COOKIES" in st.secrets:
            # In Streamlit Cloud, load from secrets
            cookie_str = st.secrets["YOUTUBE_COOKIES"].strip()
            if not cookie_str.startswith("# Netscape HTTP Cookie File"):
                cookie_str = "# Netscape HTTP Cookie File\n" + cookie_str
                
            with tempfile.NamedTemporaryFile(mode='w+', delete=False, encoding='utf-8') as temp_file:
                temp_file.write(cookie_str)
                temp_path = temp_file.name
            
            try:
                cookie_jar = http.cookiejar.MozillaCookieJar(temp_path)
                cookie_jar.load(ignore_discard=True, ignore_expires=True)
                session.cookies.update(cookie_jar)
            finally:
                os.remove(temp_path)
    except Exception as e:
        print(f"Warning: Could not load cookies - {e}")
        
    api = YouTubeTranscriptApi(http_client=session)
    transcript_data = api.fetch(get_video_id(video_url), languages=['en'])
    transcript = " ".join([entry.text for entry in transcript_data])    
    return transcript

if __name__ == "__main__":
   print(get_transcript("https://www.youtube.com/watch?v=gzt52Trk9w0"))

