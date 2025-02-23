from flask import Flask, render_template, request, jsonify
import os
import yt_dlp

app = Flask(__name__)

# Ensure 'static/downloads' directory exists
DOWNLOAD_FOLDER = "static/downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

def download_video(url, format_type):
    options = {
        'mp4': {
            'format': 'bestvideo+bestaudio/best',
            'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(title)s.mp4'),
            'postprocessors': [{'key': 'FFmpegVideoConvertor', 'preferedformat': 'mp4'}],
        },
        'mp3': {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(title)s.mp3'),
            'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': '192'}],
        }
    }

    ydl_opts = options.get(format_type, {})
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
        return filename.replace("\\", "/")  # Ensure correct path format
    except Exception as e:
        return str(e)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    data = request.get_json()
    url = data.get('url')
    format_type = data.get('format')

    if not url:
        return jsonify({'error': 'Invalid URL'}), 400

    filename = download_video(url, format_type)
    if filename:
        return jsonify({'success': True, 'filename': filename})
    else:
        return jsonify({'error': 'Download failed'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
