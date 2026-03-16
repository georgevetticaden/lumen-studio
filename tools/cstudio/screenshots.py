"""Screenshot engine — capture HTML slides/diagrams as retina PNGs.

Ported from generate-slides.py with identical Selenium logic:
- CDP viewport at 1280×720 (default), customizable per-slide via data-width/data-height
- 2x device scale factor for retina PNGs
- Element-level screenshot of .slide or .diagram container
- Build cycling via showBuild() JS function
- DPI metadata via sips for Google Slides sizing
"""

import os
import re
import subprocess
import time
from pathlib import Path

import structlog

from cstudio.config import ProjectConfig
from cstudio.exceptions import BrowserError, ScreenshotError

log = structlog.get_logger()


# ── Browser setup ─────────────────────────────────────────────────────────────


def setup_browser(width: int = 1280, height: int = 720):
    """Create a headless Chrome browser at 2x scale.

    Args:
        width: Viewport width in CSS pixels (default 1280).
        height: Viewport height in CSS pixels (default 720).

    Returns a Selenium WebDriver instance configured via CDP for
    pixel-perfect retina screenshots.
    """
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options

    log.info("[BROWSER] launching headless Chrome")

    opts = Options()
    opts.add_argument("--headless=new")
    opts.add_argument("--hide-scrollbars")
    opts.add_argument("--disable-gpu")
    opts.add_argument("--no-sandbox")

    try:
        driver = webdriver.Chrome(options=opts)
    except Exception as e:
        raise BrowserError(f"Failed to launch Chrome: {e}") from e

    # CDP viewport at 2x for retina
    driver.execute_cdp_cmd(
        "Emulation.setDeviceMetricsOverride",
        {
            "width": width,
            "height": height,
            "deviceScaleFactor": 2,
            "mobile": False,
        },
    )

    log.info("[BROWSER] ready", viewport=f"{width}×{height}", scale="2x")
    return driver


def resize_browser(driver, width: int, height: int):
    """Resize an existing browser viewport via CDP.

    Used when switching between slides that have different dimensions.
    """
    driver.execute_cdp_cmd(
        "Emulation.setDeviceMetricsOverride",
        {
            "width": width,
            "height": height,
            "deviceScaleFactor": 2,
            "mobile": False,
        },
    )
    log.debug("[BROWSER] resized", viewport=f"{width}×{height}")


# ── Dimension detection ──────────────────────────────────────────────────────

# Default viewport dimensions
DEFAULT_WIDTH = 1280
DEFAULT_HEIGHT = 720


def get_custom_dimensions(html_path: Path) -> tuple[int, int] | None:
    """Parse HTML for custom canvas dimensions.

    Looks for data-width and data-height attributes on .diagram or .slide elements.
    Example: <div class="diagram" data-width="1080" data-height="1350">

    Returns (width, height) tuple if found, or None for default dimensions.
    """
    content = html_path.read_text()

    # Look for data-width="N" and data-height="N" on .diagram or .slide
    width_match = re.search(r'data-width="(\d+)"', content)
    height_match = re.search(r'data-height="(\d+)"', content)

    if width_match and height_match:
        w, h = int(width_match.group(1)), int(height_match.group(1))
        log.debug("[SCREENSHOT] custom dimensions", width=w, height=h, file=html_path.name)
        return (w, h)

    return None


# ── Build detection ───────────────────────────────────────────────────────────


def get_total_builds(html_path: Path) -> int:
    """Parse HTML to find totalBuilds value.

    First checks for `const totalBuilds = N;` in script tags.
    Falls back to max data-build attribute value.
    Returns 0 for static slides (no builds).
    """
    content = html_path.read_text()

    match = re.search(r"totalBuilds\s*=\s*(\d+)", content)
    if match:
        return int(match.group(1))

    # Fallback: find max data-build attribute
    builds = re.findall(r'data-build="(\d+)"', content)
    if builds:
        return max(int(b) for b in builds)

    return 0


# ── Static content detection ─────────────────────────────────────────────────


_STATIC_CHECK_JS = """
if (typeof showBuild === 'function') showBuild(0);
var statics = document.querySelectorAll(
    '.title, .subtitle, .header, .top-label, .cross-accent, '
    + '.bottom-info, .journey-map, .ccc-ref, .image-placeholder'
);
var found = false;
for (var i = 0; i < statics.length; i++) {
    var el = statics[i];
    if (el && !el.closest('[data-build]') && el.offsetHeight > 0) {
        found = true; break;
    }
}
return found;
"""


def has_static_content(driver) -> bool:
    """Check if build-0 has visible static content worth capturing."""
    return driver.execute_script(_STATIC_CHECK_JS)


# ── DPI metadata ──────────────────────────────────────────────────────────────


def set_png_dpi(path: Path, dpi: int = 256) -> None:
    """Set PNG DPI metadata so Google Slides sizes correctly.

    2560px / 256 DPI = 10"  (slide width)
    1440px / 256 DPI = 5.625"  (slide height)
    """
    subprocess.run(
        ["sips", "-s", "dpiWidth", str(dpi), "-s", "dpiHeight", str(dpi), str(path)],
        capture_output=True,
    )


# ── Single slide capture ─────────────────────────────────────────────────────


def capture_slide(
    driver, html_path: Path, output_dir: Path, current_dims: tuple[int, int] = (DEFAULT_WIDTH, DEFAULT_HEIGHT)
) -> tuple[list[Path], tuple[int, int]]:
    """Capture all build states of a single slide as PNGs.

    Args:
        driver: Selenium WebDriver instance.
        html_path: Path to the HTML file.
        output_dir: Directory for output PNGs.
        current_dims: Current browser viewport (width, height) to avoid unnecessary resizes.

    Returns tuple of (list of screenshot paths, final viewport dimensions).
    """
    from selenium.webdriver.common.by import By

    slide_name = html_path.stem
    total_builds = get_total_builds(html_path)

    # Check for custom dimensions on this slide
    custom = get_custom_dimensions(html_path)
    target_dims = custom or (DEFAULT_WIDTH, DEFAULT_HEIGHT)

    # Resize browser if needed
    if target_dims != current_dims:
        resize_browser(driver, target_dims[0], target_dims[1])
        current_dims = target_dims

    driver.get(f"file://{html_path}")
    time.sleep(1.0)  # Let fonts and CSS load

    # Try .slide first (presentations), then .diagram (blog/image diagrams)
    try:
        slide_el = driver.find_element(By.CSS_SELECTOR, ".slide")
    except Exception:
        slide_el = driver.find_element(By.CSS_SELECTOR, ".diagram")
    screenshots = []

    if total_builds == 0:
        # Static slide — single screenshot
        path = output_dir / f"{slide_name}-full.png"
        slide_el.screenshot(str(path))
        set_png_dpi(path)
        screenshots.append(path)
        log.info("[SCREENSHOT] static slide", slide=slide_name, files=1)
    else:
        # Determine start build
        start = 0 if has_static_content(driver) else 1

        for b in range(start, total_builds + 1):
            driver.execute_script(
                f'if (typeof showBuild === "function") showBuild({b});'
            )
            time.sleep(0.4)

            path = output_dir / f"{slide_name}-build-{b}.png"
            slide_el.screenshot(str(path))
            set_png_dpi(path)
            screenshots.append(path)

        log.info(
            "[SCREENSHOT] build slide",
            slide=slide_name,
            builds=total_builds,
            files=len(screenshots),
            range=f"{start}–{total_builds}",
        )

    return screenshots, current_dims


# ── Main entry point ──────────────────────────────────────────────────────────


def screenshot_slides(
    config: ProjectConfig, slide_filter: str | None = None
) -> list[Path]:
    """Screenshot all (or filtered) slides from a project.

    Args:
        config: Loaded project configuration.
        slide_filter: Optional filter — a slide filename, stem, or number.
                      Examples: "slide-01-title.html", "slide-01-title", "1", "01"

    Returns:
        List of all screenshot paths created.
    """
    content_dir = config.content_dir
    screenshots_dir = config.screenshots_dir

    if not content_dir.is_dir():
        raise ScreenshotError(f"Content directory not found: {content_dir}")

    screenshots_dir.mkdir(parents=True, exist_ok=True)

    # Determine which slides to process
    if slide_filter:
        slide_files = _resolve_slide_filter(config.slides, slide_filter)
    else:
        slide_files = config.slides

    if not slide_files:
        raise ScreenshotError("No slides to process.")

    log.info(
        "[SCREENSHOT] starting",
        slides=len(slide_files),
        output=str(screenshots_dir),
    )

    # Browser lifecycle — start with default dimensions
    driver = setup_browser(DEFAULT_WIDTH, DEFAULT_HEIGHT)
    current_dims = (DEFAULT_WIDTH, DEFAULT_HEIGHT)
    all_screenshots: list[Path] = []

    try:
        for slide_file in slide_files:
            html_path = (content_dir / slide_file).resolve()
            if not html_path.is_file():
                log.warning("[SCREENSHOT] slide not found, skipping", file=slide_file)
                continue

            shots, current_dims = capture_slide(driver, html_path, screenshots_dir, current_dims)
            all_screenshots.extend(shots)
    finally:
        driver.quit()
        log.info("[BROWSER] closed")

    # Report final resolution (last slide's dimensions at 2x)
    final_w, final_h = current_dims[0] * 2, current_dims[1] * 2
    log.info(
        "[SCREENSHOT] complete",
        total_pngs=len(all_screenshots),
        resolution=f"{final_w}×{final_h}",
    )

    return all_screenshots


# ── Slide filter resolution ───────────────────────────────────────────────────


def _resolve_slide_filter(
    all_slides: list[str], filter_str: str
) -> list[str]:
    """Resolve a filter string to a list of matching slide filenames.

    Accepts:
        - Full filename: "slide-01-title.html"
        - Stem: "slide-01-title"
        - Slide number: "1", "01"
        - Partial match: "title", "big-three"
    """
    # Normalize
    f = filter_str.strip()

    # Try exact match (with or without .html)
    for slide in all_slides:
        if slide == f or slide == f"{f}.html" or os.path.splitext(slide)[0] == f:
            return [slide]

    # Try numeric match (slide number)
    if f.isdigit():
        num = int(f)
        padded = f"{num:02d}"
        for slide in all_slides:
            if f"-{padded}-" in slide:
                return [slide]

    # Try substring match
    matches = [s for s in all_slides if f in s]
    if matches:
        return matches

    log.warning("[SCREENSHOT] no slides matched filter", filter=filter_str)
    return []
