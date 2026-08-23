from dsh_assistant.prompts import (
    CAMEL_HELP,
    CAMEL_SYSTEM_PROMPT,
    VOICE_HELP,
    VOICE_SYSTEM_PROMPT,
)


def test_voice_prompt_mentions_persona():
    assert "小DeepSeek" in VOICE_SYSTEM_PROMPT
    assert "兄弟" in VOICE_SYSTEM_PROMPT


def test_camel_prompt_mentions_persona():
    assert "陈深" in CAMEL_SYSTEM_PROMPT


def test_help_texts_not_empty():
    assert VOICE_HELP.strip()
    assert CAMEL_HELP.strip()
