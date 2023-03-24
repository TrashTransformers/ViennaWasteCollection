from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials
from dotenv import find_dotenv, load_dotenv


import os


load_dotenv(find_dotenv())
load_dotenv(find_dotenv(".env.shared"))

subscription_key = os.getenv("AZURE_COMPUTER_VISION_KEY")
endpoint = "https://trash-ai.cognitiveservices.azure.com/"

computervision_client = ComputerVisionClient(
    endpoint, CognitiveServicesCredentials(subscription_key)
)


def describe_image(local_image_path: str) -> str:

    analyze_result = computervision_client.analyze_image_in_stream(
        open(local_image_path, "rb"),
        visual_features=[
            VisualFeatureTypes.categories,
            VisualFeatureTypes.tags,
            VisualFeatureTypes.objects,
            VisualFeatureTypes.description,
        ],
    )

    description = ""
    captions = " ".join(
        [str(elem.text) for i, elem in enumerate(analyze_result.description.captions)]
    )
    description += "Description: " + captions + "."

    tags = " ".join([str(elem.name) for i, elem in enumerate(analyze_result.tags)])
    description += " Tags: " + tags + "."

    if (
        len(analyze_result.categories) > 0
        and analyze_result.categories[0].name != "others_"
    ):
        description += (
            description
            + " Categories: "
            + " ".join(
                [str(elem.name) for i, elem in enumerate(analyze_result.categories)]
                + "."
            )
        )

    return description
