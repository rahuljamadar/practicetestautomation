# Test Plan Agent - BLAST Framework Plan

## Objective
Build a local Test Plan Agent for the Chapter_04 Local Test Case Generator project using the BLAST framework:
- B = Blueprint
- L = Link
- A = Architect
- S = Stylize
- T = Trigger

The agent should convert project requirements, Jira tickets, or feature briefs into a structured, high-quality test plan and executable test cases.

## Phase 1: Blueprint
- Define the primary outcome: generate actionable test plans and negative/positive test cases from requirements.
- Confirm the input sources:
  - Jira issue summary/description
  - PRD/BRD/SRS text
  - feature requirements pasted manually
- Confirm expected outputs:
  - Test plan overview
  - scope and objectives
  - assumptions and risks
  - test scenarios
  - test steps and expected results
  - test data requirements
- Define the behavioral rules:
  - Do not invent business logic.
  - Base output on provided requirements.
  - Separate positive and negative testing.
  - Highlight missing or ambiguous requirements.

## Phase 2: Link
- Validate environment setup and dependency readiness.
- Confirm local model/backend is accessible.
- Verify Jira access and app configuration if ticket-based generation is used.
- Ensure the app can load requirements and generate output reliably.

## Phase 3: Architect
### Core modules
- `app.py`: UI entry point for user prompts
- `config_store.py`: local settings and configuration handling
- `jira_client.py`: Jira ticket fetch logic
- `llm_client.py`: prompt execution and test generation logic
- `templates/`: reusable output template files

### Expected architecture behavior
- Take input from Jira or user-provided requirements.
- Parse requirement details.
- Generate a structured test plan.
- Return findings in markdown or table format.
- Keep logic deterministic and reviewable.

## Phase 4: Stylize
- Format output in readable markdown.
- Include heading sections, test IDs, priorities, assumptions, and coverage.
- Present results clearly for QA engineers and stakeholders.

## Phase 5: Trigger
- Run the app locally as a Streamlit-based agent.
- Validate output generation with a test input.
- Tune prompts for quality and completeness.
- Keep the project ready for local or future automation extension.

## Deliverables
- `task_plan.md`
- `findings.md`
- `progress.md`
- `llm.md`
- A usable local test plan generation workflow in the existing app

## Success Criteria
- Agent reads requirement input reliably.
- Output includes test objectives, scope, scenarios, steps, and expected results.
- Output is understandable and usable by QA/test teams.
- The flow works locally without external project changes.

## Checklist
- [ ] Confirm input model and requirement source
- [ ] Validate local backend and settings
- [ ] Build BLAST-based logic for test-plan generation
- [ ] Test prompt quality and output consistency
- [ ] Document findings and next improvements
