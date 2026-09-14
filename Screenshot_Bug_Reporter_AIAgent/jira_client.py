import json
from typing import Any

import requests
from requests.auth import HTTPBasicAuth


class JiraError(RuntimeError):
    pass


def _auth(email: str, api_token: str) -> HTTPBasicAuth:
    return HTTPBasicAuth(email, api_token)


def create_issue(report: dict[str, Any], base_url: str, project_key: str, issue_type: str, email: str, api_token: str) -> dict[str, Any]:
    description = "\n".join([
        report["summary"],
        "",
        "Steps to reproduce:",
        *[f"{index}. {step}" for index, step in enumerate(report["steps_to_reproduce"], 1)],
        "",
        f"Expected result: {report['expected_result']}",
        f"Actual result: {report['actual_result']}",
        f"Environment: {report['environment']}",
        f"Severity: {report['severity']}",
        f"Confidence: {report['confidence']}",
        f"Assumptions: {', '.join(report['assumptions']) or 'None'}",
    ])
    payload = {"fields": {
        "project": {"key": project_key},
        "summary": report["title"],
        "description": description,
        "issuetype": {"name": issue_type},
        "priority": {"name": report["priority"].capitalize()},
        "labels": report["labels"],
    }}
    try:
        response = requests.post(
            f"{base_url}/rest/api/3/issue",
            auth=_auth(email, api_token),
            headers={"Accept": "application/json", "Content-Type": "application/json"},
            data=json.dumps(payload),
            timeout=30,
        )
        response.raise_for_status()
        result = response.json()
    except (requests.RequestException, ValueError) as exc:
        raise JiraError(f"Jira issue creation failed: {exc}") from exc
    return {"key": result["key"], "url": f"{base_url}/browse/{result['key']}"}


def attach_screenshot(issue_key: str, content: bytes, filename: str, mime_type: str, base_url: str, email: str, api_token: str) -> dict[str, Any]:
    try:
        response = requests.post(
            f"{base_url}/rest/api/3/issue/{issue_key}/attachments",
            auth=_auth(email, api_token),
            headers={"X-Atlassian-Token": "no-check", "Accept": "application/json"},
            files={"file": (filename, content, mime_type)},
            timeout=30,
        )
        response.raise_for_status()
        return {"attached": True, "details": response.json()}
    except (requests.RequestException, ValueError) as exc:
        raise JiraError(f"Jira attachment failed: {exc}") from exc
