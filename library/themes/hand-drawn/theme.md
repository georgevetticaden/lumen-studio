# Hand Drawn Theme

Sketch-style theme for diagrams that use a handwriting aesthetic — whiteboard feel, ink-on-paper look, Caveat font. Used when content benefits from an informal, visual-thinking quality rather than a polished technical finish.

## Usage

This theme is used for:
- Workflow and process diagrams with a "working sketch" feel
- Diagrams embedded in blog posts that feel personal and informal
- Phase/stage diagrams (research → creation, iteration loops)
- Architecture sketches that feel like a whiteboard explanation

## Source of Truth

**`theme-base.css`** is the source of truth for the base theme CSS (variables, reset, body, .diagram container, build animations, and reusable sketch components). All values below are extracted from the actual sketch diagrams and documented here for reference.

## Design Philosophy

Hand-drawn, informal, personal. The design evokes:
- Whiteboard sketches and working notes
- A thinking-out-loud quality — these are ideas being worked through, not polished deliverables
- Personal warmth over corporate polish
- Slightly imperfect intentionally — slight rotations on cards create the sketch feel

**Key rules:**
- Pure white background — no gradients, no radial glows
- All borders use actual black ink (`#1a1a1a`) — thick enough to read as drawn
- Slight CSS `transform: rotate()` on cards gives the sketch feel (±0.3deg to ±0.7deg)
- Amber (`#D97706`) is the only accent color — used for skill commands and amber arrows
- SVGs draw all connecting arrows (hand-drawn style via `stroke-linecap: round`)

## Colors

### Ink Colors

| Name | CSS Variable | Value | Usage |
|------|-------------|-------|-------|
| Ink | `--color-ink` | `#1a1a1a` | Primary text, card borders, SVG strokes |
| Ink Medium | `--color-ink-medium` | `#333` | Dashed borders, strong secondary |
| Ink Light | `--color-ink-light` | `#555` | Subtitles, muted labels, dashed borders |
| Ink Muted | `--color-ink-muted` | `#888` | Section labels, captions |

### Accent Colors

| Name | CSS Variable | Value | Usage |
|------|-------------|-------|-------|
| Amber | `--color-amber` | `#D97706` | Amber arrows, highlights |
| Amber Dark | `--color-amber-dark` | `#92400E` | Skill pill text |

### Background Colors

| Name | CSS Variable | Value | Usage |
|------|-------------|-------|-------|
| Base | `--bg-base` | `#FFFFFF` | Diagram background |
| Card | `--bg-card` | `#FFFFFF` | Standard card backgrounds |
| Card Tinted | `--bg-card-tinted` | `#FAFAFA` | Deliverable cards, subtle tint |
| Phase Box | `--bg-phase-box` | `#FEFDF8` | Dashed phase containers |
| Gold Card | `--bg-gold-card` | `#FFFDF0` | Gold Context input card |

### Text Colors

| Name | CSS Variable | Value | Usage |
|------|-------------|-------|-------|
| Primary | `--text-primary` | `#1a1a1a` | Headings, titles, card content |
| Secondary | `--text-secondary` | `#555` | Subtitles, descriptions |
| Muted | `--text-muted` | `#888` | Labels, section headers |

## Typography

### Font Import

```html
<link href="https://fonts.googleapis.com/css2?family=Caveat:wght@400;500;600;700&display=swap" rel="stylesheet">
```

### Font Usage

| Element | CSS Variable | Font | Notes |
|---------|-------------|------|-------|
| All text | `--font-sketch` | Caveat | Single font family — the entire sketch feel comes from this |

### Typical Sizes

| Element | Size | Weight | Notes |
|---------|------|--------|-------|
| Diagram title | 46px | 700 | `#1a1a1a` |
| Diagram subtitle | 26px | 400 | `#555`, italic |
| Step/card title | 28-32px | 700 | `#1a1a1a` |
| Step description | 18-20px | 700 | `#555` |
| Section label | 14px | 700 | `#888`, uppercase, tracked |
| Skill pill text | 18px | 700 | `#92400E` (amber dark) |
| Tag pill text | 16px | 700 | `#444` |
| Phase box label | 24px | 700 | `#555` |

## Background

### Diagram Container

Pure white — no radial gradients, no border, no border-radius:

```css
.diagram {
    width: 960px;
    background: #FFFFFF;
    padding: 32px 44px 48px;
}
```

Note: height is variable per diagram. Set via `data-height` attribute for cstudio screenshot capture.

## Card Styling

Cards use solid black borders to create the hand-drawn ink effect:

| Element | Property | Value |
|---------|----------|-------|
| Card background | `background` | `#FFFFFF` |
| Card border | `border` | `2.5px solid #1a1a1a` |
| Card border-radius | `border-radius` | `6px` |
| Sketch rotation | `transform` | `rotate(±0.3deg to ±0.7deg)` |

### Rotation Pattern (alternating cards in a row)

```css
.step-card:nth-child(1) { transform: rotate(0.6deg); }
.step-card:nth-child(3) { transform: rotate(-0.5deg); }
.step-card:nth-child(5) { transform: rotate(0.4deg); }
.step-card:nth-child(7) { transform: rotate(-0.7deg); }
```

## Dashed Container Styling

Used for phase/loop boxes and group outlines:

```css
.sketch-box {
    border: 3px dashed #333;
    border-radius: 12px;
    background: #FEFDF8;
}

.sketch-box-label {
    position: absolute;
    top: -18px;
    left: 50%;
    transform: translateX(-50%);
    background: #FEFDF8;
    padding: 0 12px;
    font-size: 24px;
    font-weight: 700;
    color: #555;
}
```

## SVG Arrow Styling

All connecting arrows are drawn with inline SVG using hand-drawn quadratic curves:

```css
.scribble {
    stroke: #1a1a1a;
    stroke-width: 3;
    fill: none;
    stroke-linecap: round;
}
```

Amber arrows (for "delivered as" or secondary flows):

```html
<path d="M30 4 Q32 20 30 30" stroke="#D97706" stroke-width="3.5" fill="none" stroke-linecap="round"/>
```

## Pill / Badge Styling

### Skill Command Pill (amber accent)

```css
.skill-pill {
    font-size: 18px;
    font-weight: 700;
    color: #92400E;
    background: rgba(217, 119, 6, 0.18);
    border: 1.5px solid rgba(217, 119, 6, 0.5);
    border-radius: 6px;
    padding: 3px 10px;
}
```

### Generic Tag Pill

```css
.sketch-pill {
    font-size: 16px;
    font-weight: 700;
    border-radius: 20px;
    padding: 3px 10px;
    background: rgba(0, 0, 0, 0.06);
    color: #444;
    border: 1.5px solid #ccc;
}
```

## Build Animations

Diagrams use **fade-only** animations (no translateY slide-up):

```css
.build-item {
    opacity: 0;
    transition: opacity 0.5s ease-out;
}

.build-item.visible {
    opacity: 1;
}
```

## When to Use

- **Informal, personal diagrams:** Workflow explanations, phase/stage breakdowns
- **Blog posts:** Where you want content to feel like a working sketch, not a polished infographic
- **Whiteboard-style explanations:** Content that benefits from a "thinking out loud" visual quality

**Don't use for:** Polished professional diagrams (use clean-slate), presentations (use sacred-gold or luminous-ivory).

## Diagram Dimensions

Unlike clean-slate (fixed 1280×720), sketch diagrams use **variable height**:
- Width: always `960px`
- Height: set via `data-height` attribute on `.diagram` for cstudio screenshot capture
- cstudio reads `data-width` / `data-height` and sets the viewport accordingly

## Files

| File | Purpose |
|------|---------|
| `theme-base.css` | **Source of truth**: CSS variables, reset, body, .diagram container, build animations, reusable sketch components |
| `typography-colors.css` | Theme-specific text colors for typography classes (pairs with `typography.css`) |
| `theme.md` | This documentation |

## Shared Component Files

These live in `library/creative-dna/diagrams/components/`:

| File | What it provides |
|------|-----------------|
| `typography.css` | Structural font sizes/weights (theme-agnostic) |

Note: `header.css`, `nodes.css`, `connectors.css`, `layers.css` are **not used** by this theme.
Sketch diagrams build all layout and components inline — the hand-drawn aesthetic requires
full CSS control that the shared component classes don't provide.

Build system JS: `library/creative-dna/core/builds.js`
