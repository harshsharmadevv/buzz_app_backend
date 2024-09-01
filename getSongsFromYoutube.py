import yt_dlp as youtube_dl

def get_video_info(url):
    """Get video metadata such as title and thumbnail URL."""
    ydl_opts = {
        'quiet': True,  # Suppress output
        'extract_flat': True,  # Extract metadata without downloading
        'cookies': 'cookies.txt',  # Path to cookies file
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'  # Mimic a real browser
    }
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
        return info
    except Exception as e:
        print(f"Error getting video info: {e}")
        return {}

def get_audio_url(url):
    """Get the direct URL of the audio (MP3) stream for playback, along with video info."""
    ydl_opts = {
        'quiet': True,  # Suppress output
        'format': 'bestaudio/best',  # Select the best audio format available
        'noplaylist': True,  # Download only the single video, not the playlist
        'extract_flat': True,  # Extract info only, do not download
        'cookies': 'cookies.txt',  # Path to cookies file
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',  # Mimic a real browser
    }
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
        
        video_info = get_video_info(url)
        thumbnail_url = video_info.get('thumbnail', '')
        title = video_info.get('title', 'Untitled Video')
        
        if 'url' in info:
            return info['url'], thumbnail_url, title
        else:
            raise ValueError("Unable to extract audio URL.")
    except Exception as e:
        print(f"Error getting audio URL: {e}")
        return None, '', ''

# # Example usage
# if __name__ == "__main__":
#     url = 'https://www.youtube.com/watch?v=ETiHKMmfr-k'  # Replace with your video URL
#     audio_url, thumbnail_url, title = get_audio_url(url)
#     print(f"Audio URL: {audio_url}\nThumbnail URL: {thumbnail_url}\nTitle: {title}")
