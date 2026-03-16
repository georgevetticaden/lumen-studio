---
description: Auto-loaded reference for slide editing conventions
user-invocable: false
---

# Slide Conventions Reference

This skill provides conventions to follow when creating or editing HTML slides.

## Determine Theme from project.yaml

Check the project's `project.yaml` `theme` field to determine which theme to use:
- `sacred-gold` → dark background, white text, gold accent
- `luminous-ivory` → warm ivory background, dark text, gold accent

Both themes share the same fonts (Cormorant Garamond + Montserrat) and structural components. The difference is the color layer.

## Theme: sacred-gold (dark)

- **Accent color:** `rgba(218, 165, 32, 0.9)` (bright gold)
- **Background:** Dark with purple/gold radial glows + noise texture
- **Text:** White at various opacities
- **Cards:** Translucent white `rgba(255,255,255,0.03)` with subtle borders
- **Cross accent:** Gold cross element — **optional**, for religious/OCIA presentations only

### Required CSS Links (sacred-gold)

```html
<link rel="stylesheet" href="../../../../../library/themes/sacred-gold/theme-base.css">
<link rel="stylesheet" href="../../../../../library/creative-dna/slides/components/header.css">
<link rel="stylesheet" href="../../../../../library/themes/sacred-gold/header-colors.css">
<link rel="stylesheet" href="../../../../../library/creative-dna/slides/components/typography.css">
<link rel="stylesheet" href="../../../../../library/themes/sacred-gold/typography-colors.css">
<link rel="stylesheet" href="../../../../../library/themes/sacred-gold/component-colors.css">
<link rel="stylesheet" href="../../../../../library/creative-dna/slides/components/build-system.css">
```

## Theme: luminous-ivory (light)

- **Accent color:** `rgba(170, 120, 20, 0.95)` (warm gold)
- **Background:** Warm ivory (#F0EBE3 → #E8E1D7) with amber glows + noise texture
- **Text:** Dark brown `rgba(45, 42, 38)` at various opacities
- **Cards:** Pure white `#fff` with 3-layer box shadows
- **No cross accent** on title slides

### Required CSS Links (luminous-ivory)

```html
<link rel="stylesheet" href="../../../../../library/themes/luminous-ivory/theme-base.css">
<link rel="stylesheet" href="../../../../../library/themes/luminous-ivory/variables.css">
<link rel="stylesheet" href="../../../../../library/creative-dna/slides/components/header.css">
<link rel="stylesheet" href="../../../../../library/themes/luminous-ivory/header-colors.css">
<link rel="stylesheet" href="../../../../../library/creative-dna/slides/components/typography.css">
<link rel="stylesheet" href="../../../../../library/themes/luminous-ivory/typography-colors.css">
<link rel="stylesheet" href="../../../../../library/themes/luminous-ivory/component-colors.css">
<link rel="stylesheet" href="../../../../../library/creative-dna/slides/components/build-system.css">
```

### Luminous-ivory inline color reference

When writing inline CSS for luminous-ivory slides:

| Element | Color |
|---------|-------|
| Heading text | `#1E1B17` |
| Body text | `rgba(45, 42, 38, 0.78)` |
| Secondary text | `rgba(45, 42, 38, 0.65)` |
| Muted/label text | `rgba(45, 42, 38, 0.45)` |
| Subtle/ref text | `rgba(45, 42, 38, 0.35)` |
| Gold accent | `rgba(170, 120, 20, 0.95)` |
| Gold border | `rgba(170, 120, 20, 0.65)` |
| Red/negative | `rgba(180, 55, 55, 0.7)` |
| Card background | `#fff` |
| Card border | `rgba(45, 42, 38, 0.06)` |
| Card shadow | `0 1px 2px rgba(0,0,0,0.12), 0 4px 12px rgba(0,0,0,0.08), 0 16px 48px rgba(0,0,0,0.06)` |

## Shared Conventions (both themes)

### Fonts
- **Display font:** Cormorant Garamond (300–400 weight)
- **Body font:** Montserrat (400–500 weight)
- **Title size:** 74px (content slides), 38px+74px (title slide)
- **Subtitle:** 30px italic with decorative quotes

### Build System

```html
<div class="build-item" data-build="1">First to appear</div>
<div class="build-item" data-build="2">Second to appear</div>
<script>const totalBuilds = 2;</script>
<script src="../../../../../library/creative-dna/core/builds.js"></script>
```

### Image Placeholders

When adding an image placeholder to a slide, **always do both**:

1. Add the `data-prompt` attribute pointing to the prompt file
2. **Create the prompt file** at that path with YAML frontmatter and a detailed prompt

```html
<div class="image-placeholder" data-prompt="images/prompts/slide-03-books-collage-v1.md">
    <div class="placeholder-icon">📚</div>
    <div class="placeholder-text">
        <strong>IMAGE:</strong> Brief description of the image
    </div>
</div>
```

The prompt file (e.g., `slides/images/prompts/slide-03-books-collage-v1.md`):
```markdown
---
aspect_ratio: "9:16"
---

A tall portrait collage of popular self-help book covers arranged in an
overlapping stack. Include recognizable titles like Atomic Habits, The Power
of Now, 7 Habits of Highly Effective People, Think and Grow Rich. Warm
lighting, slightly worn paperback style, photorealistic.
```

- `data-prompt` path is relative to the slide HTML file
- Prompt files live in `{content_dir}/images/prompts/`
- The `data-prompt` attribute and the prompt file must be created together — never add one without the other
- The `/image` skill reads this attribute to find the prompt and generate the image
- For simple images, `data-prompt` can be omitted — the inline text is used as a fallback

### Layout Rules

- **Content slides:** Left-align titles
- **Title slides:** Center-align everything (see Title Slide Pattern below)
- **Canvas:** 1280x720px (16:9)
- **Padding:** 40-60px from edges

### CSS Grid min-height Rule

**All grid layouts inside slides** must include:
1. `grid-template-rows: 1fr` on the grid container
2. `min-height: 0` on grid children (columns)

Without these, images with tall intrinsic heights (e.g. portrait 9:16) inflate the grid row via CSS Grid's default `min-height: auto`, breaking `flex: 1` and `justify-content: center` in adjacent columns.

**For two-column layouts:** Link the shared `two-column.css` component which handles this automatically. Only define grids inline if you need a non-standard layout, and always include the protective properties.

### Title Slide Pattern

Title slides center all content vertically and horizontally. The `.bottom-info` div sits **outside** `.content` (it's absolutely positioned via `header.css`).

**Presenter name:** Default is "George Vetticaden". Use `<p class="presenter-name">George Vetticaden</p>` inside `.bottom-info`.

**Top label:** Project-specific (e.g., "OCIA Presentation", "Tech Talk"). Use `.top-label` class.

**Cross accent:** **Optional** — only include `<div class="cross-accent"></div>` for religious/OCIA presentations. Do not include for general presentations.

**Inline CSS overrides for title slide:**

```css
/* Center the flex content (header.css provides display:flex, flex-direction:column) */
.content {
    align-items: center;
    justify-content: center;
    padding: 60px 80px;
    text-align: center;
}

/* Two-part title: small lead-in + large main title */
.title {
    font-size: 38px;
    color: rgba(255, 255, 255, 0.5);  /* sacred-gold */
    letter-spacing: 3px;
    text-transform: uppercase;
    margin-bottom: 14px;
}

.title-main {
    font-family: 'Cormorant Garamond', serif;
    font-size: 74px;
    font-weight: 300;
    color: #fff;
    letter-spacing: 3px;
    text-transform: uppercase;
    line-height: 1.1;
    margin-bottom: 30px;
}

/* Or single title (no lead-in): */
.title {
    font-size: 72px;
    letter-spacing: 6px;
    text-transform: uppercase;
    margin-bottom: 30px;
}

/* Gold divider */
.divider { display: flex; align-items: center; gap: 20px; margin-bottom: 30px; }
.divider-line { width: 80px; height: 1px; background: linear-gradient(90deg, transparent, rgba(218,165,32,0.5), transparent); }
.divider-diamond { width: 8px; height: 8px; border: 1px solid rgba(218,165,32,0.5); transform: rotate(45deg); }

/* Suppress decorative quotes on subtitle */
.subtitle::before, .subtitle::after { content: none; }
```

**HTML structure:**

```html
<div class="slide">
    <!-- Optional: only for religious/OCIA presentations -->
    <div class="cross-accent"></div>

    <div class="content">
        <div class="top-label">Presentation Series Name</div>

        <!-- Option A: Two-part title -->
        <h2 class="title">The Sacrament of</h2>
        <h1 class="title-main">Reconciliation</h1>

        <!-- Option B: Single title -->
        <h1 class="title">The Beatitudes</h1>

        <div class="divider">
            <div class="divider-line"></div>
            <div class="divider-diamond"></div>
            <div class="divider-line"></div>
        </div>

        <p class="subtitle">Subtitle Goes Here</p>
    </div>

    <div class="bottom-info">
        <p class="presenter-name">George Vetticaden</p>
    </div>
</div>
```

### Typography Classes (from `typography.css`)

Standard classes available for text elements:

| Class | Font | Size | Weight | Notes |
|-------|------|------|--------|-------|
| `.card-body` | Montserrat | 17px | 400 | Card descriptions |
| `.card-desc` | Montserrat | 15px | 400 | Smaller card text |
| `.body-text` | Montserrat | 18px | 400 | General body text |
| `.quote-text` | Cormorant | 24px | 400 italic | Quote blocks |
| `.quote-text-sm` | Cormorant | 18px | 400 italic | Compact quotes |
| `.quote-attribution` | Montserrat | 13px | 400 | Quote sources (uppercase) |
| `.ref` | Montserrat | 12px | 400 | CCC/scripture refs (uppercase) |
| `.card-def-label` | Montserrat | 13px | 500 | Section labels (uppercase) |
| `.card-icon` | — | 38px | — | Large emoji icons |
| `.card-icon-sm` | — | 26px | — | Small emoji icons |
| `.gold` | — | — | 500 | Gold emphasis text |
| `.quote-mark` | Cormorant | 48px | 300 | Decorative open-quote |

Colors come from `typography-colors.css` (theme-specific). Only override inline when the slide needs different values.

## DO NOT

- Add build count badges
- Skip build numbers
- Use different backgrounds on different slides
- Use fonts outside the theme system
- Mix sacred-gold colors in luminous-ivory slides (or vice versa)
