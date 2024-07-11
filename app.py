from flask import Flask, request, render_template, jsonify
import os
import json
import subprocess

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'image' not in request.files or 'text' not in request.form:
        return "No file or text part", 400

    file = request.files['image']
    texts = request.form.get('text')

    if file.filename == '':
        return "No selected file", 400

    image_path = "static/uploaded_image.jpg"
    file.save(image_path)

    # Call the model.py script
    result = subprocess.run(
        ['python', 'model.py', image_path, texts],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        return "Error processing image", 500

    response = json.loads(result.stdout)

    # Save the JSON response to a file
    json_output_path = "static/result.json"
    with open(json_output_path, "w") as json_file:
        json.dump(response, json_file, indent=2)

    return jsonify({
        'image_url': image_path,
        'json_url': json_output_path
    })

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
