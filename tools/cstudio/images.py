"""Image generation — parse prompts, call Gemini API, embed in slides.

Supports externalized prompt files with YAML frontmatter and inline fallback.
"""

import os
import re
from pathlib import Path

import structlog
import yaml

from cstudio.exceptions import ImageError

log = structlog.get_logger()

# ── Quality → model mapping ──────────────────────────────────────────────────

QUALITY_MODELS = {
    "standard": os.environ.get("CSTUDIO_IMAGE_MODEL_STANDARD", "gemini-2.5-flash-image"),
    "high": os.environ.get("CSTUDIO_IMAGE_MODEL_HIGH", "gemini-3-pro-image-preview"),
}

VALID_ASPECT_RATIOS = {"16:9", "9:16", "1:1", "4:3", "3:4"}
DEFAULT_ASPECT_RATIO = "16:9"


# ── Placeholder parsing ─────────────────────────────────────────────────────


def parse_placeholder(html_path: Path) -> dict:
    """Parse a slide HTML file and extract image placeholder metadata.

    Returns dict with:
        prompt_path: Path | None — resolved absolute path to the prompt file
        inline_text: str | None — fallback text from inside the placeholder
        element_html: str — the full placeholder div HTML
    """
    content = html_path.read_text()

    # Find the image-placeholder div (including data-prompt attribute if present)
    pattern = re.compile(
        r'(<div\s+class="image-placeholder"[^>]*>.*?</div>\s*</div>)',
        re.DOTALL,
    )
    match = pattern.search(content)

    if not match:
        # Try simpler pattern (single closing div)
        pattern2 = re.compile(
            r'(<div\s+class="image-placeholder"[^>]*>.*?</div>)',
            re.DOTALL,
        )
        match = pattern2.search(content)

    if not match:
        raise ImageError(f"No image placeholder found in {html_path.name}")

    element_html = match.group(1)

    # Extract data-prompt attribute
    prompt_attr = re.search(r'data-prompt="([^"]+)"', element_html)
    prompt_path = None
    if prompt_attr:
        rel_path = prompt_attr.group(1)
        prompt_path = (html_path.parent / rel_path).resolve()

    # Extract inline text (fallback)
    inline_text = None
    text_match = re.search(
        r'<div\s+class="placeholder-text">(.*?)</div>', element_html, re.DOTALL
    )
    if text_match:
        # Strip HTML tags to get plain text
        raw = text_match.group(1)
        inline_text = re.sub(r"<[^>]+>", " ", raw).strip()
        inline_text = re.sub(r"\s+", " ", inline_text)

    log.debug(
        "[IMAGE] parsed placeholder",
        slide=html_path.name,
        has_prompt_path=prompt_path is not None,
        has_inline=inline_text is not None,
    )

    return {
        "prompt_path": prompt_path,
        "inline_text": inline_text,
        "element_html": element_html,
    }


# ── Prompt file loading ─────────────────────────────────────────────────────


def load_prompt(prompt_path: Path) -> dict:
    """Parse an external prompt file with YAML frontmatter.

    Returns dict with:
        text: str — the prompt body
        aspect_ratio: str — e.g. "16:9", "9:16"
        size: str | None — e.g. "2160x3840" (informational)
    """
    if not prompt_path.is_file():
        raise ImageError(f"Prompt file not found: {prompt_path}")

    content = prompt_path.read_text()

    # Split YAML frontmatter from body
    frontmatter = {}
    body = content

    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            try:
                frontmatter = yaml.safe_load(parts[1]) or {}
            except yaml.YAMLError as e:
                log.warning("[IMAGE] invalid frontmatter", path=str(prompt_path), error=str(e))
            body = parts[2].strip()

    # Reject 'model' in frontmatter — model is configured via .env or --quality flag
    if frontmatter.get("model"):
        raise ImageError(
            f"'model' field in prompt file is no longer supported: {prompt_path.name}. "
            f"Remove it and use --quality flag or CSTUDIO_IMAGE_MODEL_STANDARD/HIGH in .env instead."
        )

    aspect_ratio = str(frontmatter.get("aspect_ratio", DEFAULT_ASPECT_RATIO))
    if aspect_ratio not in VALID_ASPECT_RATIOS:
        log.warning(
            "[IMAGE] invalid aspect_ratio, using default",
            value=aspect_ratio,
            default=DEFAULT_ASPECT_RATIO,
        )
        aspect_ratio = DEFAULT_ASPECT_RATIO

    log.debug(
        "[IMAGE] loaded prompt",
        path=prompt_path.name,
        aspect_ratio=aspect_ratio,
        prompt_length=len(body),
    )

    return {
        "text": body,
        "aspect_ratio": aspect_ratio,
        "size": frontmatter.get("size"),
    }


# ── Gemini image generation ─────────────────────────────────────────────────


def generate_image(
    prompt: str,
    output_path: Path,
    aspect_ratio: str = DEFAULT_ASPECT_RATIO,
    model: str | None = None,
) -> Path:
    """Call Gemini API to generate an image from a text prompt.

    Returns the output path on success.
    """
    from google import genai
    from google.genai import types

    from cstudio.utils import load_api_key

    model = model or QUALITY_MODELS["standard"]

    api_key = load_api_key("gemini")
    client = genai.Client(api_key=api_key)

    log.info(
        "[IMAGE] generating",
        model=model,
        aspect_ratio=aspect_ratio,
        prompt_preview=prompt[:80] + "..." if len(prompt) > 80 else prompt,
    )

    try:
        response = client.models.generate_content(
            model=model,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_modalities=["IMAGE"],
                image_config=types.ImageConfig(
                    aspectRatio=aspect_ratio,
                ),
            ),
        )
    except Exception as e:
        raise ImageError(f"Gemini API call failed: {e}") from e

    # Extract image from response
    for part in response.candidates[0].content.parts:
        if part.inline_data:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_bytes(part.inline_data.data)
            size_kb = len(part.inline_data.data) // 1024
            log.info(
                "[IMAGE] saved",
                path=str(output_path),
                size_kb=size_kb,
                mime=part.inline_data.mime_type,
            )
            return output_path

    raise ImageError("Gemini API returned no image data in the response.")


# ── HTML embedding ───────────────────────────────────────────────────────────


def embed_image(html_path: Path, image_path: Path) -> None:
    """Replace the image placeholder in a slide HTML with an <img> tag.

    Computes a relative path from the HTML file to the image file.
    Preserves surrounding wrapper divs.
    """
    content = html_path.read_text()

    # Find the placeholder div (same pattern as parse_placeholder)
    pattern = re.compile(
        r'<div\s+class="image-placeholder"[^>]*>.*?</div>\s*</div>',
        re.DOTALL,
    )
    match = pattern.search(content)

    if not match:
        pattern2 = re.compile(
            r'<div\s+class="image-placeholder"[^>]*>.*?</div>',
            re.DOTALL,
        )
        match = pattern2.search(content)

    if not match:
        raise ImageError(f"No image placeholder found in {html_path.name} to replace.")

    # Compute relative path from HTML to image
    try:
        rel_path = image_path.resolve().relative_to(html_path.parent.resolve())
    except ValueError:
        # If they don't share a common base, use os.path.relpath
        import os
        rel_path = Path(os.path.relpath(image_path.resolve(), html_path.parent.resolve()))

    # Build the img tag
    img_tag = (
        f'<img src="{rel_path}" '
        f'alt="Generated image" '
        f'style="width: 100%; height: 100%; object-fit: cover; border-radius: 12px;">'
    )

    updated = content.replace(match.group(0), img_tag)
    html_path.write_text(updated)

    log.info("[IMAGE] embedded", slide=html_path.name, image=str(rel_path))
