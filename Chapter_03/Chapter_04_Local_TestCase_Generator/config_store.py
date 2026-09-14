import json
from pathlib import Path

CONFIG_FILE = Path(__file__).resolve().parent / "settings.json"

DEFAULT_SETTINGS = {
    "jira_url": "",
    "jira_email": "",
    "jira_api_token": "",
    "provider": "ollama",
    "groq_api_key": "",
    "ollama_base_url": "http://localhost:11434",
    "ollama_model": "gemma3:1b",
}


def load_settings():
    if not CONFIG_FILE.exists():
        return DEFAULT_SETTINGS.copy()

    try:
        with CONFIG_FILE.open("r", encoding="utf-8") as file:
            stored = json.load(file)
    except (json.JSONDecodeError, OSError):
        return DEFAULT_SETTINGS.copy()

    merged = DEFAULT_SETTINGS.copy()
    if isinstance(stored, dict):
        merged.update(stored)
    return merged


def save_settings(new_values):
    current = load_settings()
    if not isinstance(new_values, dict):
        raise TypeError("new_values must be a dictionary of settings")

    current.update(new_values)
    with CONFIG_FILE.open("w", encoding="utf-8") as file:
        json.dump(current, file, indent=2)

    return current
