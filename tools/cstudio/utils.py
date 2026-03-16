"""Utility functions for credential management and common operations."""

import os
import pickle
from pathlib import Path

import structlog
from dotenv import load_dotenv

from cstudio.exceptions import CredentialError

log = structlog.get_logger()

# ── Credential paths ─────────────────────────────────────────────────────────

_DEFAULT_CRED_DIR = Path.home() / ".content-studio"

GOOGLE_SCOPES = [
    "https://www.googleapis.com/auth/presentations",
    "https://www.googleapis.com/auth/drive.file",
]


def _resolve_cred_dir() -> Path:
    """Resolve credential directory.

    Resolution order:
    1. CSTUDIO_CREDENTIALS_DIR env var (must exist if set)
    2. .env file at repo root (loaded via python-dotenv)
    3. Default ~/.content-studio/ (auto-created)
    """
    # Load .env from repo root (if findable), won't override existing env vars
    try:
        from cstudio.config import find_repo_root

        repo_root = find_repo_root()
        env_file = repo_root / ".env"
        if env_file.is_file():
            load_dotenv(env_file, override=False)
    except Exception:
        pass  # Resilient — works outside the repo too

    env_dir = os.environ.get("CSTUDIO_CREDENTIALS_DIR")
    if env_dir:
        cred_dir = Path(env_dir).expanduser().resolve()
        if not cred_dir.is_dir():
            raise CredentialError(
                f"CSTUDIO_CREDENTIALS_DIR points to a non-existent directory: {cred_dir}"
            )
        log.debug("[CRED] using configured credential dir", path=str(cred_dir))
        return cred_dir

    # Default — auto-create
    _DEFAULT_CRED_DIR.mkdir(parents=True, exist_ok=True)
    return _DEFAULT_CRED_DIR


def _find_client_secret(cred_dir: Path) -> Path:
    """Find client_secret*.json in the credential directory.

    Supports Google's long auto-generated filenames like
    client_secret_672772065866-abc123.apps.googleusercontent.com.json.
    """
    matches = sorted(cred_dir.glob("client_secret*.json"))
    if not matches:
        raise CredentialError(
            f"No client_secret*.json found in {cred_dir}. "
            "Download your OAuth client secret from Google Cloud Console "
            "and place it in the credential directory."
        )
    if len(matches) > 1:
        log.warning(
            "[CRED] multiple client_secret files found, using first",
            files=[m.name for m in matches],
        )
    return matches[0]


# ── Google OAuth credentials ─────────────────────────────────────────────────


def load_google_credentials():
    """Load or refresh Google OAuth credentials.

    Finds credentials using the configured credential directory
    (env var → .env → ~/.content-studio/) and globs for client_secret*.json.

    Returns a google.oauth2.credentials.Credentials object.
    """
    # Lazy imports — only needed when publishing to Google
    from google.auth.transport.requests import Request
    from google_auth_oauthlib.flow import InstalledAppFlow

    cred_dir = _resolve_cred_dir()
    client_secret = _find_client_secret(cred_dir)
    token_file = cred_dir / "token.pickle"

    log.debug(
        "[CRED] loading google credentials",
        cred_dir=str(cred_dir),
        client_secret=client_secret.name,
        token_file=str(token_file),
    )

    creds = None
    if token_file.is_file():
        with open(token_file, "rb") as f:
            creds = pickle.load(f)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            log.info("[CRED] refreshing expired token")
            creds.refresh(Request())
        else:
            log.info("[CRED] starting OAuth flow")
            flow = InstalledAppFlow.from_client_secrets_file(
                str(client_secret), GOOGLE_SCOPES
            )
            creds = flow.run_local_server(port=0)

        with open(token_file, "wb") as f:
            pickle.dump(creds, f)
        log.info("[CRED] token saved", path=str(token_file))

    return creds


# ── API key loading ──────────────────────────────────────────────────────────


def load_api_key(service: str) -> str:
    """Load an API key from the credential directory.

    Args:
        service: Service name (e.g. "openai", "elevenlabs").

    Returns:
        The API key string, stripped of whitespace.
    """
    cred_dir = _resolve_cred_dir()
    key_file = cred_dir / f"{service}.key"

    if not key_file.is_file():
        raise CredentialError(
            f"API key not found at {key_file}. "
            f"Create the file with your {service} API key."
        )

    key = key_file.read_text().strip()
    if not key:
        raise CredentialError(f"API key file is empty: {key_file}")

    log.debug("[CRED] loaded API key", service=service)
    return key


# ── Slide dimensions (EMU) ───────────────────────────────────────────────────

# Standard 16:9 = 10" x 5.625" in EMU (1 inch = 914400 EMU)
SLIDE_WIDTH_EMU = 9144000
SLIDE_HEIGHT_EMU = 5143500
