from models import ClassificationResult

mapping = {
    "colored glass": "colored old glass container",
    "white glass": "white old glass container",
    "plastic": "yellow container",
    "paper": "paper container",
    "organic": "bio container",
    "metal": "yellow container",
    "residual": "residual container",
}


class RecyclingPointMapper:
    def __init__(self):
        pass

    def get_recycling_point(self, classification: ClassificationResult):
        return mapping[classification.category]
