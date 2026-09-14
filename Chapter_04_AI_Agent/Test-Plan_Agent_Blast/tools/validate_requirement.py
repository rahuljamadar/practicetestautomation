"""Validate a requirement payload before test plan generation.

BLAST Layer 3 (Tools): deterministic and atomic.
Input : a JSON payload matching the input schema in gemini.md
Output: JSON with `valid: bool` and `errors: list[str]`
"""

import json
import re
import sys

PLACEHOLDERS = {
    "asdf", "asdfasdf", "test", "todo", "testing",
    "none", "n/a", "na", "placeholder", "fixme", "lorem ipsum",
    "to be determined", "tbd",
}

MIN_LENGTH = 10


def validate_payload(payload):
    """Return (valid, errors). Never guesses business logic."""
    errors = []

    if not isinstance(payload, dict):
        return False, ["Payload must be a JSON object."]

    feature_name = payload.get("feature_name", "").strip()
    requirement_text = payload.get("requirement_text", "").strip()
    source = payload.get("source", "").strip()

    if not feature_name:
        errors.append("feature_name is required.")
    if not requirement_text:
        errors.append("requirement_text is required.")
    elif len(requirement_text) < MIN_LENGTH:
        errors.append(
            f"requirement_text must be at least {MIN_LENGTH} characters."
        )
    else:
        lowered = re.sub(r"[^a-z0-9 ]", "", requirement_text.lower()).strip()
        if lowered in PLACEHOLDERS:
            errors.append("requirement_text looks like placeholder text.")

    if source and source not in ("jira", "story", "manual_requirement"):
        errors.append("source must be one of: jira, story, manual_requirement.")

    if payload.get("env") and payload.get("env") not in (
        "local", "staging", "prod"
    ):
        errors.append("env must be one of: local, staging, prod.")

    return (len(errors) == 0), errors


def main():
    try:
        payload = json.loads(sys.stdin.read())
    except json.JSONDecodeError as exc:
        print(json.dumps({"valid": False, "errors": [f"Invalid JSON: {exc}"]}))
        return 1

    valid, errors = validate_payload(payload)
    print(json.dumps({"valid": valid, "errors": errors}, indent=2))
    return 0 if valid else 1


if __name__ == "__main__":
    sys.exit(main())
