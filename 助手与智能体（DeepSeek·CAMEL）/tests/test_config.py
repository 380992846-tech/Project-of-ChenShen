import logging

import pytest

from dsh_assistant.config import Settings, build_log_level


def test_from_env_defaults(monkeypatch):
    monkeypatch.setenv("DEEPSEEK_API_KEY", "sk-test")
    monkeypatch.setenv("DSH_TEMPERATURE", "0.5")
    s = Settings.from_env()
    assert s.api_key == "sk-test"
    assert s.base_url == "https://api.deepseek.com"
    assert s.model == "deepseek-chat"
    assert s.temperature == 0.5


def test_validate_requires_key():
    s = Settings(api_key="")
    with pytest.raises(RuntimeError):
        s.validate()


def test_validate_ok_with_key():
    Settings(api_key="sk-x").validate()


def test_build_log_level_mapping():
    assert build_log_level("DEBUG") == logging.DEBUG
    assert build_log_level("INFO") == logging.INFO
    assert build_log_level("info") == logging.INFO
    assert build_log_level("garbage") == logging.INFO
