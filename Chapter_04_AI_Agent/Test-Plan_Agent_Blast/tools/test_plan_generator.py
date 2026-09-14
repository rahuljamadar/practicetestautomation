"""Generate a deterministic QA test plan from a validated requirement payload.

BLAST Layer 3 (Tools): deterministic and atomic.
Input : a JSON payload matching the input schema in gemini.md
Output: markdown test plan written to .tmp/, JSON payload echoed to stdout
"""

import json
import os
import re
import sys

from validate_requirement import validate_payload

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TMP_DIR = os.path.join(ROOT, ".tmp")
OUTPUT_FILE = os.path.join(TMP_DIR, "test_plan_output.md")


def _split_sentences(text):
    """Split on sentence boundaries, dropping empties."""
    parts = re.split(r"(?<=[.!?])\s+", text.strip())
    return [p.strip() for p in parts if p.strip()]


def build_test_cases(payload):
    """Derive test cases strictly from stated requirement content."""
    requirement_text = payload.get("requirement_text", "")
    acceptance_criteria = payload.get("acceptance_criteria") or []
    cases = []
    counter = 1

    # One positive case per stated sentence (stated behavior).
    for sentence in _split_sentences(requirement_text):
        if len(sentence) < 4:
            continue
        cases.append({
            "test_id": f"TC-{counter:02d}",
            "title": f"Verify: {sentence[:60]}",
            "scenario": "Positive scenario derived from the stated requirement.",
            "steps": [
                "Open the feature in the target environment.",
                f"Execute the behavior described: {sentence}",
                "Observe the result.",
            ],
            "expected_result": "The system behaves exactly as stated in the requirement.",
            "priority": "High",
            "type": "Positive",
        })
        counter += 1

    # One positive case per acceptance criterion.
    for criterion in acceptance_criteria:
        criterion = criterion.strip()
        if not criterion:
            continue
        cases.append({
            "test_id": f"TC-{counter:02d}",
            "title": f"Acceptance: {criterion[:60]}",
            "scenario": "Acceptance criterion verification.",
            "steps": [
                "Reproduce the acceptance criterion context.",
                f"Check: {criterion}",
                "Record the actual result.",
            ],
            "expected_result": "The acceptance criterion is fully met.",
            "priority": "High",
            "type": "Positive",
        })
        counter += 1

    # A negative case: reject missing or invalid input.
    cases.append({
        "test_id": f"TC-{counter:02d}",
        "title": "Negative: invalid or incomplete input is rejected",
        "scenario": "User provides empty, placeholder, or malformed input.",
        "steps": [
            "Submit an empty requirement.",
            "Submit a placeholder requirement.",
            "Submit a valid requirement.",
        ],
        "expected_result": (
            "Empty and placeholder inputs are rejected with a clear message; "
            "valid input proceeds to plan generation."
        ),
        "priority": "Medium",
        "type": "Negative",
    })
    counter += 1

    # A boundary case whenever the requirement mentions numbers.
    if re.search(r"\d", requirement_text):
        cases.append({
            "test_id": f"TC-{counter:02d}",
            "title": "Boundary: numeric limits stated in the requirement",
            "scenario": "Test values at the stated numeric boundary.",
            "steps": [
                "Identify the numeric limit in the requirement.",
                "Test at the limit, just below it, and just above it.",
            ],
            "expected_result": (
                "Values at and below the limit succeed; values above the limit "
                "are handled gracefully per the stated rule."
            ),
            "priority": "Medium",
            "type": "Boundary",
        })

    return cases


def generate_plan(payload):
    """Build the full test plan dict following the gemini.md output schema."""
    requirement_text = payload.get("requirement_text", "")
    feature_name = payload.get("feature_name", "Untitled Feature")
    env = payload.get("env", "local")
    acceptance_criteria = payload.get("acceptance_criteria") or []
    constraints = payload.get("constraints") or []

    test_cases = build_test_cases(payload)

    plan = {
        "test_plan_name": f"Test Plan - {feature_name}",
        "objective": (
            "Validate that the feature meets the stated requirement "
            "and acceptance criteria in the target environment."
        ),
        "scope": {
            "in_scope": [feature_name],
            "out_of_scope": [
                "Performance and load testing",
                "Security penetration testing",
                "Cross-browser visual regression",
            ],
        },
        "assumptions": [
            "The requirement text is the source of truth.",
            "No business rules are assumed beyond what is stated.",
        ],
        "risks": [
            "Unstated business rules may be missed.",
        ],
        "test_strategy": (
            "Deterministic generation from the stated requirement: positive "
            "cases per stated behavior, negative case for invalid input, and "
            "boundary case when numeric limits are present."
        ),
        "test_data": [],
        "entry_criteria": [
            "Requirement text is validated and non-empty.",
            "Target environment is available.",
        ],
        "exit_criteria": [
            "All test cases are executed and reviewed.",
            "All defects are logged or explicitly accepted as risks.",
        ],
        "test_cases": test_cases,
    }

    if acceptance_criteria:
        plan["assumptions"].append(
            "Acceptance criteria were provided and mapped to test cases."
        )
    else:
        plan["risks"].append(
            "No acceptance criteria were provided; test cases are derived from "
            "requirement text only."
        )

    if constraints:
        plan["assumptions"].append(
            "Stated constraints are respected during execution."
        )

    plan["test_data"].append(
        f"Environment: {env}"
    )

    return plan


def plan_to_markdown(plan):
    """Render the plan as professional markdown (BLAST Phase 4: Stylize)."""
    lines = []
    lines.append(f"# {plan['test_plan_name']}")
    lines.append("")
    lines.append(f"**Environment:** {plan['test_data'][0]}")
    lines.append("")
    lines.append("## 1. Objective")
    lines.append(plan["objective"])
    lines.append("")
    lines.append("## 2. Scope")
    lines.append(f"**In Scope:** {', '.join(plan['scope']['in_scope'])}")
    lines.append(f"**Out of Scope:** {', '.join(plan['scope']['out_of_scope'])}")
    lines.append("")
    lines.append("## 3. Assumptions / Dependencies")
    for item in plan["assumptions"]:
        lines.append(f"- {item}")
    lines.append("")
    lines.append("## 4. Test Strategy")
    lines.append(plan["test_strategy"])
    lines.append("")
    lines.append("## 5. Test Data Requirements")
    for item in plan["test_data"]:
        lines.append(f"- {item}")
    lines.append("")
    lines.append("## 6. Risks / Constraints")
    for item in plan["risks"]:
        lines.append(f"- {item}")
    lines.append("")
    lines.append("## 7. Entry Criteria")
    for item in plan["entry_criteria"]:
        lines.append(f"- {item}")
    lines.append("")
    lines.append("## 8. Exit Criteria")
    for item in plan["exit_criteria"]:
        lines.append(f"- {item}")
    lines.append("")
    lines.append("## 9. Detailed Test Cases")
    lines.append("")
    lines.append("| ID | Title | Priority | Type |")
    lines.append("|----|-------|----------|------|")
    for tc in plan["test_cases"]:
        lines.append(f"| {tc['test_id']} | {tc['title']} | {tc['priority']} | {tc['type']} |")
    lines.append("")
    for tc in plan["test_cases"]:
        lines.append(f"### {tc['test_id']} - {tc['title']}")
        lines.append("")
        lines.append(f"- **Scenario:** {tc['scenario']}")
        lines.append("- **Steps:**")
        for step in tc["steps"]:
            lines.append(f"  1. {step}")
        lines.append(f"- **Expected Result:** {tc['expected_result']}")
        lines.append(f"- **Priority:** {tc['priority']} | **Type:** {tc['type']}")
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def main():
    try:
        payload = json.loads(sys.stdin.read())
    except json.JSONDecodeError as exc:
        print(json.dumps({"ok": False, "error": f"Invalid JSON: {exc}"}))
        return 1

    valid, errors = validate_payload(payload)
    if not valid:
        print(json.dumps({"ok": False, "errors": errors}, indent=2))
        return 1

    plan = generate_plan(payload)
    markdown = plan_to_markdown(plan)

    os.makedirs(TMP_DIR, exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as fh:
        fh.write(markdown)

    print(json.dumps({
        "ok": True,
        "test_plan_name": plan["test_plan_name"],
        "test_case_count": len(plan["test_cases"]),
        "output_file": OUTPUT_FILE,
    }, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
