import sys
import json
from PIL import Image
import torch
from transformers import AutoProcessor, Owlv2ForObjectDetection
import io

def process_image(image_bytes, texts):
    processor = AutoProcessor.from_pretrained("google/owlv2-base-patch16-ensemble")
    model = Owlv2ForObjectDetection.from_pretrained("google/owlv2-base-patch16-ensemble")

    image = Image.open(io.BytesIO(image_bytes))
    inputs = processor(text=[texts], images=image, return_tensors="pt")

    with torch.no_grad():
        outputs = model(**inputs)

    target_sizes = torch.Tensor([image.size[::-1]])
    results = processor.post_process_object_detection(
        outputs=outputs, threshold=0.2, target_sizes=target_sizes
    )

    i = 0  # Retrieve predictions for the first image for the corresponding text queries
    boxes, scores, labels = results[i]["boxes"], results[i]["scores"], results[i]["labels"]

    response = []
    for box, score, label in zip(boxes, scores, labels):
        box = [round(i, 2) for i in box.tolist()]
        response.append({
            'label': texts[label],
            'box': box,
            'score': round(score.item(), 3)
        })

    return response

if __name__ == '__main__':
    texts = sys.argv[1].split(',')
    image_bytes = sys.stdin.buffer.read()
    result = process_image(image_bytes, texts)
    print(json.dumps(result, indent=2))
