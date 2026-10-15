"""Central configuration loaded from the workspace .env file."""
import os
from pathlib import Path

from dotenv import load_dotenv

# Workspace root is the QABuddy.ai folder (config.py -> core/ -> backend/ -> root).
WORKSPACE_DIR = Path(__file__).resolve().parents[2]
ENV_FILE = WORKSPACE_DIR / ".env"
load_dotenv(ENV_FILE, override=True)

# True when running as a Vercel Function (read-only FS except /tmp)
IS_VERCEL = bool(os.environ.get("VERCEL"))


# Canonical doc types. Legacy `playwright_*` values (indexed before the
# Automation-Specs rename) keep matching through DOC_TYPE_ALIASES until
# the next Full Reindex rewrites Qdrant cleanly.
DOC_TYPES = ("jira_defect", "test_case", "automation_spec", "automation_page", "automation_module")
DOC_TYPE_ALIASES = {
    "playwright_spec": "automation_spec",
    "playwright_page": "automation_page",
    "playwright_module": "automation_module",
}
LEGACY_DOC_TYPES = tuple(DOC_TYPE_ALIASES)


def canonical_doc_type(doc_type: str | None) -> str | None:
    """Map a legacy doc_type to its canonical Automation name (None-safe)."""
    if not doc_type or doc_type == "all":
        return doc_type
    return DOC_TYPE_ALIASES.get(doc_type, doc_type)


# Embedding provider -> (default model id, default vector dimension).
#   gemini : Google Generative Language REST API, needs GEMINI_API_KEY (default)
#   local  : fastembed ONNX on CPU, offline-friendly (requires `pip install fastembed onnxruntime`)
_EMBED_PROVIDER = os.getenv("EMBED_PROVIDER", "gemini").strip().lower()
if _EMBED_PROVIDER not in ("local", "gemini"):
    _EMBED_PROVIDER = "gemini"

_EMBED_DEFAULTS = {
    "local": ("sentence-transformers/all-MiniLM-L6-v2", 384),
    "gemini": ("models/gemini-embedding-001", 768),
}
_DEFAULT_EMBED_MODEL, _DEFAULT_EMBED_DIM = _EMBED_DEFAULTS[_EMBED_PROVIDER]


class Settings:
    # --- LLM (Groq) ---
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    GROQ_MODEL: str = os.getenv("GROQ_MODEL", os.getenv("GROQ_MODEL_NAME", "qwen/qwen3.8-27b"))

    # --- Embeddings (Gemini by default; local fastembed is opt-in) ---
    EMBED_PROVIDER: str = _EMBED_PROVIDER
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    EMBEDDING_MODEL: str = os.getenv("EMBEDDING_MODEL_NAME") or _DEFAULT_EMBED_MODEL
    EMBEDDING_DIM: int = int(os.getenv("EMBEDDING_DIM") or _DEFAULT_EMBED_DIM)
    EMBED_BATCH_SIZE: int = int(os.getenv("EMBED_BATCH_SIZE", "16"))

    # --- Reranker (Cohere, with Groq LLM fallback) ---
    COHERE_API_KEY: str = os.getenv("COHERE_API_KEY", "")
    COHERE_RERANK_MODEL: str = os.getenv("COHERE_RERANK_MODEL", "rerank-v3.5")

    # --- Vector store (Qdrant embedded local mode; set QDRANT_URL for server mode) ---
    QDRANT_URL: str = os.getenv("QDRANT_URL", "")
    QDRANT_API_KEY: str = os.getenv("QDRANT_API_KEY", "")
    # Local default: on-disk store. On Vercel without QDRANT_URL: ephemeral /tmp instance.
    QDRANT_PATH: str = os.getenv(
        "QDRANT_PATH",
        str(Path("/tmp/qabuddy/qdrant") if IS_VERCEL else WORKSPACE_DIR / "storage" / "qdrant"),
    )
    COLLECTION_NAME: str = os.getenv("COLLECTION_NAME", "qabuddy_chunks")

    # --- Retrieval ---
    RETRIEVE_TOP_K: int = int(os.getenv("RETRIEVE_TOP_K", "30"))
    RERANK_TOP_N: int = int(os.getenv("RERANK_TOP_N", "20"))
    TOP_K: int = int(os.getenv("TOP_K", "5"))

    # --- Paths (on Vercel, writable state goes to /tmp; data/ is read-only bundle) ---
    DATA_DIR: Path = WORKSPACE_DIR / "data"
    STORAGE_DIR: Path = Path("/tmp/qabuddy") if IS_VERCEL else WORKSPACE_DIR / "storage"
    UPLOAD_DIR: Path = Path("/tmp/qabuddy/uploads") if IS_VERCEL else DATA_DIR / "uploads"
    PLAYWRIGHT_TESTS_DIR: Path = WORKSPACE_DIR / "Advance-Playwright-Framework" / "src" / "tests"
    PLAYWRIGHT_PAGES_DIR: Path = WORKSPACE_DIR / "Advance-Playwright-Framework" / "src" / "pages"
    PLAYWRIGHT_MODULES_DIR: Path = WORKSPACE_DIR / "Advance-Playwright-Framework" / "src" / "modules"
    # Cloned test-automation frameworks pulled via the UI (git clone/pull -> index).
    FRAMEWORKS_DIR: Path = Path("/tmp/qabuddy/frameworks") if IS_VERCEL else DATA_DIR / "frameworks"
    CACHE_DB: Path = STORAGE_DIR / "cache.sqlite3"

    ALLOWED_ORIGINS: list[str] = ["*"]


def _is_writable(path: Path) -> bool:
    """True when `path` can be created (if needed) and written to."""
    try:
        path.mkdir(parents=True, exist_ok=True)
        probe = path / ".write_probe"
        probe.write_bytes(b"")
        probe.unlink()
        return True
    except OSError:
        return False


settings = Settings()

# Vercel Functions are read-only outside /tmp, and the VERCEL probe can miss. Move every
# writable path under /tmp when the chosen state directory turns out not to be writable.
_state_read_only = not _is_writable(settings.STORAGE_DIR)
if _state_read_only:
    _fallback = Path("/tmp/qabuddy")
    if _is_writable(_fallback):
        settings.STORAGE_DIR = _fallback
        settings.CACHE_DB = _fallback / "cache.sqlite3"
        settings.UPLOAD_DIR = _fallback / "uploads"
        settings.FRAMEWORKS_DIR = _fallback / "frameworks"
        if not settings.QDRANT_URL:
            settings.QDRANT_PATH = str(_fallback / "qdrant")
        print(f"[config] state dir not writable; falling back to {_fallback} (ephemeral).")
    else:
        print("[config] WARNING: no writable state directory found; uploads will fail.")

# huggingface_hub / hf_xet stage the local embedding model under HF_HOME, which defaults
# outside /tmp; on a read-only host that raises "Read-only file system (os error 30)".
if IS_VERCEL or _state_read_only:
    os.environ.setdefault("HF_HOME", str(settings.STORAGE_DIR / "hf"))

if not settings.GROQ_API_KEY:
    print("[config] WARNING: GROQ_API_KEY is not set - LLM answers will fail.")
if settings.EMBED_PROVIDER == "local":
    print(f"[config] Embeddings: local ({settings.EMBEDDING_MODEL}, {settings.EMBEDDING_DIM}-d).")
elif not settings.GEMINI_API_KEY:
    print("[config] WARNING: GEMINI_API_KEY is not set - ingestion will fail.")
if not settings.COHERE_API_KEY:
    print("[config] INFO: COHERE_API_KEY not set - reranker will use the Groq fallback.")
