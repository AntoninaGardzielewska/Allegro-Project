from src.my_project.hello import hello


def test_hello():
    assert hello("World") == "Hello, World!"
    assert hello("") == "Hello, !"
