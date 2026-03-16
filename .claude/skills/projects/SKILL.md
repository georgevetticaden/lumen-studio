---
description: List all projects and switch to one. Use when the user wants to see their projects, switch projects, or resume work.
user-invocable: true
allowed-tools:
  - Bash(python3 -m cstudio *)
  - Bash(cd *)
  - Read
---

# /projects — Project Selection & Session Resume

## When to Use
- User invokes `/projects`
- User asks "what projects do I have?" or "switch to..." or "resume..."
- Start of a new session when the user wants to pick a project

## Steps

1. **List all projects** by running:
   ```bash
   python3 -m cstudio projects
   ```

2. **Ask the user** which project they want to work on (by number or name).

3. **Switch to the selected project** by running:
   ```bash
   cd <project_dir>
   ```
   Use the absolute path shown in the `cstudio projects` output.

4. **Show project status** to confirm the switch:
   ```bash
   python3 -m cstudio status
   ```

5. **Ask the user** what they'd like to work on in this project.
