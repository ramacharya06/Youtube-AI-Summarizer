from youtube_transcript_api import YouTubeTranscriptApi
from video_id_extractor import get_video_id

# Extract video ID from URL


def get_transcript(video_url):
    api = YouTubeTranscriptApi()
    transcript_data = api.fetch(get_video_id(video_url), languages=['en'])
    transcript = " ".join([entry.text for entry in transcript_data])    
    return transcript
# Print transcript
# for line in transcript:
#     print(line['text'])

if __name__ == "__main__":
   print(get_transcript("https://www.youtube.com/watch?v=gzt52Trk9w0"))

