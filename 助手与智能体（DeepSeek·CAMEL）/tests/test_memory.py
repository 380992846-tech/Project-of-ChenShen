from dsh_assistant.memory import MemoryStore


def test_init_adds_system(tmp_path):
    m = MemoryStore(tmp_path / "h.json", "sys", 3)
    assert m.messages[0]["role"] == "system"
    assert m.messages[0]["content"] == "sys"
    assert m.is_empty() is True


def test_add_persists_across_reload(tmp_path):
    p = tmp_path / "h.json"
    m = MemoryStore(p, "sys", 3)
    m.add("user", "hi")
    m.add("assistant", "hello")
    m2 = MemoryStore(p, "sys", 3)
    assert m2.messages[-2:] == [
        {"role": "user", "content": "hi"},
        {"role": "assistant", "content": "hello"},
    ]


def test_clear_keeps_system(tmp_path):
    m = MemoryStore(tmp_path / "h.json", "sys", 3)
    m.add("user", "a")
    m.add("assistant", "b")
    m.clear()
    assert len(m.messages) == 1
    assert m.messages[0]["role"] == "system"


def test_trim_keeps_system_and_recent(tmp_path):
    m = MemoryStore(tmp_path / "h.json", "sys", 2)
    for i in range(10):
        m.add("user", f"u{i}")
        m.add("assistant", f"a{i}")
    # 1 system + 最近 2 轮 = 1 + 4 条
    assert len(m.messages) == 1 + 2 * 2


def test_snapshot_and_recent(tmp_path):
    m = MemoryStore(tmp_path / "h.json", "sys", 10)
    m.add("user", "u1")
    m.add("assistant", "a1")
    assert len(m.recent(1)) == 1
    assert len(m.snapshot()) == 3
