---
description: Extract webpage content and save it as context for the current project
user-invocable: true
allowed-tools:
  - Bash(python3 -m cstudio *)
  - Read
  - Write
  - WebFetch
---

# Add Webpage Content

Extracts the main content from a webpage and saves it as a context source for the current project.

## Usage

The user says something like "add this webpage" or "/add-webpage https://example.com/article"

## Steps

### 1. Try WebFetch first (fast, simple)

Use the WebFetch tool with the prompt:
> "Extract the main article content from this page. Return the page title on the first line, then all body text, headings, and key quotes. Exclude navigation, ads, footers, and sidebars."

If WebFetch succeeds, skip to step 3.

### 2. If WebFetch fails — use cstudio scrape (handles Cloudflare, JS-rendered pages)

Many sites use Cloudflare bot protection that blocks simple HTTP requests with a 403. The `cstudio scrape` command uses headless Chrome to bypass this:

```bash
python3 -m cstudio scrape "URL" -o context/sources/web/{slugified-title}.md
```

This command:
- Launches headless Chrome (same browser used for screenshots)
- Waits for Cloudflare JS challenges to resolve
- Extracts clean article text (strips nav, footer, ads, sidebars)
- Saves as markdown with title, source URL, and extraction date

**IMPORTANT:** Always use `python3 -m cstudio`, never bare `python` or `cstudio`.

If you don't know the title yet for the filename, use a temporary output path like `-o /tmp/webpage.md`, read the file to get the title, then move it to the correct location.

### 3. Save to context directory

If you used `cstudio scrape -o`, the file is already saved. Otherwise, use the Write tool:

- Target directory: `context/sources/web/`
- Slugify the page title for the filename (lowercase, hyphens, no special chars)
- Example: `guide-to-seven-deadly-sins.md`

Format:
```markdown
# {Page Title}
Source: {full URL}
Extracted: {date}

---

{extracted content}
```

### 4. Report results

- Page title
- File path
- Approximate word count

## Error Handling

- **WebFetch 403 / blocked:** Use `cstudio scrape` — it handles Cloudflare and most bot protection
- **Both fail:** Offer the user copy-paste as the fallback. Do NOT keep retrying.
- **Do NOT use `grep -P`** — it doesn't work on macOS. Use `sed` or python3 for text extraction.
