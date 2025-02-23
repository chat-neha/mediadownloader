from flask import Flask, render_template, request, jsonify
import os
import yt_dlp

app = Flask(__name__)

# Ensure 'static/downloads' and 'static/cookies' directories exist
DOWNLOAD_FOLDER = "static/downloads"
COOKIES_FOLDER = "static/cookies"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)
os.makedirs(COOKIES_FOLDER, exist_ok=True)

COOKIE_FILE = os.path.join(COOKIES_FOLDER, "cookies.txt")

def sanitize_filename(filename):
    """ Ensure safe filenames by removing problematic characters """
    return "".join(c if c.isalnum() or c in " ._-" else "_" for c in filename)

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

    # If a cookie file exists, use it
    if os.path.exists(COOKIE_FILE):
        options['mp4']['cookiefile'] = COOKIE_FILE
        options['mp3']['cookiefile'] = COOKIE_FILE

    ydl_opts = options.get(format_type, {})
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = sanitize_filename(ydl.prepare_filename(info))
        return filename.replace("\\", "/")  # Ensure correct path format
    except Exception as e:
        return f"Download Error: {str(e)}"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload_cookies', methods=['POST'])
def upload_cookies():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    file.save(COOKIE_FILE)
    return jsonify({'success': True, 'message': 'Cookies uploaded successfully!'})

@app.route('/download', methods=['POST'])
def download():
    data = request.get_json()
    url = data.get('url')
    format_type = data.get('format')

    if not url:
        return jsonify({'error': 'Invalid URL'}), 400

    filename = download_video(url, format_type)
    if filename and "Download Error" not in filename:
        return jsonify({'success': True, 'filename': filename})
    else:
        return jsonify({'error': filename}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
