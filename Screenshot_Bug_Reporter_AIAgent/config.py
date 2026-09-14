import os
from dataclasses import dataclass

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass


@dataclass(frozen=True)
class Settings:
    ollama_base_url: str
    ollama_vision_model: str
    ollama_timeout_seconds: int
    jira_base_url: str
    jira_project_key: str
    jira_issue_type: str
    jira_email: str
    jira_api_token: str
    max_upload_bytes: int

    @classmethod
    def from_env(cls) -> "Settings":
        return cls(
            ollama_base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434").rstrip("/"),
            ollama_vision_model=os.getenv("OLLAMA_VISION_MODEL", "gemma3"),
            ollama_timeout_seconds=int(os.getenv("OLLAMA_TIMEOUT_SECONDS", "120")),
            jira_base_url=os.getenv("JIRA_BASE_URL", "").rstrip("/"),
            jira_project_key=os.getenv("JIRA_PROJECT_KEY", ""),
            jira_issue_type=os.getenv("JIRA_ISSUE_TYPE", "Bug"),
            jira_email=os.getenv("JIRA_EMAIL", ""),
            jira_api_token=os.getenv("JIRA_API_TOKEN", ""),
            max_upload_bytes=int(os.getenv("MAX_UPLOAD_BYTES", "10485760")),
        )

    def validate_jira(self) -> None:
        missing = [
            name for name, value in {
                "JIRA_BASE_URL": self.jira_base_url,
                "JIRA_PROJECT_KEY": self.jira_project_key,
                "JIRA_EMAIL": self.jira_email,
                "JIRA_API_TOKEN": self.jira_api_token,
            }.items() if not value
        ]
        if missing:
            raise ValueError(f"Missing Jira configuration: {', '.join(missing)}")
