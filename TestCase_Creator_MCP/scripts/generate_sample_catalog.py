from __future__ import annotations

import argparse
import csv
from pathlib import Path


FEATURES_BY_MODULE = {
    "Dashboard": ["Workspace Overview", "Recent Activity", "Workspace Health"],
    "Campaigns": [
        "Campaign List",
        "Create Campaign",
        "Edit Campaign",
        "Clone Campaign",
        "Archive Campaign",
    ],
    "A/B Testing": [
        "Experiment Setup",
        "Variation Configuration",
        "Visual Editor Launch",
        "Code Editor Launch",
        "Traffic Split",
        "Audience Allocation",
        "Experiment Launch",
    ],
    "Multivariate Testing": [
        "MVT Setup",
        "Factor Configuration",
        "Combination Preview",
        "MVT Launch",
    ],
    "Split URL Testing": [
        "URL Rule Setup",
        "URL Matching",
        "Redirect Validation",
        "Split URL Launch",
    ],
    "Personalization": [
        "Personalization Campaign Setup",
        "Audience Personalization",
        "Content Personalization",
        "Personalization Launch",
    ],
    "Visual Editor": [
        "Page Selection",
        "Element Selection",
        "Visual Change",
        "Editor Save",
    ],
    "Code Editor": [
        "Custom CSS",
        "Custom JavaScript",
        "Code Validation",
        "Code Save",
    ],
    "Audience Targeting": [
        "Audience Builder",
        "URL Targeting",
        "Geo Targeting",
        "Device Targeting",
    ],
    "Goals and Metrics": [
        "Goal Configuration",
        "Conversion Goal",
        "Revenue Goal",
        "Metric Validation",
    ],
    "Traffic Allocation": [
        "Traffic Allocation Setup",
        "Traffic Distribution",
        "Allocation Update",
    ],
    "Variations": [
        "Variation List",
        "Variation Preview",
        "Variation Save",
        "Variation Restore",
    ],
    "Reports": [
        "Report Summary",
        "Experiment Results",
        "Goal Results",
        "Report Export",
    ],
    "Integrations": [
        "Analytics Integration",
        "Tag Manager Integration",
        "Data Export",
        "Webhook Configuration",
    ],
    "Accounts and Users": [
        "User Invitation",
        "Role Assignment",
        "Account Settings",
        "Project Permissions",
        "Access Revocation",
    ],
    "SDK and Settings": [
        "SDK Installation",
        "SDK Initialization",
        "Feature Flag Configuration",
        "API Key Management",
        "Environment Configuration",
    ],
    "Data and Analytics": [
        "Event Tracking",
        "Data Validation",
        "Results Processing",
        "Analytics Attribution",
    ],
}

OPERATIONS = [
    "create",
    "edit",
    "clone",
    "publish",
    "pause",
    "resume",
    "archive",
    "delete",
    "configure",
    "preview",
]

CONDITIONS = [
    "with valid settings",
    "when a required field is missing",
    "when a value has an invalid format",
    "with insufficient permissions",
    "during a network timeout",
    "while another user updates the same item",
    "when the request is submitted twice",
]

EXPECTED_RESULTS = {
    "with valid settings": "The change succeeds and the saved state matches the submitted settings.",
    "when a required field is missing": "The request is blocked, the missing field is identified, and no partial change is saved.",
    "when a value has an invalid format": "A field-level validation message is shown and invalid data is not saved.",
    "with insufficient permissions": "Access is denied and the item remains unchanged.",
    "during a network timeout": "The timeout is reported, no partial change is committed, and retry behavior is safe.",
    "while another user updates the same item": "The concurrent update is handled without silently overwriting the other user's changes.",
    "when the request is submitted twice": "The repeated request does not create duplicate or inconsistent state.",
}

TEST_TYPES = {
    "with valid settings": "Functional",
    "when a required field is missing": "Validation",
    "when a value has an invalid format": "Validation",
    "with insufficient permissions": "Access Control",
    "during a network timeout": "Resilience",
    "while another user updates the same item": "Concurrency",
    "when the request is submitted twice": "Idempotency",
}

FIELDS = [
    "test_case_id",
    "module",
    "feature",
    "scenario",
    "priority",
    "test_type",
    "browser",
    "device",
    "status",
    "preconditions",
    "steps",
    "expected_result",
    "tags",
    "source",
]


def build_rows(count: int) -> list[dict[str, str]]:
    features = [
        (module, feature)
        for module, module_features in FEATURES_BY_MODULE.items()
        for feature in module_features
    ]
    scenario_variants = [
        (operation, condition)
        for operation in OPERATIONS
        for condition in CONDITIONS
    ]
    if count > len(features) * len(scenario_variants):
        raise ValueError(
            f"count cannot exceed {len(features) * len(scenario_variants)} unique scenarios"
        )

    priorities = ["P1", "P2", "P3", "P4"]
    browsers = ["Chrome", "Firefox", "Edge", "Safari"]
    devices = ["Desktop", "Mobile", "Tablet", "Mobile Web"]
    roles = ["administrator", "editor", "viewer"]
    rows = []

    for index in range(count):
        feature_index, variant_index = divmod(index, len(scenario_variants))
        module, feature = features[feature_index]
        operation, condition = scenario_variants[variant_index]
        role = roles[(feature_index + variant_index) % len(roles)]
        scenario = f"Verify {operation} for {feature} {condition}"
        rows.append(
            {
                "test_case_id": f"TC-{index + 1:05d}",
                "module": module,
                "feature": feature,
                "scenario": scenario,
                "priority": priorities[(feature_index + variant_index) % len(priorities)],
                "test_type": TEST_TYPES[condition],
                "browser": browsers[(feature_index + variant_index) % len(browsers)],
                "device": devices[(feature_index + variant_index) % len(devices)],
                "status": "Active",
                "preconditions": (
                    f"User is signed in with {role} access; a test workspace is available."
                ),
                "steps": (
                    f"1. Open {module}. 2. Select {feature}. "
                    f"3. Attempt to {operation} the item. 4. Apply this condition: {condition}. "
                    "5. Review the resulting state and any feedback."
                ),
                "expected_result": EXPECTED_RESULTS[condition],
                "tags": f"{module};{feature};{TEST_TYPES[condition]}",
                "source": "Synthetic sample for MCP development",
            }
        )
    return rows


def main() -> None:
    project_root = Path(__file__).resolve().parents[1]
    default_output = project_root / "data" / "vwo_5000_test_cases.csv"
    parser = argparse.ArgumentParser(
        description="Generate a synthetic test-case catalog for local MCP development."
    )
    parser.add_argument("--count", type=int, default=5000)
    parser.add_argument("--output", type=Path, default=default_output)
    arguments = parser.parse_args()

    if arguments.count < 1:
        parser.error("--count must be at least 1")

    output_path = arguments.output.expanduser().resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    rows = build_rows(arguments.count)

    with output_path.open("w", encoding="utf-8-sig", newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Wrote {len(rows)} synthetic test cases to {output_path}")


if __name__ == "__main__":
    main()