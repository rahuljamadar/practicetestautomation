import streamlit as st

from config_store import load_settings, save_settings


st.title("Settings")

settings = load_settings()

with st.form("settings_form"):
    jira_url = st.text_input("Jira URL", value=settings.get("jira_url", ""), help="Example: https://company.atlassian.net")
    jira_email = st.text_input("Jira Email", value=settings.get("jira_email", ""))
    jira_api_token = st.text_input("Jira API Token", value=settings.get("jira_api_token", ""), type="password")
    provider = st.selectbox("LLM Provider", ["ollama", "groq"], index=0 if settings.get("provider", "ollama") == "ollama" else 1)
    groq_api_key = st.text_input("Groq API Key", value=settings.get("groq_api_key", ""), type="password")
    ollama_base_url = st.text_input("Ollama Base URL", value=settings.get("ollama_base_url", "http://localhost:11434"))
    ollama_model = st.text_input("Ollama Model", value=settings.get("ollama_model", "gemma3:1b"))

    submitted = st.form_submit_button("Save Settings")
    if submitted:
        save_settings({
            "jira_url": jira_url,
            "jira_email": jira_email,
            "jira_api_token": jira_api_token,
            "provider": provider,
            "groq_api_key": groq_api_key,
            "ollama_base_url": ollama_base_url,
            "ollama_model": ollama_model,
        })
        st.success("Settings saved locally.")

st.caption("The default provider is Ollama. Groq is used only as a fallback when Ollama is unavailable or explicitly selected.")
