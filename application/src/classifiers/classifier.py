from PIL import Image
import requests
from classifiers.clip import classify_with_clip

from models import ClassificationResult


def classify_image(file_location: str) -> ClassificationResult:
    url = "https://img.fruugo.com/product/2/06/264676062_max.jpg"
    image = Image.open(requests.get(url, stream=True).raw)
    clip_result = classify_with_clip(image)
    return ClassificationResult(clip_result)
