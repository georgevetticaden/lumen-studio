# Luminous Ivory Presentation Theme

Light companion to sacred-gold. Same elegant personality — warm gold accents, Cormorant Garamond + Montserrat — inverted for light backgrounds.

## Usage

This theme is used for:
- OCIA catechesis presentations (light variant)
- Parish talks and lectures
- Scripture study materials
- Spiritual formation content

## Source of Truth

**`theme-base.css`** is the source of truth for the base theme CSS (reset, body, .slide background, noise texture). All values below are extracted from the actual iterated slides and documented here for reference.

## Design Philosophy

Warm, professional, reverent. The design evokes:
- Sacred tradition with modern clarity
- Warmth and hospitality
- Paper-like texture and depth
- Pure white cards on warm linen (Apple/Linear aesthetic)

## Colors

### Primary Palette

| Name | Value | Usage |
|------|-------|-------|
| Gold | `rgba(170, 120, 20, 0.95)` | Primary accent, emphasis |
| Gold Light | `rgba(170, 120, 20, 0.65)` | Borders, subtle accents |
| Gold Dim | `rgba(170, 120, 20, 0.35)` | Dividers, faint accents |
| Gold Subtle | `rgba(170, 120, 20, 0.06)` | Background tints |
| Title Emphasis | `rgba(170, 120, 20, 0.95)` | Gold text within titles |

### Semantic Accents

| Name | Value | Usage |
|------|-------|-------|
| Positive | `#3d8c5f` | Growth, virtue, green accents |
| Caution | `#8c5f3d` | Warning, attention |
| Negative | `rgba(180, 55, 55, 0.8)` | Sin, danger, insight bar accent |
| Spiritual | `#8c3d6d` | Mystery, spiritual depth |
| Wisdom | `#3d5f8c` | Knowledge, truth |

### Background Colors

| Name | Value | Usage |
|------|-------|-------|
| Warm Ivory | `#F0EBE3` | Slide gradient start |
| Warm Linen | `#E8E1D7` | Slide gradient end |
| Body | `#C8C1B4` | Page background behind slide |
| Card | `#ffffff` | Card backgrounds (pure white) |

### Text Colors

| Name | Value | Usage |
|------|-------|-------|
| Primary | `#1E1B17` | Headings, titles |
| Body | `rgba(45, 42, 38, 0.78)` | Body text, quotes |
| Secondary | `rgba(45, 42, 38, 0.65)` | Descriptions, card body |
| Muted | `rgba(45, 42, 38, 0.45)` | Attributions, labels |
| Subtle | `rgba(45, 42, 38, 0.35)` | References, faint labels |

## Typography

### Font Imports

```html
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;1,300;1,400&family=Montserrat:wght@300;400;500;600&display=swap" rel="stylesheet">
```

### Font Usage

| Element | Font | Weight | Size | Notes |
|---------|------|--------|------|-------|
| Content title | Cormorant Garamond | 300 | 74px | Default in header.css |
| Title (title slide) | Cormorant Garamond | 300 | 72px | Uppercase, letter-spacing 6px |
| Subtitle | Cormorant Garamond | 300 italic | 30px | Gold accent color |
| Quotes | Cormorant Garamond | 300 italic | 22-26px | Dark brown at 0.78 |
| Body text | Montserrat | 400 | 15-16px | Dark brown at 0.78 |
| Labels | Montserrat | 500 | 11-13px | Uppercase, letter-spacing |
| CCC references | Montserrat | 400 | 10-11px | Uppercase, gold dim |
| Presenter name | Montserrat | 400 | 12px | Uppercase, brown 0.3 |

## Background

### Standard Gradient

```css
background:
    radial-gradient(ellipse at 30% 30%, rgba(218, 175, 85, 0.06) 0%, transparent 50%),
    radial-gradient(ellipse at 70% 70%, rgba(180, 140, 60, 0.05) 0%, transparent 50%),
    radial-gradient(ellipse at 50% 50%, rgba(218, 165, 32, 0.03) 0%, transparent 40%),
    linear-gradient(180deg, #F0EBE3 0%, #E8E1D7 100%);
```

### Noise Texture

SVG fractal noise at 1.8% opacity, applied via `.slide::before`. Defined in `theme-base.css`. Lighter than sacred-gold (3%) for a subtle paper-like quality.

## Card Styling

Cards use **pure white backgrounds** with 3-layer crisp shadows on the warm linen base:

```css
.card {
    background: #fff;
    border: 1px solid rgba(45, 42, 38, 0.06);
    border-radius: 12px;
    box-shadow:
        0 1px 2px rgba(0, 0, 0, 0.12),
        0 4px 12px rgba(0, 0, 0, 0.08),
        0 16px 48px rgba(0, 0, 0, 0.06);
}
```

### Key Differences from Sacred-Gold Cards

| Property | Sacred-Gold (dark) | Luminous-Ivory (light) |
|----------|-------------------|----------------------|
| Background | `rgba(255, 255, 255, 0.03)` | `#fff` |
| Border | `rgba(255, 255, 255, 0.08)` | `rgba(45, 42, 38, 0.06)` |
| Depth | Subtle, ethereal | Crisp, elevated |
| Shadow | None | 3-layer pattern |
| Accent bar | Gold at 70% | Gold at 65% |

## Files

| File | Purpose |
|------|---------|
| `theme-base.css` | **Source of truth**: reset, body, .slide background, noise texture |
| `variables.css` | CSS custom properties (colors, text, spacing, shadows) |
| `header-colors.css` | Text colors for header elements (pairs with `header.css`) |
| `typography-colors.css` | Text colors for typography classes (pairs with `typography.css`) |
| `component-colors.css` | Colors for card, quote-block, stat-display, transition, image-placeholder |
| `background.html` | Standalone background for Google Slides |
| `slide-template.html` | Theme-ready content slide template |
| `title-slide-template.html` | Centered title slide template |
| `theme.md` | This documentation |

## Shared Component Files

These live in `library/creative-dna/slides/components/`:

| File | What it provides |
|------|-----------------|
| `header.css` | .content, .title (74px), .subtitle (with quotes), .top-label, .bottom-info |
| `typography.css` | .card-body, .body-text, .quote-text, .quote-attribution, .ref, .gold (sizes/weights) |
| `build-system.css` | .build-item fade + slide-up animation |
| `quote-block.css` | .quote-block layout, .ccc-quote, .ccc-ref |
| `card.css` | .card layout, .card-accent, .card-hover |
| `stat-display.css` | .stat-number, .stat-label layout |
| `transition.css` | .transition-statement layout |
| `image-placeholder.css` | .image-placeholder layout |

Build system JS: `library/creative-dna/core/builds.js`

## Typography Architecture

Typography is split into two files:
- **`library/creative-dna/slides/components/typography.css`** — Theme-agnostic structural properties (font-family, font-size, font-weight, line-height, letter-spacing, text-transform). Shared across all themes.
- **`library/themes/luminous-ivory/typography-colors.css`** — Theme-specific text colors (dark browns at various opacities, gold accents). Each theme provides its own version.

This separation means adding a new theme only requires writing color files (`header-colors.css`, `typography-colors.css`, `component-colors.css`) with appropriate colors for that theme's background.

## CSS Link Order

```html
<!-- Theme base -->
<link rel="stylesheet" href="...themes/luminous-ivory/theme-base.css">
<link rel="stylesheet" href="...themes/luminous-ivory/variables.css">
<!-- Standard components (structural) -->
<link rel="stylesheet" href="...standards/slides/components/header.css">
<link rel="stylesheet" href="...themes/luminous-ivory/header-colors.css">
<link rel="stylesheet" href="...standards/slides/components/typography.css">
<link rel="stylesheet" href="...themes/luminous-ivory/typography-colors.css">
<link rel="stylesheet" href="...themes/luminous-ivory/component-colors.css">
<!-- Build system -->
<link rel="stylesheet" href="...standards/slides/components/build-system.css">
```
