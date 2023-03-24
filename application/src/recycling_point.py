from models import ClassificationResult

mapping = {
    "glass": "old glass container",
    "plastic": "yellow container",
    "paper": "paper container",
    "metal": "yellow container",
}


class RecyclingPointMapper:
    def __init__(self):
        pass

    def get_recycling_point(self, classification: ClassificationResult):
        return mapping[classification.category]
