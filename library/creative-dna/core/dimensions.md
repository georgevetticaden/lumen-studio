# Dimensions & Canvas Standards

All slides, diagrams, and visual content follow these dimension standards.

## Standard Canvas Size

**Google Slides Compatible:** `1280px x 720px` (16:9 aspect ratio)

```css
.slide {
    width: 1280px;
    height: 720px;
    position: relative;
    overflow: hidden;
}
```

## Body Centering

Center the canvas in the viewport for browser preview:

```css
body {
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    background: #0a0a0a;
}
```

## Viewport Rules

1. **Full visibility** - All content must be visible at 100% zoom without scrolling
2. **No overflow** - Content must not extend beyond the 1280x720 canvas
3. **Readable at scale** - Text must remain legible when exported/screenshotted

## Content Padding

Standard padding from canvas edges:

| Content Type | Padding |
|--------------|---------|
| Slides | `40px 50px` to `50px 60px` |
| Diagrams | `40px 50px` |
| Dense content | `30px 40px` (minimum) |

```css
.content {
    position: relative;
    z-index: 1;
    height: 100%;
    padding: 40px 50px;
}
```

## Custom Dimensions (Per-Slide Override)

Individual slides and diagrams can override the default canvas by adding
`data-width` and `data-height` attributes to the `.slide` or `.diagram` container:

```html
<div class="diagram" data-width="1080" data-height="1350">
```

The `cstudio screenshot` tool detects these attributes and resizes the browser
viewport automatically. Other slides in the same project keep their own dimensions.

Also set matching CSS:
```css
.diagram { width: 1080px; height: 1350px; }
```

## Dimension Presets

| Name | Dimensions | Aspect | Use Case |
|------|------------|--------|----------|
| Default | 1280×720 | 16:9 | Slides, standard diagrams, Google Slides |
| Tall | 1280×960 | 4:3 | Dense diagrams, blog images |
| Portrait | 1080×1350 | 4:5 | Medium/blog optimized (larger text) |
| Square | 1080×1080 | 1:1 | Social media graphics |
| Wide | 1280×540 | 21:9 | Banners |
