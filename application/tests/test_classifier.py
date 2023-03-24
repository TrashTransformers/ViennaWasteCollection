from trash_ai import classify_image


def test_classification_plastic():
    result = classify_image("../images/paper/paper7.jpg")
    assert result.category == "paper"
