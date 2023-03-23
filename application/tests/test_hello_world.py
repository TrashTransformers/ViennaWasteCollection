from module import get_hello_text


def test_hello():
    assert get_hello_text("Trash") == "Hello Trash"
