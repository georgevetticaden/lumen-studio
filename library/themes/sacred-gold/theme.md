# OCIA Presentation Theme

Theme for personal church presentations (OCIA, Beatitudes, Reconciliation, etc.).

## Usage

This theme is used for:
- OCIA catechesis presentations
- Parish talks and lectures
- Scripture study materials
- Spiritual formation content

## Source of Truth

**`theme-base.css`** is the source of truth for the base theme CSS (reset, body, .slide, noise texture). All values below are extracted from the actual reconciliation slides and documented here for reference.

## Design Philosophy

Elegant, reverent, contemplative. The design evokes:
- Sacred tradition
- Timeless wisdom
- Warmth and hospitality
- Contemplative atmosphere

## Colors

### Primary Palette

| Name | Value | Usage |
|------|-------|-------|
| Gold | `rgba(218, 165, 32, 0.9)` | Primary accent, emphasis |
| Gold Light | `rgba(218, 165, 32, 0.6)` | Borders, subtle accents |
| Gold Dim | `rgba(218, 165, 32, 0.3)` | Backgrounds, dividers |
| Title Emphasis | `rgba(218, 165, 32, 0.95)` | Gold text within titles |

### Background Colors

| Name | Value | Usage |
|------|-------|-------|
| Dark Base | `#0d0d12` | Primary gradient start |
| Dark Alt | `#0a0a0f` | Primary gradient end |
| Body | `#0a0a0a` | Page background behind slide |
| Card | `rgba(255, 255, 255, 0.03)` | Card backgrounds |

### Text Colors

| Name | Value | Usage |
|------|-------|-------|
| Primary | `#fff` | Headings |
| Secondary | `rgba(255, 255, 255, 0.7)` | Body text |
| Muted | `rgba(255, 255, 255, 0.5)` | Labels, descriptions |
| Dim | `rgba(255, 255, 255, 0.3)` | Presenter name, faint labels |

## Typography

### Font Imports

```html
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;1,300;1,400&family=Montserrat:wght@300;400;500;600&display=swap" rel="stylesheet">
```

### Font Usage (Actual Values)

| Element | Font | Weight | Size | Notes |
|---------|------|--------|------|-------|
| Content title | Cormorant Garamond | 300 | 74px | Default in header.css |
| Title-main (title slide) | Cormorant Garamond | 300 | 74px | Uppercase, letter-spacing 3px |
| Title (title slide "The Sacrament of") | Cormorant Garamond | 300 | 38px | Override, uppercase, muted white |
| Subtitle | Cormorant Garamond | 300 italic | 30px | Gold, with decorative quotes |
| Quotes | Cormorant Garamond | 300 italic | 22-26px | White 0.85 opacity |
| Body text | Montserrat | 400 | 15-16px | |
| Labels | Montserrat | 500 | 11-13px | Uppercase, letter-spacing |
| CCC references | Montserrat | 400 | 10-11px | Uppercase, gold dim |
| Presenter name | Montserrat | 400 | 12px | Uppercase, white 0.3 |

## Background

### Standard Gradient (15 of 16 slides)

```css
background:
    radial-gradient(ellipse at 25% 25%, rgba(50, 40, 65, 0.35) 0%, transparent 50%),
    radial-gradient(ellipse at 75% 75%, rgba(65, 45, 25, 0.3) 0%, transparent 50%),
    radial-gradient(ellipse at 50% 50%, rgba(218, 165, 32, 0.03) 0%, transparent 40%),
    linear-gradient(180deg, #0d0d12 0%, #0a0a0f 100%);
```

### Prayer Slide Variant (Slide 16 — warmer golden)

```css
background:
    radial-gradient(ellipse at 50% 40%, rgba(80, 60, 15, 0.35) 0%, transparent 55%),
    radial-gradient(ellipse at 50% 80%, rgba(218, 165, 32, 0.08) 0%, transparent 40%),
    radial-gradient(ellipse at 30% 20%, rgba(50, 35, 20, 0.3) 0%, transparent 45%),
    radial-gradient(ellipse at 70% 20%, rgba(50, 35, 20, 0.3) 0%, transparent 45%),
    linear-gradient(180deg, #0a0a0e 0%, #08080c 100%);
```

### Noise Texture

SVG fractal noise at 3% opacity, applied via `.slide::before`. Defined in `theme-base.css`.

## Files

| File | Purpose |
|------|---------|
| `theme-base.css` | **Source of truth**: reset, body, .slide background, noise texture |
| `header-colors.css` | Theme-specific colors for header elements (pairs with `header.css`) |
| `typography-colors.css` | Text colors for standard typography classes (pairs with `typography.css`) |
| `component-colors.css` | Colors for card, quote-block, stat-display, transition, image-placeholder |
| `variables.css` | CSS custom properties |
| `background.html` | Standalone background for Google Slides |
| `slide-template.html` | Theme-ready slide template |
| `title-slide-template.html` | Centered title slide template |
| `theme.md` | This documentation |

## Shared Component Files

These live in `library/creative-dna/slides/components/`:

| File | What it provides |
|------|-----------------|
| `header.css` | .content, .title (74px), .subtitle (with quotes), .cross-accent, .top-label, .bottom-info |
| `typography.css` | .card-body, .body-text, .quote-text, .quote-attribution, .ref, .gold, .card-icon (sizes/weights) |
| `build-system.css` | .build-item fade + slide-up animation |
| `quote-block.css` | .quote-block layout, .ccc-quote, .ccc-ref |
| `card.css` | .card layout, .card-accent, .card-hover |
| `stat-display.css` | .stat-number, .stat-label layout |
| `transition.css` | .transition-statement layout |
| `image-placeholder.css` | .image-placeholder layout |

Build system JS: `library/creative-dna/core/builds.js`

## Typography Architecture

Slide CSS is split into structural (theme-agnostic) and color (theme-specific) layers:
- **Structural files** (`library/creative-dna/slides/components/`) define sizes, weights, spacing, layout. Shared across all themes.
- **Color files** (`library/themes/sacred-gold/`) define colors, backgrounds, borders, shadows. Theme-specific.

Color files for this theme:
- `header-colors.css` — title (#fff), subtitle (gold), cross-accent, top-label, presenter-name
- `typography-colors.css` — text colors (white at various opacities, gold accents)
- `component-colors.css` — card (translucent white), quote-block (gold gradient), stat, transition colors

This separation means adding a new theme only requires writing color files with appropriate values for that theme's background. See `luminous-ivory` for the light-background companion theme.
