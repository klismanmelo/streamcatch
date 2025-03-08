from flask import Flask, render_template, request, redirect, jsonify
from pytubefix import YouTube
import os

app = Flask(__name__)

DOWNLOAD_FOLDER = "downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

@app.route('/')
def dashboard():
    return render_template('index.html')

@app.route('/download', methods=["POST"])
def download():
    data = request.form['url_video']
    url = data

    if not url:
        return jsonify({"error": "URL não fornecida"}), 400

    try:
        yt = YouTube(url)
        stream = yt.streams.get_highest_resolution()
        filepath = os.path.join(DOWNLOAD_FOLDER, f"{yt.title}.mp4")
        stream.download(output_path=DOWNLOAD_FOLDER, filename=f"{yt.title}.mp4")

        return redirect('/')
    except Exception as e:
        return redirect('/')

    

if __name__ == '__main__':
    with app.app_context():
        app.run(debug=True, port=5432)