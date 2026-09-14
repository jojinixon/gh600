from gh600.tools import add, get_word_length


def test_add():
    assert add(2, 3) == 5


def test_get_word_length():
    assert get_word_length("hello") == 5
