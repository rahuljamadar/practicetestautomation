from image_validation import validate_image
from models import validate_bug_report


def test_accepts_png_signature():
    result = validate_image("image/png", b"\x89PNG\r\n\x1a\nrest", 100)
    assert result.valid


def test_rejects_mismatched_content_type():
    result = validate_image("image/png", b"not-an-image", 100)
    assert not result.valid


def test_rejects_oversized_image():
    result = validate_image("image/png", b"\x89PNG\r\n\x1a\n123", 8)
    assert not result.valid


def test_validates_bug_report_contract():
    report = {
        "title": "Save action fails",
        "summary": "The save action does not complete.",
        "steps_to_reproduce": ["Open page", "Click Save"],
        "expected_result": "The record is saved.",
        "actual_result": "An error is shown.",
        "environment": "Chrome on Windows",
        "severity": "major",
        "priority": "high",
        "labels": ["ui"],
        "confidence": 0.9,
        "assumptions": [],
    }
    assert validate_bug_report(report).valid


def test_reports_missing_bug_fields():
    result = validate_bug_report({"title": "Incomplete"})
    assert not result.valid
    assert "Missing required field: summary" in result.errors
