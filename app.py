import os
from flask import Flask, render_template, request, send_file, make_response
import yt_dlp
import sys


app = Flask(__name__)


# Configuration
DOWNLOAD_FOLDER = 'downloads'
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download_video():
    try:
        print("[LOG] Received download request", file=sys.stderr, flush=True)
        url = request.form.get('url')
        print(f"[LOG] URL: {url}", file=sys.stderr, flush=True)
        if not url:
            return "Error: No URL provided", 400

        # yt-dlp options
        # Prefer MP4. yt-dlp will download and (if needed) remux to MP4.
        ydl_opts = {
            'format': 'bestvideo+bestaudio/best',
            'merge_output_format': 'mp4',
            'outtmpl': os.path.join(app.config['DOWNLOAD_FOLDER'], '%(title)s.%(ext)s'),
            'noplaylist': True,
            'quiet': True,
            'no_warnings': True,
        }


        print("[LOG] Starting download...", file=sys.stderr, flush=True)
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Extract info first to get the filename
            info = ydl.extract_info(url, download=False)
            filename = ydl.prepare_filename(info)
            
            # Download the video
            ydl.download([url])

        print(f"[LOG] Download complete: {filename}", file=sys.stderr, flush=True)
        # Convert to absolute path for send_file
        filepath = os.path.abspath(filename)
        
        # Verify file exists before sending
        if not os.path.exists(filepath):
            return f"Error: File not found at {filepath}", 500
        
        print(f"[LOG] Sending file: {filepath}", file=sys.stderr, flush=True)
        filename = os.path.basename(filepath)

        print(f"[LOG] Preparing streamed response for: {filename}", file=sys.stderr, flush=True)
        response = send_file(
            filepath,
            as_attachment=True,
            download_name=filename,
            mimetype='video/mp4'
        )
        response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'

        print("[LOG] Response prepared", file=sys.stderr, flush=True)
        return response


    except Exception as e:
        print(f"[ERROR] {str(e)}", file=sys.stderr, flush=True)
        import traceback
        traceback.print_exc()
        return f"Error downloading video: {str(e)}", 500

if __name__ == '__main__':
    app.run(debug=False, port=5000)