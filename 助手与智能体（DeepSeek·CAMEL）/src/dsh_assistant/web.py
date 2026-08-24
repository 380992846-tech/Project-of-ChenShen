"""FastAPI 后端：多模型对话 Web 界面。

- ``GET  /``                —— 返回玻璃拟态前端页面；
- ``GET  /api/meta``        —— 模型与操作目录；
- ``POST /api/chat``        —— 一次性对话（chat / agent）；
- ``POST /api/chat/stream`` —— SSE 流式对话；
- ``POST /api/rewrite``     —— 重写并覆盖上一条回复；
- ``POST /api/clear``       —— 清空当前模式上下文；
- ``POST /api/tts``         —— Edge TTS 合成语音（MP3 流）。

模型标识由前端传入（取自目录，也可被用户编辑），后端直接使用；
``base_url`` / ``api_key`` 沿用 ``DEEPSEEK_*`` 环境变量。
"""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any

from fastapi import FastAPI
from fastapi.responses import HTMLResponse, StreamingResponse
from pydantic import BaseModel

from .agentic import ToolAgent
from .config import MODEL_CATALOG, Settings
from .llm import LLMClient, LLMError
from .memory import MemoryStore
from .prompts import REWRITE_INSTRUCTION

logger = logging.getLogger(__name__)

app = FastAPI(title="dsh-assistant web", version="0.2.0")

_INDEX = Path(__file__).parent / "web" / "index.html"

_settings: Settings | None = None
_llm: LLMClient | None = None
_sessions: dict[str, SessionState] = {}


def get_settings() -> Settings:
    global _settings
    if _settings is None:
        _settings = Settings.from_env()
    return _settings


def get_llm(settings: Settings) -> LLMClient:
    global _llm
    if _llm is None:
        _llm = LLMClient(settings)
    return _llm


class SessionState:
    """按会话保存 chat / agent 两套独立上下文。"""

    def __init__(self, sid: str):
        self.sid = sid
        self.memory: MemoryStore | None = None
        self.agent: ToolAgent | None = None

    def ensure_memory(self, settings: Settings) -> MemoryStore:
        if self.memory is None:
            path = settings.data_dir / "web_sessions" / f"{self.sid}.json"
            self.memory = MemoryStore(path, settings.voice_system_prompt, settings.max_rounds)
        return self.memory

    def ensure_agent(self, settings: Settings) -> ToolAgent:
        if self.agent is None:
            self.agent = ToolAgent(settings)
        return self.agent


def get_session(sid: str) -> SessionState:
    if sid not in _sessions:
        _sessions[sid] = SessionState(sid)
    return _sessions[sid]


# ---- 请求模型 ----

class ChatRequest(BaseModel):
    session: str = "default"
    mode: str = "chat"
    model: str | None = None
    message: str = ""


class RewriteRequest(BaseModel):
    session: str = "default"
    mode: str = "chat"
    model: str | None = None


class ClearRequest(BaseModel):
    session: str = "default"
    mode: str = "chat"


class TTSRequest(BaseModel):
    text: str = ""


# ---- 前端 ----

@app.get("/", response_class=HTMLResponse)
def index() -> HTMLResponse:
    if _INDEX.exists():
        return HTMLResponse(_INDEX.read_text(encoding="utf-8"))
    return HTMLResponse("<h2>前端页面缺失</h2>", status_code=500)


@app.get("/api/meta")
def meta() -> dict[str, Any]:
    settings = get_settings()
    ids = settings.model_ids()
    models = [{**entry, "model_id": ids[entry["key"]]} for entry in MODEL_CATALOG]
    modes = [
        {"key": "chat", "label": "聊天"},
        {"key": "agent", "label": "工具智能体"},
    ]
    return {"models": models, "modes": modes}


# ---- 对话 ----

def _chat_once(settings: Settings, session: SessionState, mode: str, model: str | None, message: str) -> str:
    if mode == "agent":
        return session.ensure_agent(settings).chat(message, model=model)
    mem = session.ensure_memory(settings)
    mem.add("user", message)
    try:
        reply = get_llm(settings).chat(mem.snapshot(), model=model)
    except LLMError as exc:
        logger.warning("对话失败: %s", exc)
        reply = f"（出错了：{exc}）"
    mem.add("assistant", reply)
    return reply


@app.post("/api/chat")
def chat(req: ChatRequest) -> dict[str, str]:
    settings = get_settings()
    session = get_session(req.session)
    reply = _chat_once(settings, session, req.mode, req.model, req.message)
    return {"reply": reply}


def _sse(data: dict[str, Any]) -> str:
    return f"data: {json.dumps(data, ensure_ascii=False)}\n\n"


@app.post("/api/chat/stream")
def chat_stream(req: ChatRequest) -> StreamingResponse:
    settings = get_settings()
    session = get_session(req.session)
    mode, model, message = req.mode, req.model, req.message

    def gen():
        if mode == "agent":
            # 工具智能体无法逐 token 流式（内部有函数调用），整段返回。
            reply = session.ensure_agent(settings).chat(message, model=model)
            yield _sse({"type": "text", "data": reply})
            yield _sse({"type": "done", "data": ""})
            return
        mem = session.ensure_memory(settings)
        mem.add("user", message)
        parts: list[str] = []
        try:
            for chunk in get_llm(settings).stream(mem.snapshot(), model=model):
                parts.append(chunk)
                yield _sse({"type": "text", "data": chunk})
            reply = "".join(parts).strip() or "（这次没说出话来…）"
        except LLMError as exc:
            logger.warning("流式对话失败: %s", exc)
            reply = f"（出错了：{exc}）"
            yield _sse({"type": "error", "data": reply})
            yield _sse({"type": "done", "data": ""})
            return
        mem.add("assistant", reply)
        yield _sse({"type": "done", "data": ""})

    return StreamingResponse(gen(), media_type="text/event-stream")


# ---- 重写 / 清空 ----

@app.post("/api/rewrite")
def rewrite(req: RewriteRequest) -> dict[str, str | None]:
    settings = get_settings()
    session = get_session(req.session)
    new: str | None = None
    if req.mode == "agent":
        new = session.ensure_agent(settings).rewrite_last(model=req.model)
    else:
        mem = session.ensure_memory(settings)
        pair = mem.last_pair()
        if pair is not None:
            messages = [
                {"role": "system", "content": settings.voice_system_prompt},
                {
                    "role": "user",
                    "content": f"上一轮用户问题：\n{pair[0]}\n\n上一轮助手回复：\n{pair[1]}\n\n{REWRITE_INSTRUCTION}",
                },
            ]
            try:
                new = get_llm(settings).chat(messages, model=req.model)
            except LLMError as exc:
                logger.warning("重写失败: %s", exc)
                new = None
            if new:
                mem.replace_last_assistant(new)
    return {"reply": new}


@app.post("/api/clear")
def clear(req: ClearRequest) -> dict[str, bool]:
    session = get_session(req.session)
    if req.mode == "agent":
        if session.agent is not None:
            session.agent.clear_history()
    else:
        if session.memory is not None:
            session.memory.clear()
    return {"ok": True}


# ---- 语音合成 ----

@app.post("/api/tts")
def tts(req: TTSRequest) -> StreamingResponse:
    settings = get_settings()
    voice = settings.voice

    async def gen():
        import edge_tts

        communicate = edge_tts.Communicate(req.text, voice or "zh-CN-YunxiNeural")
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                yield chunk["data"]

    return StreamingResponse(gen(), media_type="audio/mpeg")


def run(host: str = "127.0.0.1", port: int = 8000, reload: bool = False) -> None:
    import uvicorn

    uvicorn.run(app, host=host, port=port, reload=reload)
