from classifiers.azure_computer_vision import demo_call
from trash_ai import classify_image


def test_classification_plastic():
    result = classify_image("../images/paper/paper7.jpg")
    assert result.category == "paper"


def test_azure_computer_vision():
    result = demo_call("../images/paper/paper10.jpg")
    print(result)
    assert len(result) > 0
