# QA Orchestrator

This folder contains a QA orchestration agent and n8n workflow for converting business requirements into:

- requirement analysis
- test plan
- manual test cases
- Playwright automation package

## Included Files

- `QA_Orchestrator_Agent.md` — full agent guidance and rules
- `QA_Orchestrator_Prompt.md` — direct prompt for LLM/n8n use
- `n8n_QA_Orchestrator_Workflow.json` — imported workflow definition

## Core Principles

### Anti-Hallucination Rules
- Never invent behavior, APIs, fields, permissions, selectors, or acceptance criteria not supported by the requirement.
- Separate facts, assumptions, and unknowns.
- Mark unknowns as TBD.
- Ask clarifying questions when the requirement is incomplete.
- Keep traceability from requirement to test case to automation.
- Do not claim execution or validation without evidence.

### RICEPOT Method
Use the RICEPOT framework while processing every requirement:
- Role
- Instruction
- Context
- Example
- Parameters
- Output
- Tone

## Expected Flow

1. Requirement input: CRS / BRD / user story / Jira / defect / acceptance criteria
2. Requirement normalization
3. Test plan generation
4. Human review
5. Manual test case generation
6. Human review
7. Playwright automation package generation
8. Human review
9. Final QA package

## Example Requirement Input

"As a user, I want to log in with valid email and password so that I can access my dashboard. Invalid credentials should show an error message."

## Expected Output

- normalized requirement summary
- in-scope/out-of-scope analysis
- test plan with environment and risk coverage
- executable manual test cases
- Playwright JavaScript/POM automation package
- unresolved selectors flagged for human review

## Human Review Requirement

All generated outputs should be reviewed before approval. Any ambiguous selector, missing requirement detail, or unsupported assumption must be marked for follow-up.

## n8n Import Notes

- Import `n8n_QA_Orchestrator_Workflow.json` into n8n.
- Connect the Ollama model nodes to your local Ollama credential.
- Use the default local endpoint such as `http://localhost:11434` or `http://host.docker.internal:11434`.
- Review each agent node and confirm the model is connected.

## Suggested Use

Use this workflow for:
- functional requirement analysis
- QA planning
- manual testing readiness
- automation scaffold generation
- traceability-driven QA review

---

This agent is built to be conservative, review-friendly, and evidence-based rather than guessing or inventing missing product behavior.
