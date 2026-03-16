"""Custom exception hierarchy for cstudio CLI."""


class CStudioError(Exception):
    """Base exception for all cstudio errors."""


class ConfigError(CStudioError):
    """Project configuration errors (missing project.yaml, invalid fields)."""


class CredentialError(CStudioError):
    """Credential loading failures (missing files, expired tokens)."""


class ScreenshotError(CStudioError):
    """Screenshot capture failures."""


class BrowserError(CStudioError):
    """Headless browser setup or communication failures."""


class PublishError(CStudioError):
    """Google Slides publish/sync/export failures."""


class ImageError(CStudioError):
    """Image generation failures (Gemini API, prompt parsing, embedding)."""
