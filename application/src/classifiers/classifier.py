from PIL import Image
import requests
from classifiers.clip import classify_with_clip

from models import ClassificationResult


def classify_image(file_location: str) -> ClassificationResult:
    image = Image.open(requests.get(file_location, stream=True).raw)
    clip_result = classify_with_clip(image)
    return ClassificationResult(clip_result)
