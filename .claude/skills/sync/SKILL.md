---
description: Update slides in Google Slides. Use when the user wants to sync, update, or push slide changes to Google Slides.
argument-hint: "[slide-number]"
user-invocable: true
allowed-tools:
  - Bash(python3 -m cstudio *)
  - Read
---

# Sync Skill

Sync slides to an existing Google Slides deck.

## Usage

The user says something like "sync slide 5", "update Google Slides", "push my changes", or "sync all slides".

## Dynamic Context

Current project status:

```
!python3 -m cstudio status
```

## Steps

If $ARGUMENTS is provided, sync that specific slide:
1. Run `python3 -m cstudio sync --slide $ARGUMENTS`
2. If it succeeds, report the updated slide number and Google Slides URL
3. If it fails, read the error and suggest fixes

If no arguments, sync all slides:
1. Run `python3 -m cstudio sync`
2. Report how many slides were updated and the Google Slides URL

**IMPORTANT:** Always use `python3 -m cstudio`, never bare `python` or `cstudio`.

## Error Handling

- If no `project.yaml` found: tell the user to cd into a project directory
- If no `presentation_id`: suggest running `/publish` first
- If screenshot fails: check if the HTML file exists and has valid syntax
- If Google API fails: check credential directory setup — see CLAUDE.md for configuration

## Requirements

- Must be run from within a project directory that contains a `project.yaml`
- The deck must already be published (has `google.presentation_id` in `project.yaml`)
- Google OAuth credentials must be configured — see CLAUDE.md for credential directory setup
