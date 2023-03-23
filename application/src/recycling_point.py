from models import ClassificationResult

mapping = {
    "glass": "glass container",
    "plastic": "plastic container",
    "paper": "paper container",
}


class RecyclingPointMapper:
    def __init__(self):
        pass

    def get_recycling_point(self, classification: ClassificationResult):
        return mapping[classification.material]
