from models import ClassificationResult
from recycling_point import RecyclingPointMapper


def test_mapping():
    assert map("glass") == "old glass container"
    assert map("plastic") == "yellow container"
    assert map("paper") == "paper container"
    assert map("metal") == "yellow container"


def map(category: str):
    classification = ClassificationResult(category, 1.0)
    mapper = RecyclingPointMapper()
    return mapper.get_recycling_point(classification)
