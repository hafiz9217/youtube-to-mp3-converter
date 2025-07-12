from flask import Flask, render_template, request, send_file
from pytube import YouTube
import os
import uuid
from pytube.request import default_range_size, head, get

# Patch to add browser-like headers
import pytube.request
pytube.request.default_headers['User-Agent'] = (
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
    '(KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36'
)

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    url = request.form['url']
    try:
        yt = YouTube(url)
        audio_stream = yt.streams.filter(only_audio=True).first()
        filename = f"{uuid.uuid4()}.mp4"
        out_file = audio_stream.download(filename=filename)
        mp3_file = filename.replace(".mp4", ".mp3")
        os.rename(out_file, mp3_file)

        return send_file(mp3_file, as_attachment=True)
    except Exception as e:
        return f"❌ Error: {str(e)}"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=81)
