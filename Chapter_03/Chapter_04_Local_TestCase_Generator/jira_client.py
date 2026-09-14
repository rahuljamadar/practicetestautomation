import re
from typing import Dict, Any

import requests


def _clean_jira_value(value):
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    if isinstance(value, list):
        return "\n".join(part for part in (_clean_jira_value(item) for item in value) if part)
    if isinstance(value, dict):
        if "text" in value and isinstance(value["text"], str):
            return value["text"].strip()
        if "content" in value:
            content = []
            for item in value["content"]:
                text = _clean_jira_value(item)
                if text:
                    content.append(text)
            return "\n".join(content)
    return str(value).strip()


def _extract_description(description):
    if description is None:
        return "No description provided."

    if isinstance(description, str):
        return description.strip() or "No description provided."

    return _clean_jira_value(description) or "No description provided."


def _extract_acceptance_criteria(description_text):
    match = re.search(r"Acceptance Criteria\s*[:\-]?\s*(.*)", description_text, flags=re.IGNORECASE | re.DOTALL)
    if match:
        return match.group(1).strip()
    return "No explicit acceptance criteria were found in the ticket description."


def get_issue_details(jira_url: str, jira_email: str, jira_api_token: str, issue_key: str) -> Dict[str, Any]:
    if not jira_url or not jira_email or not jira_api_token:
        raise ValueError("Jira URL, email, and API token are required in Settings.")

    issue_key = issue_key.strip()
    if not issue_key:
        raise ValueError("A Jira issue key was not provided.")

    url = f"{jira_url.rstrip('/')}/rest/api/2/issue/{issue_key}?fields=summary,description"

    response = requests.get(
        url,
        auth=(jira_email, jira_api_token),
        timeout=30,
        headers={"Accept": "application/json"},
    )

    if response.status_code == 401:
        raise PermissionError("Jira authentication failed. Please verify the API token and email.")
    if response.status_code == 404:
        raise ValueError(f"Jira ticket {issue_key} was not found.")
    response.raise_for_status()

    payload = response.json()
    fields = payload.get("fields", {})
    summary = fields.get("summary", "Unknown summary")
    description = _extract_description(fields.get("description"))
    acceptance_criteria = _extract_acceptance_criteria(description)

    return {
        "key": payload.get("key", issue_key),
        "summary": summary,
        "description": description,
        "acceptance_criteria": acceptance_criteria,
    }
