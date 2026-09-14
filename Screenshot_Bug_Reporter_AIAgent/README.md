# Screenshot Bug Reporter AI Agent

A local screenshot-to-Jira workflow using a free, local Ollama vision model and n8n orchestration.

## Flow

```text
Browser upload or n8n webhook
        -> image validation
        -> Ollama vision model (structured JSON)
        -> bug-report validation
        -> Jira issue creation
        -> original screenshot attachment
```

The local Flask UI is useful for development and manual testing. The exported n8n workflow is the intended automation path.

## Setup

1. Install Ollama and pull a vision-capable model. The default is configurable; `gemma3` is the recommended starting point.

```powershell
ollama pull gemma3
```

2. Create a virtual environment and install dependencies.

```powershell
py -m venv .venv
.venv\Scripts\activate
py -m pip install -r requirements.txt
```

3. Copy `.env.example` to `.env` and set the Jira values. Never commit `.env` or tokens.

4. Start the local UI:

```powershell
py app.py
```

Open `http://127.0.0.1:5000`.

## n8n setup

1. Run local n8n and import `n8n/screenshot-bug-reporter.workflow.json`.
2. Open both **Create Jira Issue** and **Attach Screenshot**, select the same Jira Software Cloud credential, and save the workflow. The credential is intentionally not embedded in the JSON export.
3. Set n8n environment variables: `OLLAMA_BASE_URL`, `OLLAMA_VISION_MODEL`, `JIRA_BASE_URL`, `JIRA_PROJECT_KEY`, and optionally `JIRA_ISSUE_TYPE`.
4. Confirm the imported connections are linear: `Screenshot Upload` -> `Validate Screenshot` -> `Analyze with Ollama` -> `Validate Bug Report` -> `Create Jira Issue` -> `Prepare Jira Attachment` -> `Attach Screenshot` -> `Return Success`.
5. Activate the workflow and POST a multipart request with the binary field named `screenshot` and an optional text field named `context`.

Example request:

```powershell
curl.exe -X POST http://localhost:5678/webhook/screenshot-bug-reporter -F "screenshot=@.\sample.png" -F "context=Save button fails after login"
```

Local n8n must be able to reach Ollama. For n8n in Docker, `host.docker.internal` is used by the workflow fallback. n8n Cloud cannot reach a private localhost Ollama endpoint without a secure tunnel or separately reachable service.

## Contract and safety

The report contract is documented in `schemas/bug_report.schema.json` and enforced in the local Python path. Screenshots are held in memory for the request and are not archived locally. The `Prepare Jira Attachment` node intentionally restores the original binary after Jira issue creation, because the Jira create response does not carry input binary data forward. Jira receives the original upload as an attachment. The first version intentionally does not perform duplicate detection.

Do not reuse credentials found in other workspace `.env` or settings files. Rotate any credentials that may already have been exposed before testing.

## Tests

After installing dependencies:

```powershell
py -m pytest tests -q
```

The tests are offline and cover image signatures and report-contract validation. Real Ollama/Jira testing requires running services and valid credentials; use a non-production Jira project.
