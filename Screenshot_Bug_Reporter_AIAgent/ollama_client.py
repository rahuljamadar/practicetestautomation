import base64
import json
from typing import Any

import requests

from models import validate_bug_report


class OllamaError(RuntimeError):
    pass


def analyze_screenshot(content: bytes, mime_type: str, context: str, base_url: str, model: str, timeout: int) -> dict[str, Any]:
    prompt = f"""Analyze this UI screenshot as a QA engineer. Return only valid JSON, with no Markdown fences.
Use exactly these fields: title, summary, steps_to_reproduce, expected_result, actual_result,
environment, severity, priority, labels, confidence, assumptions.
Infer only what the screenshot supports. Put uncertain details in assumptions.
Optional reporter context: {context or 'None provided'}"""
    payload = {
        "model": model,
        "prompt": prompt,
        "images": [base64.b64encode(content).decode("ascii")],
        "stream": False,
        "format": "json",
    }
    try:
        response = requests.post(f"{base_url}/api/generate", json=payload, timeout=timeout)
        response.raise_for_status()
        raw = response.json().get("response", "")
        report = json.loads(raw)
    except (requests.RequestException, ValueError, json.JSONDecodeError) as exc:
        raise OllamaError(f"Ollama analysis failed: {exc}") from exc

    validation = validate_bug_report(report)
    if not validation.valid:
        raise OllamaError("Ollama returned an invalid bug report: " + "; ".join(validation.errors))
    return report
