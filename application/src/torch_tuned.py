import os
import requests
import torch
from PIL import Image
import torchvision.models as models
import torch.nn as nn
import torch.nn.functional as F
import torchvision.transforms as transforms
from classifiers.clip import classify_with_clip

from models import ClassificationResult
import __main__


classes = [
    "other",  # wrong label
    "other",  # wrong label
    "paper",  # cardboad - paper
    "other",  # wrong label
    "glass",  # glass
    "metal",  # metal
    "paper",  # paper
    "plastic",  # plastic
    "clothes",  # wrong label
    "plastic",  # wrong label
]


# classes = [
#     "metal", # wrong label
#     "glass", # wrong label
#     "biological",  # cardboad - paper
#     "paper", # wrong label
#     "battery",  # glass
#     "trash",  # metal
#     "cardboard",  # paper
#     "shoes",  # plastic
#     "clothes", # wrong label
#     "plastic", # wrong label
# ]


def accuracy(outputs, labels):
    _, preds = torch.max(outputs, dim=1)
    return torch.tensor(torch.sum(preds == labels).item() / len(preds))


class ImageClassificationBase(nn.Module):
    def training_step(self, batch):
        images, labels = batch
        out = self(images)  # Generate predictions
        loss = F.cross_entropy(out, labels)  # Calculate loss
        return loss

    def validation_step(self, batch):
        images, labels = batch
        out = self(images)  # Generate predictions
        loss = F.cross_entropy(out, labels)  # Calculate loss
        acc = accuracy(out, labels)  # Calculate accuracy
        return {"val_loss": loss.detach(), "val_acc": acc}

    def validation_epoch_end(self, outputs):
        batch_losses = [x["val_loss"] for x in outputs]
        epoch_loss = torch.stack(batch_losses).mean()  # Combine losses
        batch_accs = [x["val_acc"] for x in outputs]
        epoch_acc = torch.stack(batch_accs).mean()  # Combine accuracies
        return {"val_loss": epoch_loss.item(), "val_acc": epoch_acc.item()}

    def epoch_end(self, epoch, result):
        print(
            "Epoch {}: train_loss: {:.4f}, val_loss: {:.4f}, val_acc: {:.4f}".format(
                epoch + 1, result["train_loss"], result["val_loss"], result["val_acc"]
            )
        )


class ResNet(ImageClassificationBase):
    def __init__(self):
        super().__init__()
        # Use a pretrained model
        self.network = models.resnet50(pretrained=True)
        # Replace last layer
        num_ftrs = self.network.fc.in_features
        self.network.fc = nn.Linear(num_ftrs, len(classes))

    def forward(self, xb):
        return torch.sigmoid(self.network(xb))


model_path = os.getcwd() + "/final_model.pt"

setattr(__main__, "ResNet", ResNet)

model = torch.load(model_path, map_location=torch.device("cpu"))
print("model loaded")


def to_device(data):
    device = torch.device("cpu")
    """Move tensor(s) to chosen device"""
    if isinstance(data, (list, tuple)):
        return [to_device(x, device) for x in data]
    return data.to(device, non_blocking=True)


def predict_image(img, model):
    # Convert to a batch of 1
    xb = to_device(img.unsqueeze(0))
    # Get predictions from model
    yb = model(xb)
    # Pick index with highest probability
    prob, preds = torch.max(yb, dim=1)
    # Retrieve the class label
    return classes[preds[0].item()]


transformations = transforms.Compose(
    [transforms.Resize((256, 256)), transforms.ToTensor()]
)


def predict_external_image(image):
    try:
        example_image = transformations(image)
        prediction = predict_image(example_image, model)
        print("The image resembles", prediction + ".")
        return prediction
    except Exception as e:
        print(e)
        return


def classify_with_resnet(input):
    image = None
    if isinstance(input, Image.Image):
        image = input
    else:
        if input.startswith("http"):
            image = Image.open(requests.get(input, stream=True).raw)
        else:
            image = Image.open(input)
    try:
        prediction = predict_external_image(image)
    except Exception as e:
        print(e)
        result = classify_with_clip(image)
        if "glass" in result.category:
            result.category = "glass"
            return result

    return ClassificationResult(prediction, 0)
