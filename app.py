from flask import Flask, render_template, request, send_file
import yt_dlp
import os
import uuid

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form['url']
        download_dir = 'downloads'
        os.makedirs(download_dir, exist_ok=True)
        video_id = str(uuid.uuid4())
        output_path = os.path.join(download_dir, f"{video_id}.mp4")

        ydl_opts = {
            'outtmpl': output_path,
            'format': 'best[ext=mp4]/best',
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            return send_file(output_path, as_attachment=True)
        except Exception as e:
            return f"Error: {e}"

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
