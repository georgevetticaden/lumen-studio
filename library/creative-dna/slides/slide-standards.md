# Slide Standards

Standards for creating HTML slides for presentations. These slides are designed to be previewed in a browser and exported/screenshotted for use in Google Slides.

## Slide Dimensions

All slides use the Google Slides compatible canvas:
- **Width:** 1280px
- **Height:** 720px
- **Aspect Ratio:** 16:9

See `library/creative-dna/core/dimensions.md` for full dimension specifications.

## File Structure

Every slide HTML file should include:
1. HTML5 doctype and proper head section
2. Google Fonts import (theme-specific)
3. Theme base CSS (`<link>` to theme's `theme-base.css`)
4. Shared component CSS (`<link>` to relevant files in `library/creative-dna/slides/components/`)
5. Slide-specific inline CSS (layout, overrides)
6. Slide container with content
7. Build script (if using progressive reveals): global `totalBuilds` + shared `builds.js`

### Linking Shared CSS

From a slide in `projects/personal/ocia/2026-03-reconciliation/slides/`:

**sacred-gold (dark theme):**
```html
<link rel="stylesheet" href="../../../../../library/themes/sacred-gold/theme-base.css">
<link rel="stylesheet" href="../../../../../library/creative-dna/slides/components/header.css">
<link rel="stylesheet" href="../../../../../library/themes/sacred-gold/header-colors.css">
<link rel="stylesheet" href="../../../../../library/creative-dna/slides/components/typography.css">
<link rel="stylesheet" href="../../../../../library/themes/sacred-gold/typography-colors.css">
<link rel="stylesheet" href="../../../../../library/themes/sacred-gold/component-colors.css">
<link rel="stylesheet" href="../../../../../library/creative-dna/slides/components/build-system.css">
```

**luminous-ivory (light theme):**
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

### Build Script Pattern

```html
<!-- Before closing </body> -->
<script>const totalBuilds = 3;</script>
<script src="../../../../../library/creative-dna/core/builds.js"></script>
```

The shared `builds.js` reads `totalBuilds` from global scope and exports `showBuild()` to `window` for Selenium screenshot automation.

## Typography Rules

### Title Alignment
- **Content slides:** Always LEFT-ALIGNED
- **Title slide only:** Centered

### Title Styling — Content Slides (from `header.css`)

`header.css` provides structural properties (font-family, size, weight, letter-spacing). Colors come from the theme's `header-colors.css`:
- **sacred-gold:** `color: #fff` (white on dark)
- **luminous-ivory:** `color: #1E1B17` (dark brown on light)

```css
/* header.css (structural) */
.title {
    font-family: 'Cormorant Garamond', serif;
    font-size: 74px;
    font-weight: 300;
    letter-spacing: 2px;
}
```

Some slides override to smaller sizes inline (e.g., slide-11 uses 58px).

### Title Styling — Title Slide

The title slide uses two title elements:
- `.title` at **38px** (e.g., "The Sacrament of") — muted text, uppercase
- `.title-main` at **74px** (e.g., "Reconciliation") — primary text, uppercase

### Subtitle Styling (from `header.css` + `header-colors.css`)

```css
/* header.css (structural) */
.subtitle {
    font-family: 'Cormorant Garamond', serif;
    font-size: 30px;
    font-weight: 300;
    font-style: italic;
    letter-spacing: 1px;
}
/* Color from header-colors.css:
   sacred-gold:    rgba(218, 165, 32, 0.9)
   luminous-ivory: rgba(160, 115, 20, 0.9) */
```

`header.css` adds decorative open/close quotes via `::before`/`::after`. Title slides suppress these with `content: none`.

### Gold Emphasis in Titles

```html
<h1 class="title">What is <span class="title-emphasis">Reconciliation</span>?</h1>
```

`.title-emphasis` renders in the theme's gold accent color (from `header-colors.css`).

## Layout Patterns

**IMPORTANT — CSS Grid min-height rule:** All grid layouts inside slides must set `grid-template-rows: 1fr` on the container and `min-height: 0` on grid children. Without this, images with tall intrinsic heights (e.g. portrait 9:16) inflate the grid row via CSS Grid's default `min-height: auto`, breaking `flex: 1` and `justify-content: center` in adjacent columns. The shared `two-column.css` component handles this automatically.

### Two-Column Layout (Text + Image)

Prefer linking `two-column.css` which includes the protective properties:
```html
<link rel="stylesheet" href="path/to/library/creative-dna/slides/components/two-column.css">
```

If defining inline:
```css
.content {
    display: grid;
    grid-template-columns: 1fr 1fr;
    grid-template-rows: 1fr;
    gap: 50px;
    padding: 60px 70px;
}
.content > * {
    min-height: 0;
}
```

### Full-Width Content
```css
.content {
    display: flex;
    flex-direction: column;
    padding: 50px 60px;
}
```

### Card Grid
```css
.card-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 20px;
}
```

### Three-Column Grid
```css
.three-column {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    grid-template-rows: 1fr;
    gap: 30px;
}
.three-column > * {
    min-height: 0;
}
```

## Content Padding

Standard padding from canvas edges:

| Content Type | Padding |
|--------------|---------|
| Slides | `40px 50px` to `50px 60px` |
| Dense content | `30px 40px` (minimum) |

## Slide Types

### 1. Title Slide
- Centered layout (`.content` with `align-items: center; justify-content: center; text-align: center;`)
- `.title` at 38px + `.title-main` at 74px (both uppercase) — or single `.title` at 72px
- Gold accent divider (diamond + lines)
- Italic subtitle (no decorative quotes)
- No builds (all content visible)
- Top-label (project-specific, e.g., "OCIA Presentation", "Tech Talk") — uses `.top-label` class
- Bottom presenter name: default **"George Vetticaden"** — uses `.bottom-info` > `.presenter-name` (outside `.content`, absolutely positioned)
- Cross accent: **optional** — only for religious/OCIA presentations (not used in luminous-ivory)

### 2. Content Slide with Image
- Two-column grid (text left, image right)
- Left-aligned title/subtitle
- Build items in left column
- Image placeholder in right column

### 3. Card Grid Slide
- Left-aligned title/subtitle
- Grid of cards below
- Cards build in sequentially

### 4. Diagram/Visual Slide
- Left-aligned title/subtitle
- Large visual element
- Supporting text/explanation
- Multiple builds to reveal components

### 5. Quote Slide
- Left-aligned or centered title
- Large quote block with attribution
- CCC references via `.ccc-ref` and `.ccc-quote` classes

### 6. Prayer/Closing Slide
- Warmer golden background variant (different gradient)
- Centered layout
- Custom fade-only build animations (not standard slide-up)

## Build Animations

See `library/creative-dna/core/builds.md` for complete build system documentation.

Quick reference:
```html
<div class="build-item" data-build="1">First to appear</div>
<div class="build-item" data-build="2">Second to appear</div>
```

Standard animation (from `build-system.css`):
```css
.build-item {
    opacity: 0;
    transform: translateY(20px);
    transition: all 0.5s ease-out;
}
.build-item.visible {
    opacity: 1;
    transform: translateY(0);
}
```

Slides with custom animations (e.g., per-element timing, fade-only) define transitions inline and don't link `build-system.css`.

## Image Placeholders

Use placeholder divs during development. When the image is ready, `/image` replaces the placeholder with a generated `<img>` tag.

### With External Prompt File (preferred for complex images)

```html
<div class="image-placeholder" data-prompt="images/prompts/slide-03-books-collage-v1.md">
    <div class="placeholder-icon">📚</div>
    <div class="placeholder-text">
        <strong>IMAGE:</strong> Collage of popular self-help books
    </div>
</div>
```

The `data-prompt` attribute points to an external prompt file (relative to the slide HTML). **When creating a slide with `data-prompt`, always create the prompt file at the same time.** The prompt file uses YAML frontmatter for metadata (aspect_ratio, model) and a markdown body for the full prompt text. See `/image` skill for the prompt file format.

### Without External Prompt (simple one-liner images)

```html
<div class="image-placeholder">
    <div class="placeholder-icon">🕯️</div>
    <div class="placeholder-text">
        <strong>IMAGE:</strong> Warm golden candlelight in a dark church
    </div>
</div>
```

When no `data-prompt` is set, the `/image` skill extracts the inline text from `.placeholder-text` as a fallback prompt.

See `library/creative-dna/slides/components/image-placeholder.css` for styling.

## Shared Components

Reusable CSS in `library/creative-dna/slides/components/`:

| Component | File | Description |
|-----------|------|-------------|
| Header | `header.css` | .content, .title (74px), .subtitle, .cross-accent, .top-label, .bottom-info |
| Typography | `typography.css` | .card-body, .body-text, .quote-text, .quote-attribution, .ref, .gold, .card-icon |
| Build System | `build-system.css` | Standard .build-item fade + slide-up animation |
| Quote Block | `quote-block.css` | .quote-block, .ccc-quote, .ccc-ref (OCIA Catechism citations) |
| Card | `card.css` | Content card with accent bar |
| Image Placeholder | `image-placeholder.css` | Development placeholder |
| Stat Display | `stat-display.css` | Large number with label |
| Transition | `transition.css` | Section transition text |

Theme base CSS lives in `library/themes/{theme}/theme-base.css` (reset, body, .slide background, noise texture).

## Theme Architecture

Slide CSS is split into structural (theme-agnostic) and color (theme-specific) layers:

| Structural (shared) | Color (per-theme) |
|---|---|
| `header.css` — layout, sizes, weights | `header-colors.css` — title, subtitle, label colors |
| `typography.css` — text sizes, families | `typography-colors.css` — text colors |
| `quote-block.css` — quote layout | `component-colors.css` — card, quote, stat, transition colors |
| `card.css` — card layout | |
| `build-system.css` — animations | |

Available themes: `sacred-gold` (dark), `luminous-ivory` (light), `clean-slate` (diagrams only).

## What Goes Inline vs Shared

| Shared File | Provides |
|-------------|----------|
| `theme-base.css` | Reset, body centering, .slide (1280×720, gradient background, noise) |
| `variables.css` | CSS custom properties (luminous-ivory only) |
| `header.css` | .content (flex column), .title, .subtitle, .cross-accent, .top-label, .bottom-info |
| `header-colors.css` | Theme-specific colors for header elements |
| `typography.css` | Standard text classes (sizes, weights, families) — theme-agnostic |
| `typography-colors.css` | Text colors for typography classes — theme-specific |
| `component-colors.css` | Colors for card, quote-block, stat-display, transition, image-placeholder |
| `build-system.css` | Standard .build-item fade + slide-up |

| Inline (slide-specific) | Examples |
|--------------------------|---------|
| Layout overrides | Grid columns, padding, alignment |
| Size overrides | `.title { font-size: 38px; }` on title slide |
| Unique elements | Dividers, progress bars, node diagrams |
| Custom build animations | Per-element timing, fade-only variants |
| Slide-16 background | Warmer golden gradient override |

## Best Practices

### DO:
- Link shared CSS files instead of duplicating styles
- Use consistent background from theme-base.css
- Left-align title/subtitle on content slides
- Use theme accent color (gold) for emphasis
- Include detailed AI prompts in image placeholders
- Make full use of slide area
- Test keyboard navigation before finalizing
- Use semantic HTML structure

### DON'T:
- Duplicate reset/body/.slide CSS inline (use theme-base.css)
- Add build count badges/indicators to slides
- Add speaker notes on visible slide area
- Center titles on content slides (only title slide)
- Leave large empty areas without purpose
- Use different backgrounds on different slides (except slide-16 prayer variant)
- Skip build numbers (1, 2, 4... — missing 3)

## Checklist

Before finalizing a slide:
- [ ] Links theme-base.css (no duplicated reset/body/slide CSS)
- [ ] Links typography.css + theme typography-colors.css
- [ ] Links needed component CSS files
- [ ] Correct dimensions (1280×720, from theme-base.css)
- [ ] Theme background applied (from theme-base.css)
- [ ] Title/subtitle left-aligned (unless title slide)
- [ ] Typography matches theme (Cormorant Garamond titles, Montserrat body)
- [ ] Builds use `data-build` attributes + shared builds.js
- [ ] Keyboard navigation works (if builds exist)
- [ ] No build count badges
- [ ] Image placeholders include AI prompts
- [ ] Full use of slide area
- [ ] Consistent color palette (gold accent)
