# Gemini Project Constitution

## Project name
Test Plan Agent - BLAST

## Purpose
Generate structured, QA-ready test plans from requirement text and supporting project context.

## Input schema
```json
{
  "feature_name": "string",
  "requirement_text": "string",
  "source": "jira|story|manual_requirement",
  "acceptance_criteria": ["string"],
  "constraints": ["string"],
  "env": "local|staging|prod"
}
```

## Output schema
```json
{
  "test_plan_name": "string",
  "objective": "string",
  "scope": {
    "in_scope": ["string"],
    "out_of_scope": ["string"]
  },
  "assumptions": ["string"],
  "risks": ["string"],
  "test_strategy": "string",
  "test_data": ["string"],
  "entry_criteria": ["string"],
  "exit_criteria": ["string"],
  "test_cases": [
    {
      "test_id": "string",
      "title": "string",
      "scenario": "string",
      "steps": ["string"],
      "expected_result": "string",
      "priority": "High|Medium|Low",
      "type": "Positive|Negative|Boundary|API|UI"
    }
  ]
}
```

## Behavioral invariants
- Never assume business rules that are not stated.
- Keep outputs deterministic and consistent.
- Mark missing details as assumptions or risks.
- Output must be reviewable by humans before execution.
- Follow BLAST phases: Blueprint, Link, Architect, Stylize, Trigger.

## Architecture invariants
- Layer 1: Architecture docs and SOPs.
- Layer 2: Navigation and decision-making logic.
- Layer 3: Deterministic tool scripts.

## Maintenance rule
Update this file whenever the input/output contract or the system behavior changes.
