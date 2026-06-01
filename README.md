# Youtube Video Downloader (Flask + yt-dlp)

A simple Flask web application that lets you download the **highest-quality** MP4 of a YouTube video by providing its URL.

## Features
- Web UI (enter YouTube URL, click Download)
- Downloads the best available video/audio and merges/remuxes into **MP4**
- Saves downloads to the local `downloads/` folder
- Streams the downloaded file back to the browser for direct saving

---

## Project Structure

- app.py - Flask server + download endpoint
- templates/index.html - Frontend UI
- static/styles.css - Frontend styling
- downloads/ - Output folder for downloaded videos

---

## Prerequisites
- Python 3.9+ recommended
- Internet access (to download from YouTube)

---

## Setup & Run
### 1) Create a virtual environment
```bash
python -m venv venv
```

### 2) Activate the virtual environment
**Windows (CMD):**
```bash
venv\Scripts\activate
```

### 3) Install dependencies
```bash
pip install flask yt-dlp
```

### 4) Start the app
```bash
python app.py
```

By default, the server runs on:
- **http://127.0.0.1:5000/**

### 5) Download a video
1. Open the URL in your browser.
2. Paste a YouTube link into the input box.
3. Click **Download**.
4. The browser will download the resulting MP4.

---

## How It Works
- Frontend sends the `url` to `POST /download` using `fetch()`.
- Backend uses `yt_dlp` to:
  - fetch metadata first (to compute the expected filename)
  - download the media
  - ensure merge/remux output is `mp4`
- Backend streams the created file back using `send_file(..., as_attachment=True)`.

---

## Notes / Known Limitations
- Download time depends on your connection and the video size.
- Some YouTube videos may fail due to restrictions or changes in available streams.
- The downloaded file is saved in `downloads/` using `%(title)s.%(ext)s`.

---

## Troubleshooting
### 1) “ModuleNotFoundError”
Make sure you activated the virtual environment and re-ran:
```bash
pip install flask yt-dlp
```

### 2) App starts but downloading fails
- Check the console/log output from `app.py` (it prints URL + progress/errors).
- Try another video URL.

### 3) File not found errors
- Ensure the `downloads/` directory exists (it is created automatically on startup).

---

