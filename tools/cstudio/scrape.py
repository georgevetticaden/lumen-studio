"""Web scraping engine — extract article content from URLs using headless Chrome.

Uses Selenium to bypass Cloudflare and other JS-based bot protection that
blocks simple HTTP requests (curl, requests, WebFetch).
"""

import re
import time

import structlog

log = structlog.get_logger()

# JavaScript to clean DOM and extract article content
_EXTRACT_JS = """
// Remove non-content elements
const removeSelectors = [
    'nav', 'footer', 'header', '.sidebar', '.ad', '.advertisement',
    '.cookie-banner', '.popup', '.modal', '.social-share', '.related-posts',
    '[role="navigation"]', '[role="banner"]', '[role="complementary"]',
    'script', 'style', 'noscript', 'iframe'
];
removeSelectors.forEach(sel => {
    document.querySelectorAll(sel).forEach(el => el.remove());
});

// Strip "ADVERTISEMENT" lines from text
const stripAds = text => text.replace(/^\\s*ADVERTISEMENT.*$/gm, '').replace(/\\n{3,}/g, '\\n\\n');

// Try to find main article content (most specific first)
const candidates = [
    'article .entry-content', 'article .post-content', 'article',
    '.post-content', '.entry-content', '.article-content', '.article-body',
    'main [role="main"]', 'main', '[role="main"]'
];

for (const sel of candidates) {
    const el = document.querySelector(sel);
    if (el && el.innerText.trim().length > 200) {
        return stripAds(el.innerText.trim());
    }
}

// Fallback: full body text
return stripAds(document.body.innerText.trim());
"""


def scrape_url(url: str, wait_seconds: int = 5) -> dict:
    """Scrape a URL using headless Chrome and return extracted content.

    Args:
        url: The URL to scrape.
        wait_seconds: Seconds to wait for page load / Cloudflare challenge.

    Returns:
        dict with keys: title, content, url, word_count
    """
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options

    log.info("[SCRAPE] fetching URL", url=url)

    opts = Options()
    opts.add_argument("--headless=new")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-gpu")
    opts.add_argument("--window-size=1280,720")
    opts.add_argument(
        "--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )

    driver = webdriver.Chrome(options=opts)
    try:
        driver.get(url)
        time.sleep(wait_seconds)

        title = driver.title or "Unknown"
        # Clean trailing " - Site Name" from title
        title = re.sub(r"\s*[-|–]\s*[^-|–]+$", "", title).strip() or title

        content = driver.execute_script(_EXTRACT_JS)
        word_count = len(content.split())

        log.info(
            "[SCRAPE] extracted content",
            title=title,
            word_count=word_count,
        )

        return {
            "title": title,
            "content": content,
            "url": url,
            "word_count": word_count,
        }
    finally:
        driver.quit()


def slugify(text: str, max_length: int = 60) -> str:
    """Convert text to a URL-friendly slug for filenames."""
    slug = text.lower()
    slug = re.sub(r"[^a-z0-9\s-]", "", slug)
    slug = re.sub(r"[\s_]+", "-", slug)
    slug = re.sub(r"-+", "-", slug).strip("-")
    if len(slug) > max_length:
        slug = slug[:max_length].rsplit("-", 1)[0]
    return slug or "page"
