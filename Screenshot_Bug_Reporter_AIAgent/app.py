import uuid
from pathlib import Path

from flask import Flask, jsonify, render_template, request

from config import Settings
from image_validation import validate_image
from jira_client import JiraError, attach_screenshot, create_issue
from ollama_client import OllamaError, analyze_screenshot

app = Flask(__name__, template_folder="templates", static_folder="static")


@app.get("/")
def index():
    return render_template("index.html")


@app.post("/api/report")
def report_bug():
    settings = Settings.from_env()
    upload = request.files.get("screenshot")
    if upload is None:
        return jsonify({"error": "A screenshot file is required."}), 400

    content = upload.read()
    validation = validate_image(upload.mimetype, content, settings.max_upload_bytes)
    if not validation.valid:
        return jsonify({"error": validation.error}), 400

    request_id = str(uuid.uuid4())
    context = request.form.get("context", "")
    try:
        report = analyze_screenshot(content, upload.mimetype, context, settings.ollama_base_url, settings.ollama_vision_model, settings.ollama_timeout_seconds)
        settings.validate_jira()
        issue = create_issue(report, settings.jira_base_url, settings.jira_project_key, settings.jira_issue_type, settings.jira_email, settings.jira_api_token)
        attachment = attach_screenshot(issue["key"], content, upload.filename or "screenshot", upload.mimetype, settings.jira_base_url, settings.jira_email, settings.jira_api_token)
    except (OllamaError, JiraError, ValueError) as exc:
        return jsonify({"request_id": request_id, "error": str(exc)}), 502

    return jsonify({"request_id": request_id, "report": report, "jira": issue, "attachment": attachment})


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
