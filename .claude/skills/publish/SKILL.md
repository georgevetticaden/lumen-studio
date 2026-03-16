---
description: Create a new Google Slides deck from all slides. Use when the user wants to publish, create a deck, or generate Google Slides.
user-invocable: true
allowed-tools:
  - Bash(python3 -m cstudio *)
  - Read
  - Edit
---

# Publish Skill

Publish slides to a new Google Slides deck.

## Usage

The user says something like "publish my slides", "create a Google Slides deck", or "push to Google Slides".

## Dynamic Context

Current project status:

```
!python3 -m cstudio status
```

## Steps

1. Run `python3 -m cstudio publish`
2. If it succeeds, report:
   - The Google Slides URL
   - How many slides were created
   - Remind the user to use `/sync N` for future updates
3. If it fails, read the error and suggest fixes

**IMPORTANT:** Always use `python3 -m cstudio`, never bare `python` or `cstudio`.

## Error Handling

- If no `project.yaml`: suggest running `/new-project` first
- If project type is not presentation: inform the user `/publish` is for presentation projects
- If already published (`presentation_id` exists): ask if they want to create a NEW deck or use `/sync` to update the existing one
- If credentials missing: see CLAUDE.md for credential directory setup (env var → `.env` → `~/.content-studio/`)

### Missing Drive Folder ID

If the error contains "No google.drive_folder_id":

1. Ask the user for their Google Drive folder URL where the deck should be stored
2. Extract the folder ID from the URL using this pattern: `/folders/([a-zA-Z0-9_-]+)`
   - Supported URL formats:
     - `https://drive.google.com/drive/folders/FOLDER_ID`
     - `https://drive.google.com/drive/u/0/folders/FOLDER_ID`
     - `https://drive.google.com/drive/folders/FOLDER_ID?...` (with query params)
3. Update `project.yaml` — set `google.drive_folder_id` to the extracted ID using the Edit tool
4. Re-run `python3 -m cstudio publish`

## Requirements

- Must be run from within a project directory that contains a `project.yaml`
- Google OAuth credentials must be configured — see CLAUDE.md for credential directory setup
- `google-auth`, `google-auth-oauthlib`, `google-api-python-client` must be installed
