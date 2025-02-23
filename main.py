from flask import Flask, render_template, request, jsonify
import os
import yt_dlp

app = Flask(__name__)

# Ensure 'static/downloads' directory exists
DOWNLOAD_FOLDER = "static/downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

def sanitize_filename(filename):
    """ Ensure safe filenames by removing problematic characters """
    return "".join(c if c.isalnum() or c in " ._-" else "_" for c in filename)

def download_video(url, format_type):
    options = {
        'mp4': {
            'format': 'bestvideo+bestaudio/best',
            'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(title)s.mp4'),
            'postprocessors': [{'key': 'FFmpegVideoConvertor', 'preferedformat': 'mp4'}],
            'nocheckcertificate': True,  # Bypass SSL issues
            'force-ipv4': True,  # Avoid captcha verification
            'ignoreerrors': True,  # Continue on minor errors
            'fallback-format': '18'  # Fallback to MP4 360p if best fails
        },
        'mp3': {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(title)s.mp3'),
            'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': '192'}],
            'nocheckcertificate': True,
            'force-ipv4': True,
            'ignoreerrors': True
        }
    }

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
