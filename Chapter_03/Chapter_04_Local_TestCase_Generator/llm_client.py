import requests


def _build_test_case_prompt(ticket_details, template_text):
    return f"""You are a senior QA engineer. Use the Jira ticket below and the provided template to generate a clear, actionable test case draft.

Ticket Details:
- Key: {ticket_details.get('key', 'UNKNOWN')}
- Summary: {ticket_details.get('summary', '')}
- Description:
{ticket_details.get('description', '')}
- Acceptance Criteria:
{ticket_details.get('acceptance_criteria', '')}

Template:
{template_text}

Return a polished Markdown test case document. Do not include preamble. Focus on realistic QA scenarios, edge cases, negative checks, and expected outcomes. Keep it concise but complete.
"""


def _build_test_plan_prompt(requirement_text, template_text):
    return f"""You are the Test Plan Agent operating under the BLAST framework:
- B = Blueprint: understand the requirement
- L = Link: use the provided requirement as the source of truth
- A = Architect: organize the plan into test strategy and coverage
- S = Stylize: present the output in a professional QA format
- T = Trigger: return a ready-to-use test plan

Goal: Create a comprehensive test plan based only on the requirement text provided.

Requirement / Feature Details:
{requirement_text}

Template:
{template_text}

Instructions:
- Do not invent business logic.
- Highlight missing or ambiguous requirements as assumptions or risks.
- Include objective, scope, in-scope/out-of-scope, strategy, scenarios, test data, risks, entry criteria, exit criteria, and detailed test cases.
- Use realistic QA wording.
- Return only the final Markdown plan.
"""


def _call_ollama(prompt, ollama_base_url, ollama_model):
    url = f"{ollama_base_url.rstrip('/')}/api/chat"
    payload = {
        "model": ollama_model,
        "messages": [{"role": "user", "content": prompt}],
        "stream": False,
    }
    response = requests.post(url, json=payload, timeout=90)
    response.raise_for_status()
    payload = response.json()
    content = payload.get("message", {}).get("content", "")
    if not content:
        raise ValueError("Ollama returned an empty response.")
    return content.strip()


def _call_groq(prompt, groq_api_key):
    if not groq_api_key:
        raise ValueError("Groq API key is missing. Add one in Settings before using the fallback.")

    url = "https://api.groq.com/openai/v1/chat/completions"
    payload = {
        "model": "llama-3.1-8b-instant",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.2,
        "max_tokens": 2000,
    }
    headers = {
        "Authorization": f"Bearer {groq_api_key}",
        "Content-Type": "application/json",
    }
    response = requests.post(url, json=payload, headers=headers, timeout=90)
    response.raise_for_status()
    data = response.json()
    content = data["choices"][0]["message"]["content"]
    if not content:
        raise ValueError("Groq returned an empty response.")
    return content.strip()


def generate_test_cases(ticket_details, template_text, settings):
    prompt = _build_test_case_prompt(ticket_details, template_text)
    provider = (settings.get("provider") or "ollama").lower()
    groq_api_key = (settings.get("groq_api_key") or "").strip()
    ollama_base_url = settings.get("ollama_base_url", "http://localhost:11434")
    ollama_model = settings.get("ollama_model", "gemma3:1b")

    if provider == "groq":
        return _call_groq(prompt, groq_api_key)

    try:
        return _call_ollama(prompt, ollama_base_url, ollama_model)
    except Exception as ollama_error:
        if not groq_api_key:
            raise RuntimeError(
                "Ollama is unavailable and no Groq API key is configured. Please update Settings."
            ) from ollama_error
        return _call_groq(prompt, groq_api_key)


def generate_test_plan(requirement_text, template_text, settings):
    prompt = _build_test_plan_prompt(requirement_text, template_text)
    provider = (settings.get("provider") or "ollama").lower()
    groq_api_key = (settings.get("groq_api_key") or "").strip()
    ollama_base_url = settings.get("ollama_base_url", "http://localhost:11434")
    ollama_model = settings.get("ollama_model", "gemma3:1b")

    if provider == "groq":
        return _call_groq(prompt, groq_api_key)

    try:
        return _call_ollama(prompt, ollama_base_url, ollama_model)
    except Exception as ollama_error:
        if not groq_api_key:
            raise RuntimeError(
                "Ollama is unavailable and no Groq API key is configured. Please update Settings."
            ) from ollama_error
        return _call_groq(prompt, groq_api_key)
