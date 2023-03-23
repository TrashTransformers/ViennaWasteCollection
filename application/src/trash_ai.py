from PIL import Image
import requests
from classifiers.clip import classify_with_clip

from models import ClassificationResult


def classify_image(input) -> ClassificationResult:
    # check if input is string
    image: Image = None
    if isinstance(input, Image.Image):
        image = input
    else:
        if input.startswith("http"):
            image = Image.open(requests.get(input, stream=True).raw)
        else:
            image = Image.open(input).convert("RGB")

    clip_result = classify_with_clip(image)
    return ClassificationResult(clip_result)
