"""Publish and sync presentations to Google Slides.

Handles the full lifecycle:
- publish: Create a new Google Slides deck from screenshots
- sync: Update all or individual slides in an existing deck
- export: Export deck as PDF
"""

from pathlib import Path

import structlog
import yaml

from cstudio.config import ProjectConfig
from cstudio.exceptions import PublishError
from cstudio.gslides import (
    add_slides,
    create_presentation,
    delete_slides,
    export_as_pdf,
    get_slide_index,
    replace_slide_image,
    upload_screenshot,
)
from cstudio.screenshots import screenshot_slides

log = structlog.get_logger()


# ── Slide mapping ────────────────────────────────────────────────────────────
#
# The slide_mapping in project.yaml tracks the relationship between
# HTML slides and Google Slides pages:
#
#   google:
#     presentation_id: "abc123"
#     slide_mapping:
#       - html_file: slide-01-title.html
#         builds:
#           - screenshot: slide-01-title-full.png
#             slide_id: slide_abc123
#             image_id: image_def456
#       - html_file: slide-02-intro.html
#         builds:
#           - screenshot: slide-02-intro-build-0.png
#             slide_id: slide_ghi789
#             image_id: image_jkl012
#           - screenshot: slide-02-intro-build-1.png
#             slide_id: slide_mno345
#             image_id: image_pqr678
#


def _save_google_config(config: ProjectConfig, presentation_id: str, slide_mapping: list[dict]) -> None:
    """Save presentation_id and slide_mapping back to project.yaml."""
    yaml_path = config.project_dir / "project.yaml"
    with open(yaml_path) as f:
        raw = yaml.safe_load(f)

    if "google" not in raw:
        raw["google"] = {}

    raw["google"]["presentation_id"] = presentation_id
    raw["google"]["slide_mapping"] = slide_mapping

    with open(yaml_path, "w") as f:
        yaml.dump(raw, f, default_flow_style=False, sort_keys=False, allow_unicode=True)

    log.info("[PUBLISH] saved mapping to project.yaml", slides=len(slide_mapping))


def _load_google_config(config: ProjectConfig) -> tuple[str, list[dict]]:
    """Load presentation_id and slide_mapping from project.yaml.

    Returns (presentation_id, slide_mapping).
    Raises PublishError if not published yet.
    """
    google = config.raw.get("google", {}) or {}
    presentation_id = google.get("presentation_id")
    if not presentation_id:
        raise PublishError(
            "No presentation_id in project.yaml. Run 'cstudio publish' first."
        )

    slide_mapping = google.get("slide_mapping", [])
    return presentation_id, slide_mapping


def _group_screenshots_by_slide(
    screenshots: list[Path], slide_files: list[str]
) -> dict[str, list[Path]]:
    """Group screenshot paths by their HTML slide file.

    Returns dict mapping html_file -> list of screenshot paths (in build order).
    """
    grouped: dict[str, list[Path]] = {}

    for slide_file in slide_files:
        stem = Path(slide_file).stem
        # Find all screenshots for this slide (full or build-N)
        matching = sorted(
            [s for s in screenshots if s.stem.startswith(stem)],
            key=lambda p: p.stem,
        )
        if matching:
            grouped[slide_file] = matching

    return grouped


# ── Publish (create new deck) ────────────────────────────────────────────────


def publish_presentation(config: ProjectConfig) -> str:
    """Create a new Google Slides deck from all project screenshots.

    Steps:
    1. Screenshot all slides
    2. Create Google Slides presentation
    3. Upload all screenshots to Drive
    4. Add slides with full-bleed images
    5. Save mapping to project.yaml

    Returns the Google Slides URL.
    """
    # Check for existing presentation
    google = config.raw.get("google", {}) or {}
    if google.get("presentation_id"):
        raise PublishError(
            f"Already published as {google['presentation_id']}. "
            "Use 'cstudio sync' to update, or remove google.presentation_id "
            "from project.yaml to create a new deck."
        )

    # 1. Check for Drive folder ID (fail fast before screenshotting)
    folder_id = config.drive_folder_id or None
    if not folder_id:
        raise PublishError(
            "No google.drive_folder_id in project.yaml. "
            "Set it to a Google Drive folder ID where the presentation "
            "and screenshots will be stored. "
            "You can get this from a Drive folder URL: "
            "https://drive.google.com/drive/folders/<FOLDER_ID>"
        )

    # 2. Screenshot all slides
    log.info("[PUBLISH] capturing all slides")
    screenshots = screenshot_slides(config)

    if not screenshots:
        raise PublishError("No screenshots generated. Check your slides.")

    # 3. Group screenshots by HTML slide
    grouped = _group_screenshots_by_slide(screenshots, config.slides)

    # 4. Create presentation
    title = config.presentation_title or config.name
    presentation_id = create_presentation(title, folder_id)

    # 5. Upload all screenshots and add slides
    all_image_urls = []
    screenshot_names = []
    for slide_file in config.slides:
        if slide_file not in grouped:
            continue
        for png_path in grouped[slide_file]:
            url = upload_screenshot(png_path, folder_id)
            all_image_urls.append(url)
            screenshot_names.append((slide_file, png_path.name))

    # 6. Add all slides at once
    slide_info_list = add_slides(presentation_id, all_image_urls)

    # 7. Build slide_mapping
    slide_mapping = []
    idx = 0
    for slide_file in config.slides:
        if slide_file not in grouped:
            continue
        builds = []
        for png_path in grouped[slide_file]:
            if idx < len(slide_info_list):
                info = slide_info_list[idx]
                builds.append(
                    {
                        "screenshot": png_path.name,
                        "slide_id": info["slide_id"],
                        "image_id": info["image_id"],
                    }
                )
                idx += 1
        slide_mapping.append({"html_file": slide_file, "builds": builds})

    # 8. Save to project.yaml
    _save_google_config(config, presentation_id, slide_mapping)

    url = f"https://docs.google.com/presentation/d/{presentation_id}/edit"
    total_gslides = sum(len(m["builds"]) for m in slide_mapping)
    log.info(
        "[PUBLISH] complete",
        presentation_id=presentation_id,
        html_slides=len(slide_mapping),
        google_slides=total_gslides,
        url=url,
    )
    return url


# ── Sync (update existing deck) ─────────────────────────────────────────────


def sync_all(config: ProjectConfig) -> str:
    """Update all slides in the existing Google Slides deck.

    Re-screenshots everything and replaces images on existing Google Slides.
    Handles build count changes per slide.

    Returns the Google Slides URL.
    """
    presentation_id, slide_mapping = _load_google_config(config)

    # Screenshot all slides
    log.info("[SYNC] capturing all slides")
    screenshots = screenshot_slides(config)
    grouped = _group_screenshots_by_slide(screenshots, config.slides)

    folder_id = config.drive_folder_id or None
    updated_mapping = []

    for mapping_entry in slide_mapping:
        html_file = mapping_entry["html_file"]
        old_builds = mapping_entry["builds"]

        if html_file not in grouped:
            # Slide no longer exists — keep old mapping entry as-is
            updated_mapping.append(mapping_entry)
            continue

        new_screenshots = grouped[html_file]

        if len(new_screenshots) == len(old_builds):
            # Same build count — replace images in-place
            new_builds = []
            for old_build, png_path in zip(old_builds, new_screenshots):
                url = upload_screenshot(png_path, folder_id)
                new_image_id = replace_slide_image(
                    presentation_id,
                    old_build["slide_id"],
                    old_build["image_id"],
                    url,
                )
                new_builds.append(
                    {
                        "screenshot": png_path.name,
                        "slide_id": old_build["slide_id"],
                        "image_id": new_image_id,
                    }
                )
            updated_mapping.append({"html_file": html_file, "builds": new_builds})
            log.info("[SYNC] updated slide", html_file=html_file, builds=len(new_builds))
        else:
            # Build count changed — delete old slides, insert new ones
            new_builds = _handle_build_count_change(
                presentation_id,
                old_builds,
                new_screenshots,
                folder_id,
            )
            updated_mapping.append({"html_file": html_file, "builds": new_builds})
            log.info(
                "[SYNC] rebuilt slide",
                html_file=html_file,
                old_count=len(old_builds),
                new_count=len(new_builds),
            )

    # ── Add new slides not yet in mapping ──
    mapped_files = {m["html_file"] for m in updated_mapping}
    new_slides = [s for s in config.slides if s in grouped and s not in mapped_files]

    if new_slides:
        log.info("[SYNC] adding new slides", count=len(new_slides))
        for html_file in new_slides:
            new_screenshots = grouped[html_file]
            image_urls = []
            for png_path in new_screenshots:
                url = upload_screenshot(png_path, folder_id)
                image_urls.append(url)

            # Append to end of deck
            slide_info_list = add_slides(presentation_id, image_urls)

            new_builds = []
            for png_path, info in zip(new_screenshots, slide_info_list):
                new_builds.append(
                    {
                        "screenshot": png_path.name,
                        "slide_id": info["slide_id"],
                        "image_id": info["image_id"],
                    }
                )
            updated_mapping.append({"html_file": html_file, "builds": new_builds})
            log.info(
                "[SYNC] added new slide",
                html_file=html_file,
                builds=len(new_builds),
            )

    _save_google_config(config, presentation_id, updated_mapping)

    url = f"https://docs.google.com/presentation/d/{presentation_id}/edit"
    log.info("[SYNC] complete", total_slides=len(updated_mapping))
    return url


def sync_single_slide(config: ProjectConfig, slide_filter: str) -> str:
    """Update a single slide in the existing Google Slides deck.

    Args:
        config: Project configuration.
        slide_filter: Slide name, number, or partial match.

    Returns the Google Slides URL.
    """
    from cstudio.screenshots import _resolve_slide_filter

    presentation_id, slide_mapping = _load_google_config(config)

    # Resolve which slide to sync
    matched = _resolve_slide_filter(config.slides, slide_filter)
    if not matched:
        raise PublishError(f"No slides matched filter: {slide_filter}")
    if len(matched) > 1:
        raise PublishError(
            f"Filter '{slide_filter}' matched multiple slides: {matched}. "
            "Be more specific."
        )

    html_file = matched[0]

    # Find this slide in the mapping
    mapping_idx = None
    old_entry = None
    for i, entry in enumerate(slide_mapping):
        if entry["html_file"] == html_file:
            mapping_idx = i
            old_entry = entry
            break

    # Screenshot just this slide
    log.info("[SYNC] capturing single slide", slide=html_file)
    screenshots = screenshot_slides(config, slide_filter)
    grouped = _group_screenshots_by_slide(screenshots, [html_file])

    if html_file not in grouped:
        raise PublishError(f"No screenshots generated for {html_file}")

    new_screenshots = grouped[html_file]
    folder_id = config.drive_folder_id or None

    if mapping_idx is None:
        # New slide not yet in mapping — add to end of deck
        log.info("[SYNC] adding new slide to deck", html_file=html_file)
        image_urls = []
        for png_path in new_screenshots:
            url = upload_screenshot(png_path, folder_id)
            image_urls.append(url)

        slide_info_list = add_slides(presentation_id, image_urls)

        new_builds = []
        for png_path, info in zip(new_screenshots, slide_info_list):
            new_builds.append(
                {
                    "screenshot": png_path.name,
                    "slide_id": info["slide_id"],
                    "image_id": info["image_id"],
                }
            )
        slide_mapping.append({"html_file": html_file, "builds": new_builds})
        log.info(
            "[SYNC] added new slide",
            html_file=html_file,
            builds=len(new_builds),
        )
    elif len(new_screenshots) == len(old_entry["builds"]):
        # Same build count — replace images in-place
        old_builds = old_entry["builds"]
        new_builds = []
        for old_build, png_path in zip(old_builds, new_screenshots):
            url = upload_screenshot(png_path, folder_id)
            new_image_id = replace_slide_image(
                presentation_id,
                old_build["slide_id"],
                old_build["image_id"],
                url,
            )
            new_builds.append(
                {
                    "screenshot": png_path.name,
                    "slide_id": old_build["slide_id"],
                    "image_id": new_image_id,
                }
            )
        slide_mapping[mapping_idx] = {"html_file": html_file, "builds": new_builds}
        log.info("[SYNC] updated slide", html_file=html_file, builds=len(new_builds))
    else:
        # Build count changed — delete + reinsert
        new_builds = _handle_build_count_change(
            presentation_id,
            old_entry["builds"],
            new_screenshots,
            folder_id,
        )
        slide_mapping[mapping_idx] = {"html_file": html_file, "builds": new_builds}
        log.info(
            "[SYNC] rebuilt slide",
            html_file=html_file,
            old_count=len(old_entry["builds"]),
            new_count=len(new_builds),
        )

    _save_google_config(config, presentation_id, slide_mapping)

    url = f"https://docs.google.com/presentation/d/{presentation_id}/edit"
    return url


def _handle_build_count_change(
    presentation_id: str,
    old_builds: list[dict],
    new_screenshots: list[Path],
    folder_id: str | None,
) -> list[dict]:
    """Handle a slide whose build count changed.

    Deletes old Google Slides and inserts new ones at the same position.

    Returns the new builds list for the mapping.
    """
    if not old_builds:
        raise PublishError("Cannot handle build count change with empty old_builds")

    # Find the position of the first old slide
    first_slide_id = old_builds[0]["slide_id"]
    try:
        insert_index = get_slide_index(presentation_id, first_slide_id)
    except PublishError:
        # If slide not found, append to end
        insert_index = None

    # Delete old slides
    old_slide_ids = [b["slide_id"] for b in old_builds]
    delete_slides(presentation_id, old_slide_ids)

    # Upload new screenshots
    image_urls = []
    for png_path in new_screenshots:
        url = upload_screenshot(png_path, folder_id)
        image_urls.append(url)

    # Insert new slides at the same position
    slide_info_list = add_slides(presentation_id, image_urls, insert_at=insert_index)

    # Build new mapping entries
    new_builds = []
    for png_path, info in zip(new_screenshots, slide_info_list):
        new_builds.append(
            {
                "screenshot": png_path.name,
                "slide_id": info["slide_id"],
                "image_id": info["image_id"],
            }
        )

    return new_builds


# ── Export ───────────────────────────────────────────────────────────────────


def export_presentation(config: ProjectConfig) -> Path:
    """Export the published Google Slides deck as PDF.

    Saves to {exports_dir}/{name}-deck.pdf.

    Returns the output path.
    """
    presentation_id, _ = _load_google_config(config)

    # Resolve output path
    exports_dir = config.exports_dir or "exports"
    output_dir = config.project_dir / exports_dir
    output_dir.mkdir(parents=True, exist_ok=True)

    # Slugify the name for the filename
    slug = config.name.lower().replace(" ", "-").replace("&", "and")
    output_path = output_dir / f"{slug}-deck.pdf"

    export_as_pdf(presentation_id, output_path)
    return output_path
