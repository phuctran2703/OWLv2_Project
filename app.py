from flask import Flask, request, render_template, jsonify
import subprocess
import json
import io
from model import process_image
from PIL import Image

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'image' not in request.files or 'text' not in request.form:
        return "No file or text part", 400

    file = request.files['image']
    texts = request.form.get('text').split(",")

    if file.filename == '':
        return "No selected file", 400

    # Read the image in memory
    image_bytes = file.read()

    # Call the model.py script
    result = process_image(image_bytes, texts)
    
    return result

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
