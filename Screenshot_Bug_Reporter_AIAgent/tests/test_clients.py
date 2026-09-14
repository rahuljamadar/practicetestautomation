from unittest.mock import Mock

import jira_client
import ollama_client


def test_ollama_client_rejects_invalid_report(monkeypatch):
    response = Mock()
    response.json.return_value = {"response": '{"title":"only title"}'}
    response.raise_for_status.return_value = None
    monkeypatch.setattr(ollama_client.requests, "post", lambda *args, **kwargs: response)

    try:
        ollama_client.analyze_screenshot(b"\x89PNG\r\n\x1a\n", "image/png", "", "http://ollama", "gemma3", 1)
    except ollama_client.OllamaError as error:
        assert "invalid bug report" in str(error)
    else:
        raise AssertionError("Expected invalid report to be rejected")


def test_jira_issue_payload(monkeypatch):
    response = Mock()
    response.json.return_value = {"key": "QA-42"}
    response.raise_for_status.return_value = None
    monkeypatch.setattr(jira_client.requests, "post", lambda *args, **kwargs: response)
    report = {"title": "Broken save", "summary": "Save fails", "steps_to_reproduce": ["Click save"], "expected_result": "Saved", "actual_result": "Error", "environment": "Chrome", "severity": "major", "priority": "high", "labels": ["ui"], "confidence": 0.9, "assumptions": []}

    issue = jira_client.create_issue(report, "https://jira.example", "QA", "Bug", "qa@example.com", "token")
    assert issue == {"key": "QA-42", "url": "https://jira.example/browse/QA-42"}
