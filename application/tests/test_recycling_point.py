from models import ClassificationResult
from recycling_point import RecyclingPointMapper


def test_mapping():
    assert map("paper") == "paper container"


def map(category: str):
    classification = ClassificationResult(category)
    mapper = RecyclingPointMapper()
    return mapper.get_recycling_point(classification)
