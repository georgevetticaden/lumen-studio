---
description: Generate an image for a slide from its prompt file. Use when the user wants to generate, create, or iterate on an image for a slide or diagram.
user-invocable: true
allowed-tools:
  - Bash(python3 -m cstudio *)
  - Read
  - Write
  - Edit
---

# /image — Per-Slide Image Generation & Iteration

Generates images for slides using Gemini API, then iterates based on user feedback.

## Usage

The user says something like "generate the image for slide 3", "let's work on the image", or invokes `/image slide-03`.

## Dynamic Context

Current project status:

```
!python3 -m cstudio status
```

## The Iteration Loop

### First Generation

1. **Identify the slide** from the user's request (by number, name, or current context)
2. **Check for a prompt file:**
   - Read the slide HTML and look for `data-prompt` attribute on `.image-placeholder`
   - If a prompt file exists at that path → read it
   - If no prompt file exists → draft one from the placeholder inline text and slide context,
     save it to `{content_dir}/images/prompts/{slide-name}-{description}-v1.md` with YAML frontmatter:
     ```markdown
     ---
     aspect_ratio: "16:9"
     ---

     [Detailed prompt text]
     ```
   - Add a `data-prompt` attribute to the placeholder div pointing to the new prompt file
3. **Generate the image:**
   ```bash
   python3 -m cstudio image <slide-filter>
   ```
4. **Screenshot the slide** so the user can see the result in context:
   ```bash
   python3 -m cstudio screenshot <slide-filter>
   ```
5. **Show the screenshot** to the user and ask for feedback

### Iteration (user gives feedback)

**Content/style feedback** ("too dark", "books too neat", "add more books", "make it warmer"):
1. Read the current prompt file
2. Create a new version with the feedback applied (v1 → v2, v2 → v3, etc.)
3. Update the `data-prompt` attribute in the slide HTML to point to the new version
4. Regenerate: `python3 -m cstudio image <slide-filter>`
5. Re-screenshot: `python3 -m cstudio screenshot <slide-filter>`
6. Show the updated screenshot

**Layout/sizing feedback** ("shift left", "make smaller", "add padding"):
1. Edit the slide CSS/HTML to adjust positioning — no regeneration needed
2. Re-screenshot: `python3 -m cstudio screenshot <slide-filter>`
3. Show the result

### Done

When the user confirms the image ("looks good", "perfect", "let's move on"), the loop ends. The prompt file stays in `images/prompts/` as a record of what produced the final image.

## Prompt File Format

```markdown
---
aspect_ratio: "16:9"
---

[Full detailed prompt text here — be specific about style, composition, lighting, mood, etc.]
```

Frontmatter fields:
- `aspect_ratio` (required): "16:9", "9:16", "1:1", "4:3", or "3:4"
- `size` (optional): informational, e.g. "2560x1440"

**Do NOT put `model` in prompt files.** Model is controlled via `--quality standard|high` flag, with defaults configured in `.env` (`CSTUDIO_IMAGE_MODEL_STANDARD`, `CSTUDIO_IMAGE_MODEL_HIGH`). The CLI will error if `model` is found in frontmatter.

## Quality Tiers

- `--quality standard` (default): `gemini-2.5-flash-image` — fast, good for iteration
- `--quality high`: `gemini-3-pro-image-preview` — slower, higher quality for final images

Suggest starting with standard quality for iteration, then regenerating with `--quality high` once the prompt is finalized.

## Error Handling

- If no `project.yaml` found: suggest running `/new-project` first
- If no image placeholder in the slide: inform the user the slide has no `.image-placeholder` div
- If Gemini API fails: check that `gemini.key` exists in the credential directory (see CLAUDE.md)
- If quality is poor after iteration: suggest `--quality high` for a better model
- If the prompt file doesn't exist but `data-prompt` is set: offer to create it

**IMPORTANT:** Always use `python3 -m cstudio`, never bare `python` or `cstudio`.
