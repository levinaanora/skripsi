# load libraries
from flask import send_from_directory
from flask import Flask, render_template, request, Response, send_file, redirect, jsonify, url_for, flash
from warnings import filterwarnings
from yolov5 import load
import os

app = Flask(__name__, static_folder = "static")
app.config["IMAGE_UPLOADS"] = "static/styles/"
filterwarnings('ignore')

model = load('static/models/best.pt')

@app.route('/upload-image', methods=['GET', 'POST'])
def upload_image():
    if request.method == "POST":
        if request.files:
            try:
                image = request.files["image"]
                image.save(os.path.join(app.config["IMAGE_UPLOADS"], image.filename))
            except:
                pass
            return render_template("upload.html", uploaded_image=image.filename)
    return render_template("upload.html")


@app.route('/uploads/<filename>')
def send_uploaded_file(filename=''):
    # object detection model applied
    results = model('static/styles/' + filename, size=640)
    results.save('static/styles/')
    return send_from_directory(app.config["IMAGE_UPLOADS"], filename)

if __name__ == "__main__":
    app.run(debug = True, use_reloader = True, host = "0.0.0.0")