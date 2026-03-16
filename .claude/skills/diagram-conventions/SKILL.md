---
description: Auto-loaded reference for diagram editing conventions
user-invocable: false
---

# Diagram Conventions Reference

This skill provides conventions to follow when creating or editing HTML diagrams (blog diagrams, standalone images).

## Theme: clean-slate (light)

- **Heading font:** Space Grotesk (500-600 weight)
- **Body font:** DM Sans
- **Mono font:** JetBrains Mono
- **Primary:** `#0D9488` (teal), Secondary: `#0891B2` (cyan), Tertiary: `#7C3AED` (purple)
- **Background:** `#F8FAFC` off-white with subtle purple/cyan radial glows
- **Title:** 48px, purple-to-cyan gradient text, centered
- **Subtitle:** 24px, `#64748B` secondary text

## Required CSS Links (clean-slate diagrams)

Every clean-slate diagram must link these shared stylesheets:

```html
<link rel="stylesheet" href="../../../../../library/themes/clean-slate/theme-base.css">
<link rel="stylesheet" href="../../../../../library/creative-dna/diagrams/components/header.css">
<link rel="stylesheet" href="../../../../../library/creative-dna/diagrams/components/typography.css">
<link rel="stylesheet" href="../../../../../library/themes/clean-slate/typography-colors.css">
```

Adjust `../` depth based on file location relative to repo root.

## Build System (Fade-Only)

Diagram builds use fade-only animation (no translateY), defined in theme-base.css:

```html
<div class="build-item" data-build="1">First to appear</div>
<div class="build-item" data-build="2">Second to appear</div>
<script>const totalBuilds = 2; const initialBuild = 2;</script>
<script src="../../../../../library/creative-dna/core/builds.js"></script>
```

Set `initialBuild = totalBuilds` to show all builds by default (diagrams are static images, not presentations).

## Typography Classes

Standard classes from `typography.css` — use these for consistent text sizing:

| Class | Font | Size | Weight | Notes |
|---|---|---|---|---|
| `.node-title` | Space Grotesk | 18px | 600 | Dense diagrams |
| `.node-title-lg` | Space Grotesk | 22px | 600 | Medium/simple diagrams |
| `.node-desc` | DM Sans | 13px | 400 | Dense |
| `.node-desc-lg` | DM Sans | 15px | 400 | Medium/simple |
| `.node-skill` | JetBrains Mono | 12px | 500 | Monospace annotations |
| `.phase-label` | Space Grotesk | 13px | 600 | Uppercase category |
| `.phase-name` | Space Grotesk | 20px | 600 | Section name |
| `.phase-desc` | DM Sans | 13px | 400 | Italic tagline |
| `.pill` | DM Sans | 12px | 500 | Rounded tag |
| `.pill-lg` | DM Sans | 13px | 500 | Larger tag |
| `.col-label` | Space Grotesk | 15px | 600 | Uppercase column header |
| `.annotation` | DM Sans | 12px | 400 | Italic footnote |

Colors come from `typography-colors.css` (linked separately). Accent colors for icons, badges, and pills are diagram-specific — apply inline.

## Additional CSS Variables

Theme-base provides: teal, cyan, purple, green. Add others inline as needed:

```css
:root {
    --color-orange: #D97706;
    --color-orange-rgb: 217, 119, 6;
    --color-blue: #2563EB;
    --color-blue-rgb: 37, 99, 235;
}
```

## Layout Rules

- **Flow direction:** Left-to-right (primary)
- **Title:** Centered, gradient text
- **Canvas:** 1280x720px (16:9)
- **Cards:** White (`#FFFFFF`) with subtle shadows, colored left borders
- **Content padding:** 40px 50px (default), override inline for tighter layouts

## Node Color Conventions

| Role | Color | Usage |
|------|-------|-------|
| Primary | Teal `#0D9488` | Main components |
| Secondary | Cyan `#0891B2` | Supporting components |
| Tertiary | Purple `#7C3AED` | Data/knowledge |
| Success | Green `#059669` | Tools/actions |
| Warning | Orange `#D97706` | Attention items |
| Info | Blue `#2563EB` | Storage/external |

## Blog Diagram Embedding

When a diagram in a `type: blog` project is finalized (user approves the screenshot), automatically update the blog markdown:

1. Read `project.yaml` → `blog.file` to find the blog markdown
2. Find the matching `*[Image: ...]*` placeholder — match by diagram topic/title
3. Replace the placeholder with the image reference and caption (see format below)
4. The screenshot filename follows the pattern: `{diagram-name}-build-{totalBuilds}.png` (final build shows all elements)
5. Caption format: `*Diagram Title — Brief description of what the diagram shows.*`
6. Confirm the replacement to the user

**Path convention:** Blog markdown lives in `blog/`, screenshots in `diagrams/screenshots/`, so the relative path from the markdown file is `../diagrams/screenshots/`.

**When NOT to embed:** If the project is `type: image` or `type: presentation`, there is no blog file — skip this step.

## DO NOT

- Add build count badges
- Skip build numbers
- Use dark backgrounds (clean-slate is light-only)
- Use fonts outside the theme system
