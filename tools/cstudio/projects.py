"""List all projects in the content-studio repo."""

from pathlib import Path

import structlog
import yaml

from cstudio.config import find_repo_root

log = structlog.get_logger()


def list_projects(repo_root: Path | None = None) -> list[dict]:
    """Scan for all project.yaml files and return project metadata.

    Returns a list of dicts sorted by date (newest first), then name.
    """
    root = repo_root or find_repo_root()
    projects_dir = root / "projects"

    if not projects_dir.is_dir():
        return []

    results = []
    for yaml_path in sorted(projects_dir.rglob("project.yaml")):
        try:
            data = yaml.safe_load(yaml_path.read_text())
        except Exception as e:
            log.warning("[PROJECTS] failed to parse", path=str(yaml_path), error=str(e))
            continue

        if not isinstance(data, dict) or "name" not in data:
            continue

        slides = data.get("slides", []) or []
        google = data.get("google", {}) or {}
        published = bool(google.get("presentation_id") or google.get("drive_folder_id"))

        results.append({
            "name": data["name"],
            "type": data.get("type", "presentation"),
            "theme": data.get("theme", "sacred-gold"),
            "date": str(data["date"]) if data.get("date") else "",
            "slide_count": len(slides),
            "published": published,
            "rel_path": str(yaml_path.parent.relative_to(projects_dir)),
            "project_dir": yaml_path.parent,
        })

    # Sort by date descending, then name ascending
    results.sort(key=lambda p: (p["date"] or "", p["name"]), reverse=True)
    # Secondary sort: for same date, sort name ascending
    results.sort(key=lambda p: p["date"] or "", reverse=True)

    return results
