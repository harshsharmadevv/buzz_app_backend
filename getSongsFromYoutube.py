import yt_dlp as youtube_dl

def get_video_info(url):
    """Get video metadata such as title and thumbnail URL."""
    ydl_opts = {
        'quiet': True,  # Suppress output
        'extract_flat': True,  # Extract metadata without downloading
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
    return info

def get_audio_url(url):
    """Get the direct URL of the audio (MP3) stream for playback, along with video info."""
    # Options to extract the best audio format
    ydl_opts = {
        'quiet': True,  # Suppress output
        'format': 'bestaudio/best',  # Select the best audio format available
        'noplaylist': True,  # Download only the single video, not the playlist
        'extract_flat': True,  # Extract info only, do not download
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
    
    # Fetch additional video info for thumbnail and title
    video_info = get_video_info(url)
    thumbnail_url = video_info.get('thumbnail', '')
    title = video_info.get('title', 'Untitled Video')
    
    # Check if the 'url' key exists in the info dictionary
    if 'url' in info:
        return info['url'], thumbnail_url, title
    else:
        raise ValueError("Unable to extract audio URL.")

