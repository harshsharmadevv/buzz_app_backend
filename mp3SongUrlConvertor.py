import requests
import subprocess
import os

def download_file(url, filename):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Will raise HTTPError for bad responses (4xx and 5xx)
        
        with open(filename, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        return filename
    except requests.RequestException as e:
        print(f"Failed to download file: {e}")
        return None

def convert_mp4_to_mp3(input_file, output_file):
    ffmpeg_path = r'C:\ffmpeg\ffmpeg-7.0.2-full_build\bin\ffmpeg.exe'
    
    if not os.path.exists(ffmpeg_path):
        raise FileNotFoundError(f"FFmpeg executable not found at {ffmpeg_path}")
    
    if not os.path.exists(input_file):
        raise FileNotFoundError(f"Input file not found: {input_file}")
    
    command = [
        ffmpeg_path,
        '-y',                  # Force overwrite of output file
        '-i', input_file,
        '-q:a', '0',           # Quality setting: 0 is best quality
        '-map', 'a',           # Only map the audio stream
        output_file
    ]
    
    try:
        subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        if not os.path.exists(output_file):
            raise FileNotFoundError(f"Output file was not created: {output_file}")
        
        print(f"MP3 file created ata : {output_file}")
        return output_file
    except subprocess.CalledProcessError as e:
        print(f"FFmpeg error: {e.stderr.decode()}")
        raise
    except Exception as e:
        print(f"An error occurred: {e}")
        raise
