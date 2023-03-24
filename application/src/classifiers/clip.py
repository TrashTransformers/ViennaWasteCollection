import requests
from transformers import CLIPProcessor, CLIPModel
from PIL import Image

from models import ClassificationResult

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

    classes_with_category = {
        # "food": "organic",
        "glass": "glass",
        "metal": "metal",
        "paper": "paper",
        # "something else": "residual waste",
        "plastic": "plastic",
    }
    classes = list(classes_with_category.keys())
    texts = [f"a photo of object(s) made of {elem}" for elem in classes]
    inputs = processor(text=texts, images=image, return_tensors="pt", padding=True)

    outputs = model(**inputs)
    logits_per_image = (
        outputs.logits_per_image
    )  # this is the image-text similarity score
    probs = (
        logits_per_image.softmax(dim=1).detach().numpy()
    )  # we can take the softmax to get the label prob
    determined_class = classes_with_category[probs.argmax()]
    prob = probs[0][probs.argmax()]
    if prob < 70:
        # get the second best
        probs[0][probs.argmax()] = 0
        second_best_determined_class = classes[probs.argmax()]
        classes = [determined_class, second_best_determined_class]
        text = [f"a photo of an object made of {elem}" for elem in classes]
        probs = get_probs(text)
        prob = probs[0][probs.argmax()]
        determined_class = classes_with_category[probs.argmax()]
        prob = probs[0][probs.argmax()]
    return ClassificationResult(classes_with_category[determined_class], prob)


def get_probs(text: str, image):
    inputs = processor(text=[text], images=image, return_tensors="pt", padding=True)

    outputs = model(**inputs)
    logits_per_image = (
        outputs.logits_per_image
    )  # this is the image-text similarity score
    probs = (
        logits_per_image.softmax(dim=1).detach().numpy()
    )  # we can take the softmax to get the label prob

    return probs
