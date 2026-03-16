"""Project configuration loading and path resolution.

Discovers repo root, loads project.yaml, and resolves all paths to absolutes.
"""

from dataclasses import dataclass, field
from pathlib import Path

import structlog
import yaml

from cstudio.exceptions import ConfigError

log = structlog.get_logger()


# ── Repo root discovery ──────────────────────────────────────────────────────


def find_repo_root(start: Path | None = None) -> Path:
    """Walk up from start (default CWD) looking for .git/ + library/.

    Returns the content-studio repo root, or raises ConfigError.
    """
    current = (start or Path.cwd()).resolve()

    for directory in [current, *current.parents]:
        if (directory / ".git").is_dir() and (directory / "library").is_dir():
            log.debug("[CONFIG] repo root", path=str(directory))
            return directory

    raise ConfigError(
        f"Could not find content-studio repo root from {current}. "
        "Expected a parent directory containing both .git/ and library/."
    )


# ── Project YAML discovery ───────────────────────────────────────────────────


def find_project_yaml(start: Path | None = None) -> Path:
    """Walk up from start (default CWD) looking for project.yaml.

    Stops at the repo root (won't search above it).
    """
    current = (start or Path.cwd()).resolve()
    repo_root = find_repo_root(current)

    for directory in [current, *current.parents]:
        candidate = directory / "project.yaml"
        if candidate.is_file():
            log.debug("[CONFIG] found project.yaml", path=str(candidate))
            return candidate
        if directory == repo_root:
            break

    raise ConfigError(
        f"No project.yaml found between {current} and repo root {repo_root}."
    )


# ── Project config dataclass ─────────────────────────────────────────────────


@dataclass
class ProjectConfig:
    """Parsed and resolved project configuration."""

    # Identity
    name: str
    type: str  # "presentation", "blog", or "image"
    theme: str

    # Resolved absolute paths
    project_dir: Path
    repo_root: Path
    content_dir: Path  # Type-specific: slides/, diagrams/, or images/
    screenshots_dir: Path
    theme_dir: Path

    # Slide list (ordered) — used for all project types (slides, diagrams, images)
    slides: list[str] = field(default_factory=list)

    # Gold context
    gold_outline: str = ""  # from gold.outline

    # Blog-specific
    blog_file: str = ""  # from blog.file
    demo_video_script: str = ""  # from demo_video.script

    # Talk track (presentations)
    talk_track_file: str = ""  # from talk_track.file
    talk_track_tts_script: str = ""  # from talk_track.tts_script

    # Google integration
    drive_folder_id: str = ""
    presentation_title: str = ""

    # Audio config
    audio_voice_id: str = ""  # from audio.voice_id
    audio_output_dir: str = ""  # from audio.output_dir

    # Exports
    exports_dir: str = ""  # from exports_dir

    # Raw YAML for extensibility
    raw: dict = field(default_factory=dict, repr=False)

    @property
    def slides_dir(self) -> Path:
        """Alias for content_dir — backwards compatibility."""
        return self.content_dir


# ── Theme path resolution ────────────────────────────────────────────────────


def resolve_theme_path(repo_root: Path, theme_name: str) -> Path:
    """Resolve theme name to absolute path under library/themes/."""
    theme_dir = repo_root / "library" / "themes" / theme_name
    if not theme_dir.is_dir():
        raise ConfigError(
            f"Theme '{theme_name}' not found at {theme_dir}. "
            f"Available themes: {[d.name for d in (repo_root / 'library' / 'themes').iterdir() if d.is_dir()]}"
        )
    return theme_dir


# ── Load config ──────────────────────────────────────────────────────────────


def load_config(project_yaml: Path | None = None) -> ProjectConfig:
    """Load project.yaml and return a fully-resolved ProjectConfig.

    Args:
        project_yaml: Explicit path to project.yaml. If None, discovers it
                       by walking up from CWD.
    """
    if project_yaml is None:
        project_yaml = find_project_yaml()

    project_yaml = project_yaml.resolve()
    project_dir = project_yaml.parent

    log.info("[CONFIG] loading project", path=str(project_yaml))

    with open(project_yaml) as f:
        raw = yaml.safe_load(f)

    if not raw or not isinstance(raw, dict):
        raise ConfigError(f"Empty or invalid project.yaml: {project_yaml}")

    # Required fields
    name = raw.get("name")
    if not name:
        raise ConfigError("project.yaml missing required field: name")

    project_type = raw.get("type", "presentation")
    theme_name = raw.get("theme", "sacred-gold")

    # Discover repo root
    repo_root = find_repo_root(project_dir)

    # Resolve theme
    theme_dir = resolve_theme_path(repo_root, theme_name)

    # Resolve content directory based on project type
    if project_type == "blog":
        content_rel = raw.get("diagrams_dir", "diagrams")
    elif project_type == "image":
        content_rel = raw.get("images_dir", "images")
    else:  # presentation
        content_rel = raw.get("slides_dir", "slides")
    content_dir = (project_dir / content_rel).resolve()

    # Resolve screenshots directory
    default_screenshots = f"{content_rel}/screenshots"
    screenshots_rel = raw.get("screenshots_dir", default_screenshots)
    screenshots_dir = (project_dir / screenshots_rel).resolve()

    # Build ordered slide list
    slides = raw.get("slides", [])
    if isinstance(slides, list):
        # Ensure .html extension
        slides = [s if s.endswith(".html") else f"{s}.html" for s in slides]

    # Gold context
    gold = raw.get("gold", {}) or {}
    gold_outline = gold.get("outline", "")

    # Blog-specific
    blog = raw.get("blog", {}) or {}
    blog_file = blog.get("file", "")

    # Demo video
    demo_video = raw.get("demo_video", {}) or {}
    demo_video_script = demo_video.get("script", "")

    # Talk track (presentations)
    talk_track = raw.get("talk_track", {}) or {}
    talk_track_file = talk_track.get("file", "")
    talk_track_tts_script = talk_track.get("tts_script", "")

    # Google integration
    google = raw.get("google", {}) or {}
    drive_folder_id = google.get("drive_folder_id", "")
    presentation_title = google.get("presentation_title", name)

    # Audio config
    audio = raw.get("audio", {}) or {}
    audio_voice_id = audio.get("voice_id", "") or audio.get("voice", "")
    audio_output_dir = audio.get("output_dir", "")

    # Exports
    exports_dir = raw.get("exports_dir", "")

    config = ProjectConfig(
        name=name,
        type=project_type,
        theme=theme_name,
        project_dir=project_dir,
        repo_root=repo_root,
        content_dir=content_dir,
        screenshots_dir=screenshots_dir,
        theme_dir=theme_dir,
        slides=slides,
        gold_outline=gold_outline,
        blog_file=blog_file,
        demo_video_script=demo_video_script,
        talk_track_file=talk_track_file,
        talk_track_tts_script=talk_track_tts_script,
        drive_folder_id=drive_folder_id,
        presentation_title=presentation_title,
        audio_voice_id=audio_voice_id,
        audio_output_dir=audio_output_dir,
        exports_dir=exports_dir,
        raw=raw,
    )

    log.info(
        "[CONFIG] loaded",
        name=config.name,
        type=config.type,
        theme=config.theme,
        slides=len(config.slides),
    )

    return config
