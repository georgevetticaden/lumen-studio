# File Naming Conventions

Consistent file naming ensures organization and easy navigation across all projects.

## General Rules

1. **Use kebab-case** - lowercase with hyphens: `my-file-name.html`
2. **Be descriptive** - Name should indicate content
3. **No spaces** - Use hyphens instead
4. **No special characters** - Letters, numbers, hyphens only

## Project Folders

Format: `YYYY-MM-{descriptive-slug}/`

Examples:
- `2026-01-mindset-agent-launch/`
- `2026-02-reconciliation-talk/`
- `2025-12-beatitudes/`

The date prefix ensures chronological sorting and easy identification.

## Slides

Format: `slide-{NN}-{short-name}.html`

| Component | Description |
|-----------|-------------|
| `slide-` | Prefix (required) |
| `{NN}` | Two-digit number (00-99) |
| `{short-name}` | Brief descriptive name |

Examples:
```
slide-00-background.html      # Background-only for Google Slides
slide-01-title.html           # Title slide
slide-02-agenda.html          # Agenda/overview
slide-03-problem-statement.html
slide-04-solution-overview.html
slide-05-architecture.html
slide-06-demo.html
slide-07-conclusion.html
```

### Special Slides
- `slide-00-background.html` - Always the standalone background
- Version suffixes: `slide-05-architecture-v2.html` (for iterations)

## Diagrams

Format: `{descriptive-name}.html`

Use clear, descriptive names that indicate what the diagram shows:

Examples:
```
architecture-overview.html
streaming-context-flow.html
oauth-handshake-sequence.html
system-components.html
data-pipeline.html
agent-knowledge-layers.html
```

## Images

Format: `{descriptive-name}.{ext}`

For generated/exported images:
```
architecture-overview.png
flow-diagram.png
screenshot-demo-01.png
```

## Video Assets

### Scripts
Format: `script-{section}.md` or `script.md` (if single script)

```
script.md                     # Main script
script-intro.md               # Section-specific
script-demo.md
script-conclusion.md
```

### Assets
Format: `{descriptive-name}.{ext}`

```
intro-animation.mp4
demo-recording.mp4
background-music.mp3
```

## Archive Files

When archiving old versions, move them to an `archive/` subfolder within the appropriate directory.

### Blog Diagrams

For blog projects, store all diagram files in `images/`:

```
professional/blogs/YYYY-MM-{project}/
├── {blog-post}.md                # Blog content
└── images/
    ├── {diagram-name}.html       # Final diagram HTML
    ├── {diagram-name}.png        # Exported PNG
    └── archive/
        ├── {diagram-name}-v1.html
        ├── {diagram-name}-v2.html
        └── {diagram-name}-v3.html
```

**Workflow:**
1. Keep working versions with `-v1`, `-v2` suffixes during iteration
2. Once finalized, rename to clean name (no version suffix)
3. Move all previous versions to `images/archive/`
4. Export final diagram as PNG to `images/`

### Slides and Presentations

For slides, use an `archive/` subfolder at project level:

```
professional/presentations/YYYY-MM-{project}/
├── slide-01-title.html
├── slide-02-agenda.html
└── archive/
    └── slide-02-agenda-v1.html
```

Optionally add date: `slide-05-v1-archived-2026-01-15.html`

## Version Suffixes

When iterating on files, use version suffixes:

```
slide-05-architecture.html      # Current version
slide-05-architecture-v1.html   # Previous version (in archive/)
slide-05-architecture-v2.html   # Alternative version
```

Or use descriptive suffixes:
```
slide-05-architecture.html
slide-05-architecture-detailed.html
slide-05-architecture-simplified.html
```

## Summary Table

| Content Type | Format | Example |
|--------------|--------|---------|
| Project folder | `YYYY-MM-{slug}/` | `2026-01-mindset-agent/` |
| Slide | `slide-{NN}-{name}.html` | `slide-03-overview.html` |
| Diagram | `{descriptive-name}.html` | `data-flow.html` |
| Image | `{descriptive-name}.{ext}` | `architecture.png` |
| Script | `script.md` or `script-{section}.md` | `script-demo.md` |
