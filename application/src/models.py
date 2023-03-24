class ClassificationResult:
    def __init__(self, category: str, probability: float):
        self.category = category
        self.probability = probability


class RecyclingPoint:
    def __init__(self, name: str):
        self.name = name
