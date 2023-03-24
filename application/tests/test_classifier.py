from classifiers.clip import classify_with_clip


def test_classification_plastic():
    result = classify_with_clip("../images/paper/paper7.jpg")
    assert result.category == "paper"
