from flask import Flask, request, render_template, send_file
import os
from PIL import Image, ImageDraw, ImageFont
import torch
from transformers import AutoProcessor, Owlv2ForObjectDetection

app = Flask(__name__)

processor = AutoProcessor.from_pretrained("google/owlv2-base-patch16-ensemble")
model = Owlv2ForObjectDetection.from_pretrained("google/owlv2-base-patch16-ensemble")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'image' not in request.files or 'text' not in request.form:
        return "No file or text part", 400

    file = request.files['image']
    texts = request.form.get('text').split(',')

    if file.filename == '':
        return "No selected file", 400

    image = Image.open(file.stream)
    inputs = processor(text=[texts], images=image, return_tensors="pt")

    with torch.no_grad():
        outputs = model(**inputs)

    target_sizes = torch.Tensor([image.size[::-1]])
    results = processor.post_process_object_detection(
        outputs=outputs, threshold=0.2, target_sizes=target_sizes
    )

    i = 0  # Retrieve predictions for the first image for the corresponding text queries
    boxes, scores, labels = results[i]["boxes"], results[i]["scores"], results[i]["labels"]
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default()

    for box, score, label in zip(boxes, scores, labels):
        box = [round(i, 2) for i in box.tolist()]
        draw.rectangle(box, outline="green", width=3)
        draw.text((box[0], box[1]), f"{texts[label]}: {round(score.item(), 3)}", fill="yellow", font=font)

    output_path = "static/annotated_image.jpg"
    image.save(output_path)
    return send_file(output_path, mimetype='image/jpeg')

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
