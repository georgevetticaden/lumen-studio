# Clean Slate Theme

Light theme for blog diagrams, standalone images, and professional content on white/light backgrounds.

## Usage

This theme is used for:
- Blog post diagrams (architecture, flow, concept visuals)
- Standalone images (README diagrams, social media graphics, documentation)
- Professional content for Medium, WordPress, documentation sites
- Any context requiring a light background

## Source of Truth

**`theme-base.css`** is the source of truth for the base theme CSS (variables, reset, body, .diagram container, build animations). All values below are extracted from the actual blog diagrams and documented here for reference.

## Design Philosophy

Clean, modern, professional. The design evokes:
- Technical clarity
- Contemporary SaaS aesthetics
- Approachable yet authoritative
- Subtle depth through gradient glows

## Colors

### Primary Palette

| Name | CSS Variable | Value | Usage |
|------|-------------|-------|-------|
| Teal | `--color-teal` | `#0D9488` | Primary nodes, main components |
| Teal RGB | `--color-teal-rgb` | `13, 148, 136` | For rgba() backgrounds/borders |
| Cyan | `--color-cyan` | `#0891B2` | Secondary nodes, supporting components |
| Cyan RGB | `--color-cyan-rgb` | `8, 145, 178` | For rgba() backgrounds/borders |
| Purple | `--color-purple` | `#7C3AED` | Tertiary nodes, advanced/optional |
| Purple RGB | `--color-purple-rgb` | `124, 58, 237` | For rgba() backgrounds/borders |
| Green | `--color-green` | `#059669` | Success states, positive indicators |
| Green RGB | `--color-green-rgb` | `5, 150, 105` | For rgba() backgrounds/borders |

### Background Colors

| Name | CSS Variable | Value | Usage |
|------|-------------|-------|-------|
| Base | `--bg-base` | `#F8FAFC` | Diagram background |
| Card | `--bg-card` | `#FFFFFF` | Card/node backgrounds |
| Body | — | `#E2E8F0` | Page background behind diagram |

### Text Colors

| Name | CSS Variable | Value | Usage |
|------|-------------|-------|-------|
| Primary | `--text-primary` | `#1E293B` | Headings, titles |
| Secondary | `--text-secondary` | `#64748B` | Body text, descriptions |
| Muted | `--text-muted` | `#94A3B8` | Labels, captions |

### Title Gradient

| Name | CSS Variable | Value | Usage |
|------|-------------|-------|-------|
| Gradient Purple | `--gradient-purple` | `#8B5CF6` | Title gradient start |
| Gradient Cyan | `--gradient-cyan` | `#06B6D4` | Title gradient end |

## Typography

### Font Import

```html
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=DM+Sans:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
```

### Font Usage

| Element | CSS Variable | Font | Usage |
|---------|-------------|------|-------|
| Headings | `--font-heading` | Space Grotesk | Titles, node labels |
| Body | `--font-body` | DM Sans | Descriptions, body text |
| Code | `--font-mono` | JetBrains Mono | Code snippets, technical labels |

### Typical Sizes

| Element | Size | Weight | Notes |
|---------|------|--------|-------|
| Diagram title | 28-32px | 600 | Purple→cyan gradient text |
| Diagram subtitle | 16-18px | 400 | Muted gray (`--text-secondary`) |
| Node title | 14-16px | 500 | Primary text color |
| Node description | 12-13px | 400 | Secondary text color |
| Badge/pill text | 11-12px | 500 | Accent color (NOT white) |

## Background

### Diagram Container

```css
.diagram {
    width: 1280px;
    height: 720px;
    background:
        radial-gradient(ellipse at 20% 30%, rgba(139, 92, 246, 0.06) 0%, transparent 50%),
        radial-gradient(ellipse at 80% 70%, rgba(6, 182, 212, 0.06) 0%, transparent 50%),
        #F8FAFC;
    border: 1px solid rgba(148, 163, 184, 0.3);
    border-radius: 8px;
}
```

The subtle purple and cyan glows at 6% opacity add depth without being visible at a glance. The border gives definition when embedded in white-background contexts.

## Card Styling

Cards and nodes use subtle colored backgrounds to stand out against the off-white canvas.

| Element | Property | Value |
|---------|----------|-------|
| Card background | `background` | `rgba(var(--color-teal-rgb), 0.05)` |
| Card border | `border` | `1px solid rgba(var(--color-teal-rgb), 0.4)` |
| Card shadow | `box-shadow` | `0 1px 3px rgba(0,0,0,0.08)` |
| Accent border | `border-top` | `3px solid var(--color-teal)` |
| Icon background | `background` | `rgba(var(--color-teal-rgb), 0.2)` |

**Key rule:** Card backgrounds must NOT be transparent — they blend into the base gradient. Use at least `0.05` opacity.

## Badge Styling

Badges and pills use **colored text on colored background** — NOT white text.

```css
/* CORRECT */
background: rgba(var(--color-cyan-rgb), 0.12);
color: var(--color-cyan);

/* WRONG — don't use white text on colored badge */
background: rgba(var(--color-cyan-rgb), 0.12);
color: #fff;
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

This differs from slides, which use fade + slide-up.

## When to Use

- **Light background contexts:** Medium, WordPress, documentation sites, README files
- **Embedded in blog posts:** Diagrams sit naturally alongside text
- **Professional content:** Technical architecture, data flows, concept illustrations
- **Standalone images:** Social media graphics, GitHub repo visuals

**Don't use for:** Dark background contexts (use a dark theme instead), church/spiritual content (use sacred-gold).

## Typography Architecture

Typography is split into two files:
- **`library/creative-dna/diagrams/components/typography.css`** — Theme-agnostic structural properties
  (font-family, font-size, font-weight, line-height, letter-spacing, text-transform).
  Shared across all themes.
- **`library/themes/clean-slate/typography-colors.css`** — Theme-specific text colors.
  Each theme provides its own version.

This separation means adding a new diagram theme only requires writing a new
`typography-colors.css` with appropriate text colors for that theme's background.

## Files

| File | Purpose |
|------|---------|
| `theme-base.css` | **Source of truth**: CSS variables, reset, body, .diagram container, build animations |
| `typography-colors.css` | Theme-specific text colors for typography classes (pairs with `typography.css`) |
| `theme.md` | This documentation |

## Shared Component Files

These live in `library/creative-dna/diagrams/components/`:

| File | What it provides |
|------|-----------------|
| `header.css` | Gradient title, subtitle, content wrapper |
| `typography.css` | Structural font sizes/weights for node-title, node-desc, phase-label, pill, etc. |
| `nodes.css` | Node styles (primary, secondary, tertiary) |
| `connectors.css` | Arrows and connection lines |
| `layers.css` | Layered architecture diagrams |

Build system JS: `library/creative-dna/core/builds.js`

Diagram template: `library/creative-dna/diagrams/diagram-template.html`
