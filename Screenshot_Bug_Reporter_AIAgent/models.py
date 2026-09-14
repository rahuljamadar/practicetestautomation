from dataclasses import dataclass
from typing import Any


REQUIRED_REPORT_FIELDS = (
    "title",
    "summary",
    "steps_to_reproduce",
    "expected_result",
    "actual_result",
    "environment",
    "severity",
    "priority",
    "labels",
    "confidence",
    "assumptions",
)
ALLOWED_SEVERITIES = {"blocker", "critical", "major", "minor", "trivial"}
ALLOWED_PRIORITIES = {"highest", "high", "medium", "low", "lowest"}


@dataclass(frozen=True)
class ValidationResult:
    valid: bool
    errors: list[str]


def validate_bug_report(report: Any) -> ValidationResult:
    errors: list[str] = []
    if not isinstance(report, dict):
        return ValidationResult(False, ["Bug report must be a JSON object."])

    for field in REQUIRED_REPORT_FIELDS:
        if field not in report:
            errors.append(f"Missing required field: {field}")

    for field in ("title", "summary", "expected_result", "actual_result", "environment"):
        if field in report and (not isinstance(report[field], str) or not report[field].strip()):
            errors.append(f"{field} must be a non-empty string.")

    for field in ("steps_to_reproduce", "labels", "assumptions"):
        if field in report and not isinstance(report[field], list):
            errors.append(f"{field} must be an array.")

    if isinstance(report.get("severity"), str) and report["severity"].lower() not in ALLOWED_SEVERITIES:
        errors.append("severity must be blocker, critical, major, minor, or trivial.")
    if isinstance(report.get("priority"), str) and report["priority"].lower() not in ALLOWED_PRIORITIES:
        errors.append("priority must be highest, high, medium, low, or lowest.")
    if "confidence" in report and (not isinstance(report["confidence"], (int, float)) or not 0 <= report["confidence"] <= 1):
        errors.append("confidence must be a number between 0 and 1.")

    return ValidationResult(not errors, errors)
