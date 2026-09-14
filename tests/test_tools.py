from gh600.tools import add, get_word_length, lookup_fact


def test_add():
    assert add(2, 3) == 5


def test_get_word_length():
    assert get_word_length("hello") == 5


def test_lookup_fact_known_topic():
    assert "Python" in lookup_fact("python")


def test_lookup_fact_is_case_insensitive():
    assert lookup_fact("Python") == lookup_fact("python")


def test_lookup_fact_unknown_topic():
    assert lookup_fact("banana") == "No fact found for 'banana'."
