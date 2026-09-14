from pathlib import Path

import streamlit as st

from config_store import load_settings
from jira_client import get_issue_details
from llm_client import generate_test_cases, generate_test_plan


st.set_page_config(page_title="Jira Test Case Generator", page_icon="🧪", layout="wide")


def load_template(template_name="test_case_template.md"):
    template_path = Path(__file__).resolve().parent / "templates" / template_name
    if not template_path.exists():
        fallback = {
            "test_case_template.md": "# Test Cases\n\n- Test ID:\n- Title:\n- Scenario:\n- Steps:\n- Expected Result:\n",
            "test_plan_template.md": "# Test Plan\n\n## Objective\n<goal>\n\n## Scope\n<scope>\n\n## Test Cases\n- TC-01: <title>\n",
        }
        return fallback.get(template_name, fallback["test_case_template.md"])
    return template_path.read_text(encoding="utf-8")


def extract_issue_key(message):
    import re

    match = re.search(r"\b[A-Z][A-Z0-9]+-\d+\b", message or "")
    return match.group(0) if match else None


if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("Jira Test Case Generator")

with st.sidebar:
    st.caption("Default backend: Ollama on localhost")
    settings = load_settings()
    provider = settings.get("provider", "ollama").capitalize()
    st.write(f"Provider: {provider}")
    st.write(f"Model: {settings.get('ollama_model', 'gemma3:1b')}")
    st.write("Settings are stored locally in settings.json")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

user_prompt = st.chat_input("Type a request such as 'create test plan for login flow' or 'create test cases for QA-102'")

if user_prompt:
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    with st.chat_message("user"):
        st.markdown(user_prompt)

    prompt_lower = user_prompt.lower()
    wants_test_plan = "test plan" in prompt_lower or "testplan" in prompt_lower

    if wants_test_plan:
        settings = load_settings()
        try:
            template_text = load_template("test_plan_template.md")
            generated_plan = generate_test_plan(user_prompt, template_text, settings)
            response = f"## Test Plan\n\n{generated_plan}"
        except Exception as exc:
            response = f"I hit an issue while generating the test plan: {exc}"

        st.session_state.messages.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.markdown(response)
    else:
        issue_key = extract_issue_key(user_prompt)
        if not issue_key:
            response = "I could not detect a Jira issue key. Please include a valid ticket ID such as QA-102 or ask for a test plan."
            st.session_state.messages.append({"role": "assistant", "content": response})
            with st.chat_message("assistant"):
                st.markdown(response)
        else:
            settings = load_settings()
            if not settings.get("jira_url") or not settings.get("jira_email") or not settings.get("jira_api_token"):
                response = "Jira settings are incomplete. Please save the Jira URL, email, and API token in the Settings page."
                st.session_state.messages.append({"role": "assistant", "content": response})
                with st.chat_message("assistant"):
                    st.markdown(response)
            else:
                try:
                    ticket_details = get_issue_details(
                        settings["jira_url"],
                        settings["jira_email"],
                        settings["jira_api_token"],
                        issue_key,
                    )
                    template_text = load_template()
                    generated_cases = generate_test_cases(ticket_details, template_text, settings)
                    response = f"## Test Cases for {ticket_details['key']}\n\n{generated_cases}"
                except Exception as exc:
                    response = f"I hit an issue while generating the test cases: {exc}"

                st.session_state.messages.append({"role": "assistant", "content": response})
                with st.chat_message("assistant"):
                    st.markdown(response)
