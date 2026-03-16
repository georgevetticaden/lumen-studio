"""Project scaffolding — create new content projects from templates."""

import re
from datetime import date
from pathlib import Path

import structlog

from cstudio.exceptions import ConfigError

log = structlog.get_logger()

VALID_TYPES = {"presentation", "blog", "image"}


def scaffold_project(
    target: Path,
    theme: str,
    repo_root: Path,
    project_type: str | None = None,
    display_name: str | None = None,
) -> None:
    """Scaffold a new project at target from the appropriate template.

    Args:
        target: Absolute path for the new project directory.
        theme: Theme name (e.g. "sacred-gold", "clean-slate").
        repo_root: Content-studio repository root.
        project_type: Explicit project type. If None, inferred from path.
        display_name: Human-readable project name (e.g. "Sin & Virtue").
                      If None, falls back to the directory name.
    """
    if target.exists():
        raise ConfigError(f"Target directory already exists: {target}")

    # Determine project type
    if project_type is None:
        project_type = _infer_type(target)

    if project_type not in VALID_TYPES:
        raise ConfigError(
            f"Invalid project type '{project_type}'. "
            f"Valid types: {', '.join(sorted(VALID_TYPES))}"
        )

    log.info("[INIT] scaffolding project", type=project_type, path=str(target))

    # Find template
    template_dir = repo_root / "library" / "project-templates" / project_type

    if not template_dir.is_dir():
        raise ConfigError(f"Template directory not found: {template_dir}")

    # Create directory structure
    target.mkdir(parents=True, exist_ok=True)

    if project_type == "presentation":
        _scaffold_presentation(target)
    elif project_type == "blog":
        _scaffold_blog(target)
    else:
        _scaffold_image(target)

    # Create context directory (shared across all project types)
    _scaffold_context(target)

    # Write project.yaml from template
    _write_yaml(target, theme, template_dir, display_name)

    log.info("[INIT] complete", path=str(target))


def _infer_type(target: Path) -> str:
    """Infer project type from the target path."""
    path_str = str(target).lower()
    if "blog" in path_str:
        return "blog"
    elif "image" in path_str:
        return "image"
    else:
        return "presentation"


def _scaffold_presentation(target: Path) -> None:
    """Create presentation project structure."""
    for subdir in [
        "slides",
        "slides/screenshots",
        "slides/images",
        "slides/images/prompts",
        "talk-track",
        "talk-track/audio",
        "materials",
        "exports",
    ]:
        (target / subdir).mkdir(parents=True, exist_ok=True)


def _scaffold_blog(target: Path) -> None:
    """Create blog project structure."""
    for subdir in [
        "blog",
        "diagrams",
        "diagrams/screenshots",
        "diagrams/images",
        "diagrams/images/prompts",
        "demo-video",
        "linkedin-post",
    ]:
        (target / subdir).mkdir(parents=True, exist_ok=True)


def _scaffold_image(target: Path) -> None:
    """Create image project structure."""
    for subdir in ["images", "images/screenshots", "images/prompts"]:
        (target / subdir).mkdir(parents=True, exist_ok=True)


def _scaffold_context(target: Path) -> None:
    """Create standardized context directory."""
    for subdir in [
        "context/gold",
        "context/sources",
        "context/sources/transcripts",
        "context/sources/web",
        "context/prompts",
    ]:
        d = target / subdir
        d.mkdir(parents=True, exist_ok=True)
        # Add .gitkeep so empty dirs are tracked
        (d / ".gitkeep").touch()


def _derive_slug(name: str) -> str:
    """Derive a URL-friendly slug from the project directory name.

    Examples:
        '2026-02-my-project' → 'my-project'
        'My Cool Project' → 'my-cool-project'
    """
    # Strip leading YYYY-MM- date prefix if present
    slug = re.sub(r"^\d{4}-\d{2}-", "", name)
    # Lowercase, replace spaces/underscores with hyphens
    slug = slug.lower().replace(" ", "-").replace("_", "-")
    # Remove non-alphanumeric chars (except hyphens)
    slug = re.sub(r"[^a-z0-9-]", "", slug)
    # Collapse multiple hyphens
    slug = re.sub(r"-+", "-", slug).strip("-")
    return slug or "project"


def _write_yaml(
    target: Path,
    theme: str,
    template_dir: Path,
    display_name: str | None = None,
) -> None:
    """Write project.yaml from template with placeholder substitution."""
    name = display_name or target.name
    template_yaml = template_dir / "project.yaml.template"
    if template_yaml.is_file():
        content = template_yaml.read_text()
        content = content.replace("{{THEME}}", theme)
        content = content.replace("{{NAME}}", name)
        content = content.replace("{{DATE}}", date.today().isoformat())
        content = content.replace("{{SLUG}}", _derive_slug(target.name))
        (target / "project.yaml").write_text(content)
    else:
        _write_minimal_yaml(target, theme, template_dir.name, name)


def _write_minimal_yaml(
    target: Path, theme: str, project_type: str, display_name: str | None = None
) -> None:
    """Write a minimal project.yaml when no template is available."""
    name = display_name or target.name
    if project_type == "presentation":
        content = f"""name: "{name}"
type: presentation
theme: {theme}

slides_dir: slides
screenshots_dir: slides/screenshots

slides: []

google:
  drive_folder_id: null
  presentation_title: "{name}"
"""
    elif project_type == "blog":
        content = f"""name: "{name}"
type: blog
theme: {theme}

diagrams_dir: diagrams
screenshots_dir: diagrams/screenshots

slides: []

linkedin_post:
  file: linkedin-post/{_derive_slug(target.name)}-linkedin-v1.md
  published_url: null
"""
    else:
        content = f"""name: "{name}"
type: {project_type}
theme: {theme}

images_dir: images
screenshots_dir: images/screenshots

slides: []
"""
    (target / "project.yaml").write_text(content)
