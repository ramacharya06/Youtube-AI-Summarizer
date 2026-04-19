from urllib.parse import urlparse, parse_qs

def get_video_id(url):
    # Handle different YouTube URL formats
    # youtube.com/watch?v=VIDEO_ID
    # youtu.be/VIDEO_ID
    # youtube.com/embed/VIDEO_ID
    
    if 'youtu.be' in url:
        return url.split('/')[-1].split('?')[0]
    elif 'youtube.com' in url:
        parsed = urlparse(url)
        return parse_qs(parsed.query).get('v', [None])[0]
