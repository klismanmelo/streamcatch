from flask import Flask, render_template, request, redirect, jsonify
from pytubefix import YouTube
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app) # Permite que o Flet (front) acesse a API

DOWNLOAD_FOLDER = "downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

@app.route('/')
def dashboard():
    return render_template('index.html')

@app.route('/download', methods=["POST"])
def download():
    data = request.json
    url = data.get("url")

    if not url:
        return jsonify({"error": "URL não fornecida"}), 400

    try:
        yt = YouTube(url)
        stream = yt.streams.get_highest_resolution()
        filepath = os.path.join(DOWNLOAD_FOLDER, f"{yt.title}.mp4")
        filename = f"{yt.title}.mp4"
        stream.download(output_path=DOWNLOAD_FOLDER, filename=filename)

        #return redirect('/')
        return jsonify({"message": "Download concluído!", "filename": filename, "path": filepath}), 200
    except Exception as e:
        #return redirect('/')
        return jsonify({"error": str(e)}), 500

    

if __name__ == '__main__':
    with app.app_context():
        app.run(debug=True, port=5432)