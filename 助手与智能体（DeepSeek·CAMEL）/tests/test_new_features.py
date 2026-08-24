"""覆盖新增深化功能：工具注册/安全计算、记忆覆盖、/rewrite 消息构造与流式解析。"""

from __future__ import annotations

import pytest

from dsh_assistant import agentic, assistant, camel_agent, tools
from dsh_assistant.config import Settings
from dsh_assistant.llm import LLMClient
from dsh_assistant.memory import MemoryStore

# ---- 工具 ----

def test_safe_calculate():
    assert tools.safe_calculate("(2+3)*4") == 20.0
    assert tools.safe_calculate("2**10") == 1024.0
    assert tools.safe_calculate("10//3") == 3.0
    assert abs(tools.safe_calculate("-5 + 3") - (-2.0)) < 1e-9


def _raises(expr: str) -> bool:
    try:
        tools.safe_calculate(expr)
    except (SyntaxError, ValueError):
        return True
    return False


def test_safe_calculate_rejects_arbitrary_code():
    for bad in ["__import__('os')", "os.system('ls')", "lambda: 1", "a+b"]:
        assert _raises(bad), f"应拒绝表达式: {bad}"


def test_tool_schemas_and_run_tool():
    schemas = tools.tool_schemas()
    assert len(schemas) == 3
    assert schemas[0]["type"] == "function"
    names = tools.available_names()
    assert names == ["calculate", "current_time", "roll_dice"]

    assert "=" in tools.run_tool("calculate", {"expression": "3*7"})
    assert "当前" not in tools.run_tool("current_time", {})  # 只要不抛异常即可
    assert tools.run_tool("current_time", {}).strip() != ""
    assert "未知工具" in tools.run_tool("nope", {})


# ---- 记忆覆盖 ----

def test_replace_last_assistant(tmp_path):
    m = MemoryStore(tmp_path / "h.json", "sys", 3)
    m.add("user", "hello")
    m.add("assistant", "old")
    assert m.last_pair() == ("hello", "old")
    assert m.replace_last_assistant("new") is True
    assert m.snapshot()[-1]["content"] == "new"


def test_last_pair_none_and_replace_missing(tmp_path):
    m = MemoryStore(tmp_path / "h.json", "sys", 3)
    m.add("user", "only-user")
    assert m.last_pair() is None
    assert m.replace_last_assistant("x") is False  # 没有 assistant 消息


# ---- /rewrite 消息构造（离线，monkeypatch LLM）----

def test_assistant_rewrite_overwrites(tmp_path, monkeypatch):
    settings = Settings(api_key="sk-x")
    a = assistant.VoiceAssistant(settings)
    a.memory = MemoryStore(tmp_path / "h.json", settings.voice_system_prompt, 3)
    a.memory.add("user", "怎么算 8*7？")
    a.memory.add("assistant", "56")
    monkeypatch.setattr(a.llm, "chat", lambda messages: "56，这是正确答案。")
    new = a.rewrite_last()
    assert new == "56，这是正确答案。"
    assert a.memory.snapshot()[-1]["content"] == "56，这是正确答案。"


def test_camel_rewrite_overwrites(monkeypatch):
    settings = Settings(api_key="sk-x")
    ca = camel_agent.CamelChatAgent(settings)
    ca.history = [("晓晓", "今天星期几？"), ("陈深", "今天是周一。")]
    monkeypatch.setattr(ca.rewrite_llm, "chat", lambda messages: "今天是周一。")
    new = ca.rewrite_last()
    assert new == "今天是周一。"
    assert ca.history[-1] == ("陈深", "今天是周一。")


def test_agent_rewrite_overwrites(monkeypatch):
    settings = Settings(api_key="sk-x")
    ag = agentic.ToolAgent(settings)
    ag.history = [{"role": "user", "content": "1+1?"}, {"role": "assistant", "content": "2"}]
    monkeypatch.setattr(ag.llm, "chat", lambda messages, model=None: "2。")
    new = ag.rewrite_last()
    assert new == "2。"
    assert ag.history[-1] == {"role": "assistant", "content": "2。"}
    # 历史不足时返回 None
    ag.history = [{"role": "user", "content": "x"}]
    assert ag.rewrite_last() is None


# ---- 流式解析 ----

def test_stream_yields_chunks(monkeypatch):
    class FakeDelta:
        content = "你"

    class FakeChoice:
        delta = FakeDelta()

    class FakeChunk:
        def __init__(self):
            self.choices = [FakeChoice()]

    class FakeCompletions:
        def create(self, **kwargs):
            assert kwargs["stream"] is True
            return iter([FakeChunk(), FakeChunk()])

    class FakeChat:
        completions = FakeCompletions()

    class FakeClient:
        chat = FakeChat()

    llm = LLMClient(Settings(api_key="sk-x"))
    monkeypatch.setattr(llm, "_get_client", lambda: FakeClient())
    out = "".join(list(llm.stream([{"role": "user", "content": "hi"}])))
    assert out == "你你"


# ---- 多模型配置与 Web 后端 ----

def test_model_ids_defaults_and_override():
    s = Settings(api_key="x", model="deepseek-chat")
    ids = s.model_ids()
    assert ids == {
        "pro": "deepseek-v4-pro",
        "flash": "deepseek-v4-flash",
        "vision": "deepseek-v4-flash-vision-exp",
    }
    # 显式覆盖；留空则回退到 self.model
    s2 = Settings(api_key="x", model="deepseek-chat", model_pro="custom-pro", model_flash="")
    assert s2.model_ids()["pro"] == "custom-pro"
    assert s2.model_ids()["flash"] == "deepseek-chat"


def test_model_catalog():
    s = Settings(api_key="x", model="deepseek-chat", model_flash="v4-flash")
    cat = s.model_catalog()
    assert len(cat) == 3
    assert {c["label"] for c in cat} == {"V4 Pro", "V4 Flash", "V4 Flash 视觉"}
    flash = next(c for c in cat if c["key"] == "flash")
    assert flash["model_id"] == "v4-flash"


def test_web_meta_and_index():
    pytest.importorskip("fastapi")
    from fastapi.testclient import TestClient

    from dsh_assistant.web import app

    client = TestClient(app)
    meta = client.get("/api/meta")
    assert meta.status_code == 200
    assert len(meta.json()["models"]) == 3
    assert len(meta.json()["modes"]) == 2
    index = client.get("/")
    assert index.status_code == 200
    assert "小深" in index.text
