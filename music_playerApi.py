from flask import Flask, abort, jsonify, request, send_file, url_for, send_from_directory
import os
import json
# from downloadAudioFromYt import download_video, video_to_mp3, download_thumbnail, get_video_info
from getSongsFromYoutube import get_audio_url
from mp3SongUrlConvertor import convert_mp4_to_mp3, download_file
import uuid
import io
from pymongo import MongoClient
import gridfs

from bson.objectid import ObjectId

# MongoDB connection details
MONGO_URI = 'mongodb://localhost:27017/'  # Apne MongoDB server ka URI yahan daalain
DATABASE_NAME = 'musicDB'
COLLECTION_NAME = 'songsFiles'

app = Flask(__name__)

client = MongoClient(MONGO_URI)
db = client[DATABASE_NAME]
fs = gridfs.GridFS(db, collection=COLLECTION_NAME)


STATIC_FOLDER = 'static'


@app.route('/', methods=['GET'])
def main():
    return 'Buzz MusicPlayer Api'


@app.route('/static/audio/<path:filename>')
def serve_audio(filename):
    return send_from_directory(os.path.join(STATIC_FOLDER, 'audio'), filename)

@app.route('/static/videos/<path:filename>')
def serve_video(filename):
    return send_from_directory(os.path.join(STATIC_FOLDER, 'videos'), filename)

@app.route("/downloadAudioFromYoutube", methods=['POST'])
def downloadAudioFromYoutube():
    data = request.get_json()
    url = data.get('youtubeVideoUrl', '')

    if not url:
        return jsonify({'error': 'No URL provided'}), 400

    try:
        audio_url, thumbnail_url, title = get_audio_url(url)
        
        return jsonify({
            'message': 'Video downloaded and converted to MP3',
            'audio_url': audio_url,
            'video_url': '',
            'thumbnail_url': thumbnail_url,
            'title': title
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/convert', methods=['POST'])
def convert():
    data = request.json
    mp4_url = data.get('mp4_url')
    song_id = data.get('song_id')

    if not mp4_url:
        return jsonify({"error": "MP4 URL is required"}), 400

    mp3_filename = f'{song_id}.mp3'

    # Check if the MP3 file already exists in GridFS
    existing_file = fs.find_one({"filename": mp3_filename})
    if existing_file:
        # File already exists, return the URL
        file_id = existing_file._id

        try:
            # Generate a URL to access the MP3 file
            file_url = url_for('serve_file', file_id=file_id, _external=True)
            return jsonify({
                "message": "File found",
                "mp3_url": file_url
            })
        except Exception as e:
            print(f"Error retrieving file with ID {file_id}: {e}")
            return jsonify({"error": str(e)}), 500

    # Generate filenames
    unique_id = uuid.uuid4().hex
    mp4_filename = f'temp_{unique_id}.mp4'

    # Download the file
    downloaded_file = download_file(mp4_url, mp4_filename)

    if downloaded_file:
        try:
            # Convert MP4 to MP3
            convert_mp4_to_mp3(mp4_filename, mp3_filename)
            
            # Read the MP3 file as binary data
            with open(mp3_filename, 'rb') as mp3_file:
                file_id = fs.put(mp3_file, filename=mp3_filename)
                
            print(f'File saved with ID: {file_id}')

            # Generate a URL to access the MP3 file
            file_url = url_for('serve_file', file_id=file_id, _external=True)

            # Clean up temporary files
            os.remove(mp4_filename)
            os.remove(mp3_filename)
            
            return jsonify({
                "message": "The MP3 file can be accessed at:",
                "mp3_url": file_url
            })
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    else:
        return jsonify({"error": "Failed to download MP4 file."}), 500

@app.route('/files/<file_id>', methods=['GET'])
def serve_file(file_id):
    try:
        file_id = ObjectId(file_id)  # Convert file_id to ObjectId
        file_data = fs.get(file_id).read()  # Retrieve file from GridFS
        return send_file(io.BytesIO(file_data), mimetype='audio/mp3')  # Serve the file for streaming
    except Exception as e:
        print(f"Error retrieving file with ID {file_id}: {e}")
        return jsonify({"error": str(e)}), 404

if __name__ == '__main__':
    app.run(debug=True, port=8080)
