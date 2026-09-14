from gh600.memory import Memory


def test_memory_add_and_history():
    memory = Memory()
    memory.add("user", "hi")
    memory.add("assistant", "hello")

    assert memory.history() == [("user", "hi"), ("assistant", "hello")]


def test_memory_clear():
    memory = Memory()
    memory.add("user", "hi")
    memory.clear()

    assert memory.history() == []
