---
description: Capture HTML slides as retina PNG screenshots for Google Slides
user-invocable: true
allowed-tools:
  - Bash(python3 -m cstudio *)
  - Read
---

# Screenshot Skill

Captures HTML slides as 2560×1440 retina PNGs using headless Chrome.

## Usage

The user says something like "screenshot my slides", "take screenshots", or "capture slide 5".

## Dynamic Context

Current project status:

```
!python3 -m cstudio status
```

## Steps

1. If the user wants **all slides**: run `python3 -m cstudio screenshot`
2. If the user wants a **specific slide**: run `python3 -m cstudio screenshot <filter>`
   - By name: `python3 -m cstudio screenshot slide-01-title`
   - By number: `python3 -m cstudio screenshot --slide 5`
   - By partial match: `python3 -m cstudio screenshot title`
3. Report the results — number of PNGs created and where they were saved.

**IMPORTANT:** Always use `python3 -m cstudio`, never bare `python` or `cstudio`.

## Requirements

- Must be run from within a project directory (or subdirectory) that contains a `project.yaml`
- Chrome/Chromium must be installed
- Selenium must be installed (`python3 -m pip install selenium`)
