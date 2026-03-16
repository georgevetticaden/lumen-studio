---
description: Export Google Slides deck as PDF. Use when the user wants to export, download, or save a PDF of their deck.
user-invocable: true
allowed-tools:
  - Bash(python3 -m cstudio *)
  - Read
---

# Export Skill

Export the published Google Slides deck as PDF.

## Usage

The user says something like "export as PDF", "download the deck", or "save a PDF".

## Dynamic Context

Current project status:

```
!python3 -m cstudio status
```

## Steps

1. Run `python3 -m cstudio export`
2. If it succeeds, report:
   - The output PDF file path
   - The file size
   - Remind the user the PDF is in the `exports/` directory
3. If it fails, read the error and suggest fixes

**IMPORTANT:** Always use `python3 -m cstudio`, never bare `python` or `cstudio`.

## Error Handling

- If no `project.yaml`: suggest running `/new-project` first
- If no `presentation_id`: suggest running `/publish` first — the deck must exist before exporting
- If Google API fails: check credential directory setup — see CLAUDE.md for configuration
- If `exports/` directory doesn't exist: it will be created automatically

## Requirements

- Must be run from within a project directory that contains a `project.yaml`
- The deck must already be published (has `google.presentation_id` in `project.yaml`)
- Google OAuth credentials must be configured — see CLAUDE.md for credential directory setup
