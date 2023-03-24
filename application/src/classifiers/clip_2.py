import requests
from transformers import CLIPProcessor, CLIPModel
from PIL import Image


def classify_with_clip_2(image: Image):
    if isinstance(input, Image.Image):
        image = input
    else:
        if input.startswith("http"):
            image = Image.open(requests.get(input, stream=True).raw)
        else:
            image = Image.open(input).convert("RGB")
    # see details about the model here
    # https://huggingface.co/docs/transformers/model_doc/clip
    model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
    processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

    classes_with_category = {
        "food": "organic",
        "brown glass": "colored glass",
        "green glass": "colored glass",
        "white glass": "white glass",
        "metal": "metal",
        "paper": "paper",
        "something else": "residual waste",
        "plastic": "plastic",
    }
    classes = classes_with_category.keys()
    texts = [f"a photo of object(s) made of {elem}" for elem in classes]
    inputs = processor(text=texts, images=image, return_tensors="pt", padding=True)

    outputs = model(**inputs)
    logits_per_image = (
        outputs.logits_per_image
    )  # this is the image-text similarity score
    probs = (
        logits_per_image.softmax(dim=1).detach().numpy()
    )  # we can take the softmax to get the label prob
    determined_class = classes[probs.argmax()]
    return classes_with_category[determined_class]
