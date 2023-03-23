from transformers import CLIPProcessor, CLIPModel
from PIL import Image
from classifiers.classification_common import garbage_classes


def classify_with_clip(image: Image):
    # see details about the model here
    # https://huggingface.co/docs/transformers/model_doc/clip
    model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
    processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

    classes = garbage_classes
    texts = [f"a photo of object(s) made of {elem}" for elem in classes]
    inputs = processor(text=texts, images=image, return_tensors="pt", padding=True)

    outputs = model(**inputs)
    logits_per_image = (
        outputs.logits_per_image
    )  # this is the image-text similarity score
    probs = (
        logits_per_image.softmax(dim=1).detach().numpy()
    )  # we can take the softmax to get the label prob
    return classes[probs.argmax()]
