from youtube_transcript_api import YouTubeTranscriptApi
from video_id_extractor import get_video_id

# Extract video ID from URL


def get_transcript(video_url):
    transcript_data = YouTubeTranscriptApi.get_transcript(
        get_video_id(video_url), 
        languages=['en'],
        cookies='cookies.txt'
    )
    transcript = " ".join([entry['text'] for entry in transcript_data])    
    return transcript

if __name__ == "__main__":
   print(get_transcript("https://www.youtube.com/watch?v=gzt52Trk9w0"))

