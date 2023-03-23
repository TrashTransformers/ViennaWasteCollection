from trash_ai import classify_image


def test_classification_plastic():
    result = classify_image(
        "https://www.ikea.com/at/de/images/products/"
        + "spartansk-wasserflasche-klarglas-gruen__1062060_pe850637_s5"
        + ".jpg?f=xl"
    )
    assert result.category == "plastic"
