# SOP: Test Plan Generation

## Goal
Turn a feature requirement (Jira ticket, user story, or freeform text) into a structured, QA-ready test plan.

## Inputs
- `feature_name`: string
- `requirement_text`: string (the source-of-truth requirement)
- `source`: jira | story | manual_requirement
- `acceptance_criteria`: array of strings (optional)
- `constraints`: array of strings (optional)
- `env`: local | staging | prod

## Tool logic
1. Validate the requirement: non-empty, minimum length, and not placeholder text.
2. If invalid, return validation errors and do not generate a plan.
3. If valid, map the requirement into the output schema defined in `gemini.md`.
4. Derive test cases from the requirement and acceptance criteria:
   - Positive tests for each stated behavior
   - Negative tests for missing/invalid input
   - Boundary tests when numeric ranges are stated
5. Mark anything not stated in the requirement as an **assumption** or **risk**, never as fact.
6. Write the generated plan as markdown to `.tmp/`.

## Edge cases
- Empty or whitespace-only requirement -> validation error.
- Requirement shorter than 10 characters -> validation error.
- Placeholder text ("asdf", "todo", "test") -> validation error.
- Missing acceptance criteria -> generate from stated behaviors; note the gap as a risk.

## Golden rule
If the plan-generation logic changes, update this SOP **before** changing the code in `tools/`.
