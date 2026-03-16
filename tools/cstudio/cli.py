"""CLI entry point for cstudio.

Usage:
    cstudio status                          # Show project info
    cstudio screenshot                      # All slides → PNGs
    cstudio screenshot slide-01-title       # Single slide
    cstudio screenshot --slide 5            # By number
    cstudio init <path> --theme <theme>     # Scaffold new project
    cstudio publish                         # Create Google Slides deck
    cstudio sync                            # Update all slides in deck
    cstudio sync --slide 5                  # Update single slide
    cstudio export                          # Export deck as PDF
"""

import argparse
import sys
from pathlib import Path

import structlog

from cstudio import __version__
from cstudio.exceptions import CStudioError
from cstudio.logging_config import configure_logging

log = structlog.get_logger()


def main(argv: list[str] | None = None) -> None:
    """Parse arguments and route to the appropriate command handler."""
    configure_logging()

    parser = argparse.ArgumentParser(
        prog="cstudio",
        description="Content Studio CLI — screenshots, publishing, and project scaffolding",
    )
    parser.add_argument(
        "--version", action="version", version=f"cstudio {__version__}"
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # ── status ────────────────────────────────────────────────────────────
    subparsers.add_parser("status", help="Show project info from project.yaml")

    # ── screenshot ────────────────────────────────────────────────────────
    p_screenshot = subparsers.add_parser(
        "screenshot", help="Capture slide screenshots as PNGs"
    )
    p_screenshot.add_argument(
        "filter",
        nargs="?",
        default=None,
        help="Slide name, stem, or partial match (e.g. 'slide-01-title', 'title')",
    )
    p_screenshot.add_argument(
        "--slide",
        type=str,
        default=None,
        help="Slide number (e.g. 5 or 05)",
    )

    # ── init ──────────────────────────────────────────────────────────────
    p_init = subparsers.add_parser("init", help="Scaffold a new project")
    p_init.add_argument("path", help="Target directory for the new project")
    p_init.add_argument(
        "--theme",
        default="sacred-gold",
        help="Theme name (default: sacred-gold)",
    )
    p_init.add_argument(
        "--type",
        dest="project_type",
        choices=["presentation", "blog", "image"],
        default=None,
        help="Project type (default: inferred from path)",
    )
    p_init.add_argument(
        "--name",
        default=None,
        help='Display name for the project (e.g., "Sin & Virtue")',
    )

    # ── scrape ─────────────────────────────────────────────────────────────
    p_scrape = subparsers.add_parser(
        "scrape", help="Extract webpage content using headless Chrome"
    )
    p_scrape.add_argument("url", help="URL to scrape")
    p_scrape.add_argument(
        "--output",
        "-o",
        default=None,
        help="Output file path (default: stdout)",
    )
    p_scrape.add_argument(
        "--wait",
        type=int,
        default=5,
        help="Seconds to wait for page load (default: 5)",
    )

    # ── transcribe ─────────────────────────────────────────────────────────
    p_transcribe = subparsers.add_parser(
        "transcribe",
        help="Download YouTube audio and transcribe with Whisper",
    )
    p_transcribe.add_argument("url", help="YouTube video URL")
    p_transcribe.add_argument(
        "--output",
        "-o",
        default=None,
        help="Output file path (default: stdout)",
    )
    p_transcribe.add_argument(
        "--model",
        default="base",
        choices=["tiny", "base", "small", "medium", "large"],
        help="Whisper model size (default: base)",
    )

    # ── publish ─────────────────────────────────────────────────────────
    subparsers.add_parser(
        "publish", help="Create a new Google Slides deck from all screenshots"
    )

    # ── sync ───────────────────────────────────────────────────────────
    p_sync = subparsers.add_parser(
        "sync", help="Update slides in an existing Google Slides deck"
    )
    p_sync.add_argument(
        "filter",
        nargs="?",
        default=None,
        help="Slide name, stem, or partial match for single-slide sync",
    )
    p_sync.add_argument(
        "--slide",
        type=str,
        default=None,
        help="Slide number for single-slide sync (e.g. 5 or 05)",
    )

    # ── export ─────────────────────────────────────────────────────────
    p_export = subparsers.add_parser(
        "export", help="Export Google Slides deck as PDF"
    )
    p_export.add_argument(
        "--format",
        default="pdf",
        choices=["pdf"],
        help="Export format (default: pdf)",
    )

    # ── projects ───────────────────────────────────────────────────────────
    subparsers.add_parser("projects", help="List all projects in the repo")

    # ── image ──────────────────────────────────────────────────────────────
    p_image = subparsers.add_parser(
        "image", help="Generate image from placeholder prompt via Gemini API"
    )
    p_image.add_argument(
        "filter", help="Slide name, stem, or partial match"
    )
    p_image.add_argument(
        "--prompt", default=None, help="Override prompt (inline text, bypasses prompt file)"
    )
    p_image.add_argument(
        "--quality",
        default="standard",
        choices=["standard", "high"],
        help="Model quality: standard (flash) or high (pro) — default: standard",
    )

    # ── stubs for future commands ─────────────────────────────────────────
    subparsers.add_parser("audio", help="Generate audio narration (coming soon)")

    args = parser.parse_args(argv)

    if not args.command:
        parser.print_help()
        sys.exit(1)

    # Route to handler
    handlers = {
        "status": cmd_status,
        "screenshot": cmd_screenshot,
        "init": cmd_init,
        "scrape": cmd_scrape,
        "transcribe": cmd_transcribe,
        "publish": cmd_publish,
        "sync": cmd_sync,
        "export": cmd_export,
        "projects": cmd_projects,
        "image": cmd_image,
        "audio": cmd_stub,
    }

    try:
        handlers[args.command](args)
    except CStudioError as e:
        log.error(f"[CLI] {e}")
        sys.exit(1)


# ── Command handlers ──────────────────────────────────────────────────────────


def cmd_status(args: argparse.Namespace) -> None:
    """Show project info from project.yaml."""
    from cstudio.config import load_config

    config = load_config()

    # Type-specific labels
    content_labels = {
        "presentation": ("Slides dir", "Slides"),
        "blog": ("Diagrams dir", "Diagrams"),
        "image": ("Images dir", "Images"),
    }
    dir_label, items_label = content_labels.get(config.type, ("Content dir", "Files"))

    print(f"\n  Project:      {config.name}")
    print(f"  Type:         {config.type}")
    print(f"  Theme:        {config.theme}")
    print(f"  {dir_label}:  {config.content_dir}")
    print(f"  Screenshots:  {config.screenshots_dir}")
    print(f"  {items_label}:     {len(config.slides)}")

    if config.slides:
        for i, s in enumerate(config.slides, 1):
            print(f"    {i:2d}. {s}")

    if config.drive_folder_id:
        print(f"  Drive folder: {config.drive_folder_id}")

    print()


def cmd_screenshot(args: argparse.Namespace) -> None:
    """Capture slide screenshots as PNGs."""
    from cstudio.config import load_config
    from cstudio.screenshots import screenshot_slides

    config = load_config()

    # Resolve filter: --slide N takes priority over positional
    slide_filter = args.slide or args.filter

    screenshots = screenshot_slides(config, slide_filter)

    print(f"\n  {len(screenshots)} PNGs (2x retina)")
    print(f"  Saved to: {config.screenshots_dir}\n")


def cmd_init(args: argparse.Namespace) -> None:
    """Scaffold a new project."""
    from cstudio.config import find_repo_root
    from cstudio.init import scaffold_project

    repo_root = find_repo_root()
    target = Path(args.path)

    # If relative, resolve from repo root
    if not target.is_absolute():
        target = repo_root / target

    scaffold_project(
        target, args.theme, repo_root, args.project_type, args.name
    )

    display = args.name or target.name
    print(f"\n  Project scaffolded: {display}")
    print(f"  Path: {target}")
    print(f"  Theme: {args.theme}")
    print(f"  Next: add context sources, then create content\n")


def cmd_scrape(args: argparse.Namespace) -> None:
    """Extract webpage content using headless Chrome."""
    from datetime import date

    from cstudio.scrape import scrape_url, slugify

    result = scrape_url(args.url, wait_seconds=args.wait)

    # Format as markdown
    md = (
        f"# {result['title']}\n"
        f"Source: {result['url']}\n"
        f"Extracted: {date.today().isoformat()}\n"
        f"\n---\n\n"
        f"{result['content']}\n"
    )

    if args.output:
        out = Path(args.output)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(md)
        print(f"\n  Saved: {out}")
    else:
        print(md)

    print(f"\n  Title: {result['title']}")
    print(f"  Words: ~{result['word_count']}")
    if args.output:
        print(f"  File:  {args.output}")
    print()


def cmd_transcribe(args: argparse.Namespace) -> None:
    """Download YouTube audio and transcribe with Whisper."""
    from datetime import date

    from cstudio.transcribe import slugify, transcribe_youtube

    result = transcribe_youtube(args.url, model_name=args.model)

    # Format as markdown
    md = (
        f"# YouTube Transcript: {result['title']}\n"
        f"Source: {result['url']}\n"
        f"Duration: {result['duration']}\n"
        f"Extracted: {date.today().isoformat()}\n"
        f"Method: Whisper ({args.model} model)\n"
        f"\n---\n\n"
        f"{result['text']}\n"
    )

    if args.output:
        out = Path(args.output)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(md)
        print(f"\n  Saved: {out}")
    else:
        print(md)

    print(f"\n  Title:    {result['title']}")
    print(f"  Duration: {result['duration']}")
    print(f"  Words:    ~{result['word_count']}")
    print(f"  Time:     {result['transcribe_seconds']}s (Whisper {args.model})")
    if args.output:
        print(f"  File:     {args.output}")
    print()


def cmd_publish(args: argparse.Namespace) -> None:
    """Create a new Google Slides deck from all screenshots."""
    from cstudio.config import load_config
    from cstudio.publish import publish_presentation

    config = load_config()
    url = publish_presentation(config)

    # Count total Google Slides pages
    google = config.raw.get("google", {}) or {}
    # Re-read to get updated mapping
    from cstudio.config import load_config as reload

    updated = reload(config.project_dir / "project.yaml")
    mapping = updated.raw.get("google", {}).get("slide_mapping", [])
    total_pages = sum(len(m.get("builds", [])) for m in mapping)

    print(f"\n  Published to Google Slides!")
    print(f"  URL: {url}")
    print(f"  HTML slides: {len(config.slides)}")
    print(f"  Google Slides pages: {total_pages}")
    print(f"  Use 'cstudio sync --slide N' for future updates\n")


def cmd_sync(args: argparse.Namespace) -> None:
    """Sync slides to Google Slides."""
    from cstudio.config import load_config
    from cstudio.publish import sync_all, sync_single_slide

    config = load_config()

    # Resolve filter: --slide N takes priority over positional
    slide_filter = args.slide or args.filter

    if slide_filter:
        url = sync_single_slide(config, slide_filter)
        print(f"\n  Synced slide '{slide_filter}' to Google Slides")
    else:
        url = sync_all(config)
        print(f"\n  Synced all slides to Google Slides")

    print(f"  URL: {url}\n")


def cmd_export(args: argparse.Namespace) -> None:
    """Export Google Slides deck as PDF."""
    from cstudio.config import load_config
    from cstudio.publish import export_presentation

    config = load_config()
    output_path = export_presentation(config)

    size_kb = output_path.stat().st_size // 1024
    print(f"\n  Exported PDF: {output_path}")
    print(f"  Size: {size_kb} KB\n")


def cmd_image(args: argparse.Namespace) -> None:
    """Generate image from placeholder prompt via Gemini API."""
    from cstudio.config import load_config
    from cstudio.images import (
        QUALITY_MODELS,
        embed_image,
        generate_image,
        load_prompt,
        parse_placeholder,
    )
    from cstudio.screenshots import _resolve_slide_filter

    config = load_config()

    # Resolve slide file
    matches = _resolve_slide_filter(config.slides, args.filter)
    if not matches:
        log.error(f"[CLI] No slides matched filter: {args.filter}")
        sys.exit(1)
    slide_file = matches[0]
    html_path = (config.content_dir / slide_file).resolve()

    if not html_path.is_file():
        log.error(f"[CLI] Slide file not found: {html_path}")
        sys.exit(1)

    # Parse placeholder
    placeholder = parse_placeholder(html_path)

    # Determine prompt and aspect_ratio
    if args.prompt:
        # Inline override
        prompt_text = args.prompt
        aspect_ratio = "16:9"
    elif placeholder["prompt_path"]:
        # External prompt file
        prompt_data = load_prompt(placeholder["prompt_path"])
        prompt_text = prompt_data["text"]
        aspect_ratio = prompt_data["aspect_ratio"]
    elif placeholder["inline_text"]:
        # Fallback to inline text
        prompt_text = placeholder["inline_text"]
        aspect_ratio = "16:9"
    else:
        log.error("[CLI] No prompt found — no data-prompt attribute, no inline text, and no --prompt flag")
        sys.exit(1)

    # Model: from .env via QUALITY_MODELS, selected by --quality flag
    model = QUALITY_MODELS[args.quality]

    # Determine output path
    if placeholder["prompt_path"]:
        # Derive name from prompt file: slide-03-books-collage-v2.md → slide-03-books-collage.png
        stem = placeholder["prompt_path"].stem
        # Strip version suffix (e.g., -v1, -v2)
        import re
        stem = re.sub(r"-v\d+$", "", stem)
        image_name = f"{stem}.png"
    else:
        # Derive from slide name
        image_name = f"{Path(slide_file).stem}-image.png"

    images_dir = config.content_dir / "images"
    output_path = images_dir / image_name

    # Generate
    generate_image(prompt_text, output_path, aspect_ratio=aspect_ratio, model=model)

    # Embed in HTML
    embed_image(html_path, output_path)

    print(f"\n  Image generated: {output_path}")
    print(f"  Model: {model}")
    print(f"  Aspect ratio: {aspect_ratio}")
    print(f"  Slide updated: {slide_file}")
    print(f"  Next: run 'cstudio screenshot {args.filter}' to see it in context\n")


def cmd_projects(args: argparse.Namespace) -> None:
    """List all projects in the repo."""
    from cstudio.projects import list_projects

    projects = list_projects()

    if not projects:
        print("\n  No projects found. Use 'cstudio init' to create one.\n")
        return

    # Print table header
    print()
    print(f"  {'#':>3}  {'Name':<24} {'Type':<15} {'Theme':<17} {'Slides':>6}  {'Status'}")
    for i, p in enumerate(projects, 1):
        status = "published" if p["published"] else "draft"
        name = p["name"][:23]
        print(f"  {i:>3}  {name:<24} {p['type']:<15} {p['theme']:<17} {p['slide_count']:>6}  {status}")

    # Print paths
    print()
    for i, p in enumerate(projects, 1):
        print(f"  {i:>3}  {p['project_dir']}")

    print(f"\n  {len(projects)} projects found.\n")


def cmd_stub(args: argparse.Namespace) -> None:
    """Placeholder for future commands."""
    log.info(f"[CLI] '{args.command}' is not yet implemented. Coming soon!")
