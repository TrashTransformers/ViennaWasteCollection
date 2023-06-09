import requests
from transformers import CLIPProcessor, CLIPModel
from PIL import Image

from models import ClassificationResult
from classifiers.classification_common import garbage_classes, classes_with_category

# see details about the model here
# https://huggingface.co/docs/transformers/model_doc/clip
model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")


def classify_with_clip(input):
    image = None
    if isinstance(input, Image.Image):
        image = input
    else:
        if input.startswith("http"):
            image = Image.open(requests.get(input, stream=True).raw)
        else:
            image = Image.open(input).convert("RGB")


    texts = [f"a photo of object(s) made of {elem}" for elem in garbage_classes]
    inputs = processor(text=texts, images=image, return_tensors="pt", padding=True)

    outputs = model(**inputs)
    logits_per_image = (
        outputs.logits_per_image
    )  # this is the image-text similarity score
    probs = (
        logits_per_image.softmax(dim=1).detach().numpy()
    )  # we can take the softmax to get the label prob
    determined_class = garbage_classes[probs.argmax()]
    return ClassificationResult(
        classes_with_category[determined_class], probs[0][probs.argmax()]
    )
