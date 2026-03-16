---
description: Scaffold a new presentation, blog, or image project
user-invocable: true
allowed-tools:
  - Bash(python3 -m cstudio *)
  - Read
  - Write
---

# New Project Skill

Creates a new project with the correct directory structure and project.yaml.

## Usage

The user says something like "create a new presentation about X", "set up a new blog project for Y", or "create an image project for Z".

## Steps

1. **Determine the project type and path** from the user's request:
   - OCIA presentations: `projects/personal/ocia/YYYY-MM-{topic}/` (type: presentation)
   - Professional presentations: `projects/professional/presentations/YYYY-MM-{topic}/` (type: presentation)
   - Blog projects: `projects/professional/blogs/YYYY-MM-{slug}/` (type: blog)
   - Image projects: `projects/professional/images/YYYY-MM-{slug}/` or `projects/personal/images/YYYY-MM-{slug}/` (type: image)

2. **Determine the theme:**
   - **Blog or image** → `clean-slate` (always — no need to ask)
   - **Presentation** → ask the user which theme they want:
     - `sacred-gold` — dark background, gold accent (good for church/OCIA presentations)
     - `luminous-ivory` — light ivory background, warm gold accent (good for lighter, modern presentations)

3. **Run scaffold command:**
   ```bash
   python3 -m cstudio init <path> --theme <theme> --type <type> --name "<Display Name>"
   ```
   - **ALWAYS use `python3 -m cstudio`**, never bare `python` or `cstudio`
   - The `--name` flag sets the display name in project.yaml (e.g., `--name "Sin & Virtue"`)
   - The `--type` flag is optional — if omitted, the type is inferred from the path

4. **Customize project.yaml** if needed — edit the generated file to add:
   - Google Drive folder ID (if known, presentations only)
   - Initial slide/diagram list (if the user has one)

5. Report what was created and suggest next steps:
   - Presentation: "Create your outline, then start building slides"
   - Blog: "Add context sources, write the blog post, then create diagrams"
   - Image: "Add context sources, then create HTML diagrams"
