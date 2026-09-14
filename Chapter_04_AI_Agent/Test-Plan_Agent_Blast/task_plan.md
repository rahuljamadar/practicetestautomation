# Test Plan Agent - BLAST Task Plan

## Objective
Design and initialize a Test Plan Agent that follows the BLAST framework and produces a structured, deterministic QA test plan from feature requirements or Jira context.

## Phase 0: Initialization
- Create project memory files:
  - `task_plan.md`
  - `findings.md`
  - `progress.md`
  - `llm.md`
  - `gemini.md`
- Establish the project constitution and constraints.
- Confirm no implementation is started before the problem, payload, and rules are defined.

## Phase 1: Blueprint
- Define the singular desired outcome: generate robust, QA-ready test plans.
- Identify likely input sources:
  - Jira tickets
  - feature requirements
  - acceptance criteria
  - user stories
- Document behavioral rules:
  - do not invent business logic
  - separate assumptions and risks
  - prioritize test quality over verbosity
  - return execution-ready markdown output
- Define data schema for the input payload and expected output plan.

## Phase 2: Link
- Verify local environment readiness.
- Confirm whether external services or API access will be used.
- Validate model or execution backend availability.
- Confirm requirement source is reliable before generating the plan.
- Result: no external APIs needed; fully local deterministic pipeline.

## Phase 3: Architect
- Create the three-layer architecture:
  - `architecture/SOP_test_plan_generation.md` for SOPs and rules
  - navigation/decision layer for flow logic
  - `tools/` for deterministic execution scripts
- Ensure the plan generator has a clean separation between:
  - input collection (index.html + server.py)
  - test plan generation (tools/test_plan_generator.py)
  - output formatting (markdown renderer in index.html)
- Result: implemented.

## Phase 4: Stylize
- Format the final output as clean markdown.
- Include section headings, tables where useful, and execution-friendly details.
- Ensure readability for QA engineers, stakeholders, and leads.
- Result: implemented (sectioned markdown with test case table and detail blocks).

## Phase 5: Trigger
- Run the agent in a local environment.
- Validate output quality against a sample requirement.
- Adjust prompt or structure if the generated plan is vague or inconsistent.
- Result: verified on 127.0.0.1:8000 (GET / -> 200, valid + invalid POST /generate paths tested).

## Acceptance Criteria
- The agent produces a structured test plan from a requirement. (done)
- Output covers objective, scope, assumptions, risks, and test cases. (done)
- The workflow aligns with BLAST principles. (done)
- The project includes memory docs and a valid architecture baseline. (done)

## Checklist
- [x] Define the project goal
- [x] Define data contract in `gemini.md`
- [x] Document findings and project constraints
- [x] Prepare the BLAST-oriented plan structure
- [x] Validate the workflow in a browser or local runtime

## How to run
```
cd Test-Plan_Agent_Blast
py server.py
# open http://127.0.0.1:8000
```
