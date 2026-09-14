# Architecture: Test Plan Agent

## What we are doing
We are building a local Test Plan Agent that turns a feature requirement into a structured QA test plan.

The system follows the BLAST framework:
- Blueprint: define the goal, data contract, and rules
- Link: connect to the requirement source and validate environment readiness
- Architect: separate concerns into clear layers
- Stylize: format the final output for human review
- Trigger: run and validate the app in the browser

## Goal
Create a deterministic, review-friendly workflow that generates:
- objective
- scope
- assumptions
- risks
- test strategy
- detailed test cases

## System architecture

### Layer 1: Architecture
This project stores system rules, data contracts, and SOPs in Markdown files such as:
- `gemini.md`
- `task_plan.md`
- `findings.md`
- `progress.md`
- `llm.md`
- `architecture.md`

### Layer 2: Navigation / Decision Layer
This is the reasoning layer that decides:
- whether input is a feature requirement, Jira ticket, or freeform prompt
- whether to generate a full plan or a smaller summary
- how to structure the final answer for QA readability

### Layer 3: Tooling / Execution Layer
This layer is responsible for:
- collecting requirement text
- validating content
- formatting markdown output
- optionally integrating with Ollama or another LLM backend

## Recommended runtime flow
1. User enters a feature description.
2. The app checks whether input is missing, unclear, or incomplete.
3. The app converts the input into a structured test plan.
4. The output is displayed as markdown in the browser.
5. The user reviews the generated content and can refine requirements if needed.

## Non-goals
- We are not creating a production-grade external integration yet.
- We are not making assumptions about business logic without a source requirement.
- We are not skipping the review stage before launch.

## Current implementation status
This project is currently in the planning + initialization stage, with the architecture and operational memory files in place. The next step is a browser-ready local app that can generate the test plan from user input.
