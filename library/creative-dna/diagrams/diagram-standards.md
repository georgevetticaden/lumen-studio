# Diagram Standards

Standards for creating HTML diagrams for blogs, documentation, and presentations.

## Overview

Diagrams are standalone HTML files that visualize:
- Architecture (system components, data flow)
- Processes (workflows, sequences)
- Concepts (relationships, hierarchies)
- Comparisons (before/after, options)

## Title Alignment

**Diagrams:** Title and subtitle are **CENTERED**

This differs from slides, where content slide titles are left-aligned.

```css
.header {
    text-align: center;
    margin-bottom: 30px;
}
```

## Diagram Title Typography

| Element | Font | Size | Weight |
|---------|------|------|--------|
| Title | Space Grotesk | **48px** | 600 |
| Subtitle | DM Sans | **20px** | 400 |

```css
.title {
    font-family: var(--font-heading);
    font-size: 48px;
    font-weight: 600;
    letter-spacing: -0.5px;
    margin-bottom: 10px;
}

.subtitle {
    font-size: 20px;
    color: rgba(255, 255, 255, 0.6);
}
```

## Hero Title Gradient (Agentic Mindset Theme)

For diagram titles, use the brand gradient text effect:

```css
:root {
    --gradient-purple: #A78BFA;
    --gradient-cyan: #22D3EE;
}

.title {
    background: linear-gradient(90deg, var(--gradient-purple) 0%, var(--gradient-cyan) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
```

The gradient flows from light purple (`#A78BFA`) to cyan (`#22D3EE`) at 90deg (left to right), matching the agenticmindset.ai styling.

**Note:** This gradient is for diagrams only. Slide titles use solid white text.

## Canvas Dimensions

**Default canvas:** `1280px × 720px` (16:9, Google Slides compatible)

Diagrams can override the default dimensions for blog/Medium readability by adding
`data-width` and `data-height` attributes to the `.diagram` container:

```html
<div class="diagram" data-width="1080" data-height="1350">
```

The `cstudio screenshot` tool automatically detects these attributes and resizes
the browser viewport per-slide. No project-level config changes needed — other
slides/diagrams in the same project keep their own dimensions.

**CSS override:** Also set matching width/height in the `.diagram` rule:

```css
.diagram {
    width: 1080px;
    height: 1350px;
}
```

### Standard Dimension Presets

| Name | Dimensions | Aspect | Use Case |
|------|------------|--------|----------|
| Default | 1280×720 | 16:9 | Slides, standard diagrams |
| Wide | 1280×540 | 21:9 | Banners, wide diagrams |
| Tall | 1280×960 | 4:3 | Dense diagrams, blog images |
| Portrait | 1080×1350 | 4:5 | Medium/blog optimized (larger text at column width) |
| Square | 1080×1080 | 1:1 | Social media graphics |

## Diagram Flow Direction

**Primary Direction:** LEFT-TO-RIGHT

This follows natural reading order and is standard for:
- Architecture diagrams
- Data flow diagrams
- Process diagrams
- Sequence diagrams

Exceptions:
- Hierarchies: TOP-TO-BOTTOM
- Cycles: CLOCKWISE rotation

## Layout Patterns

### Left-to-Right Flow
```css
.diagram-flow {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 30px;
}

.flow-arrow {
    font-size: 24px;
    color: var(--accent-color);
    opacity: 0.7;
}
```

### Three-Stage Flow
```html
<div class="diagram-flow">
    <div class="stage">Input</div>
    <div class="flow-arrow">→</div>
    <div class="stage">Process</div>
    <div class="flow-arrow">→</div>
    <div class="stage">Output</div>
</div>
```

### Grid Layout (Components)
```css
.component-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 25px;
}
```

### Layered Architecture
```css
.layer-stack {
    display: flex;
    flex-direction: column;
    gap: 15px;
}

.layer {
    padding: 20px;
    border-radius: 8px;
    text-align: center;
}
```

## Visual Elements

### Boxes/Nodes (Cards)

Cards need subtle colored backgrounds to stand out against the gradient background. Pure transparent backgrounds blend in and become hard to read.

```css
/* Base card styling */
.node {
    background: rgba(var(--color-teal-rgb), 0.05);  /* Subtle colored background */
    border: 1px solid rgba(var(--color-teal-rgb), 0.4);  /* Visible colored border */
    border-radius: 16px;
    padding: 20px 25px;
}

.node-title {
    font-family: var(--font-heading);
    font-size: 18px;
    font-weight: 500;  /* Not 600 - better readability */
    color: #fff;  /* Pure white for titles */
    margin-bottom: 6px;
}

.node-description {
    font-size: 13px;
    color: rgba(255, 255, 255, 0.6);  /* Secondary text color */
    line-height: 1.5;
}
```

**Card Background Opacity Guide:**
| Element | Opacity | Example |
|---------|---------|---------|
| Card background | `0.05` | `rgba(color, 0.05)` |
| Card border | `0.4` | `rgba(color, 0.4)` |
| Icon background | `0.2` | `rgba(color, 0.2)` |

**Why colored backgrounds?** The hero gradient background has purple and cyan glows. Pure transparent cards (`rgba(255,255,255, 0.03)`) blend into these areas and become hard to distinguish. Subtle colored backgrounds provide necessary contrast.

### Icon Containers
```css
.node-icon {
    width: 42px;
    height: 42px;
    border-radius: 10px;
    background: rgba(var(--color-teal-rgb), 0.2);  /* Slightly more visible */
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 20px;
}
```

### Arrows/Connectors
For simple arrows, use Unicode or CSS:
```css
.arrow-right::after {
    content: '→';
    font-size: 24px;
    color: var(--accent-color);
}

/* Or SVG for complex paths */
.connector {
    stroke: var(--accent-color);
    stroke-width: 2;
    fill: none;
}
```

### Labels
```css
.label {
    font-size: 12px;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: rgba(255, 255, 255, 0.5);
}
```

### Badges/Pills (Column Headers, Category Labels)

Badges use colored text on a darker colored background - NOT white text.

```css
.badge {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    font-family: var(--font-heading);
    font-size: 12px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    padding: 5px 14px;
    border-radius: 20px;
    /* Key: colored background with COLORED text */
    background: rgba(var(--color-cyan-rgb), 0.2);
    color: var(--color-cyan);  /* NOT white - use the accent color */
}
```

**Badge Color Variants:**
```css
.badge-purple { background: rgba(var(--color-purple-rgb), 0.2); color: var(--color-purple); }
.badge-cyan { background: rgba(var(--color-cyan-rgb), 0.2); color: var(--color-cyan); }
.badge-teal { background: rgba(var(--color-teal-rgb), 0.2); color: var(--color-teal); }
.badge-green { background: rgba(var(--color-green-rgb), 0.2); color: var(--color-green); }
.badge-blue { background: rgba(var(--color-blue-rgb), 0.2); color: var(--color-blue); }
.badge-orange { background: rgba(var(--color-orange-rgb), 0.2); color: var(--color-orange); }
```

## Component Types

### 1. Architecture Box
```html
<div class="arch-box">
    <div class="arch-icon">🔧</div>
    <div class="arch-title">Component Name</div>
    <div class="arch-tech">Technology</div>
</div>
```

### 2. Data Flow Node
```html
<div class="flow-node">
    <div class="node-label">Data Source</div>
    <div class="node-content">Database</div>
</div>
```

### 3. Process Step
```html
<div class="process-step">
    <div class="step-number">1</div>
    <div class="step-content">
        <div class="step-title">Step Name</div>
        <div class="step-desc">Description</div>
    </div>
</div>
```

### 4. Connection Line
```html
<svg class="connector-svg">
    <line x1="0" y1="50%" x2="100%" y2="50%"
          stroke="var(--accent-color)"
          stroke-width="2"
          stroke-dasharray="5,5"/>
</svg>
```

## Build Animations

Diagrams support builds like slides. Common patterns:

### Sequential Reveal
```html
<div class="node" data-build="1">First component</div>
<div class="arrow" data-build="2">→</div>
<div class="node" data-build="3">Second component</div>
```

### Group Reveal
```html
<!-- All core components appear together -->
<div class="node" data-build="1">Component A</div>
<div class="node" data-build="1">Component B</div>
<div class="node" data-build="1">Component C</div>
<!-- Then connections -->
<div class="connections" data-build="2">...</div>
```

### Layer Reveal
```html
<div class="layer" data-build="1">Foundation Layer</div>
<div class="layer" data-build="2">Service Layer</div>
<div class="layer" data-build="3">Application Layer</div>
```

## Color Coding

Use consistent colors for component types:

| Component Type | Color Variable | Default Value |
|----------------|----------------|---------------|
| Primary/Core | `--color-primary` | Teal (#14B8A6) |
| Secondary | `--color-secondary` | Cyan (#06B6D4) |
| Tertiary | `--color-tertiary` | Purple (#8B5CF6) |
| Data/Storage | `--color-data` | Blue (#3B82F6) |
| External | `--color-external` | Gray (#6B7280) |
| User/Client | `--color-user` | Green (#10B981) |
| Warning/Alert | `--color-warning` | Orange (#F59E0B) |

## Typography in Diagrams

Font sizes for diagram content are defined in the shared typography standard.
See `library/creative-dna/diagrams/components/typography.css` for the complete class list.

Link both the structural and color files in each diagram:

```html
<link rel="stylesheet" href="...diagrams/components/typography.css">
<link rel="stylesheet" href="...themes/clean-slate/typography-colors.css">
```

| Element | Class | Size | Weight |
|---------|-------|------|--------|
| Node titles | `.node-title` | 18px | 600 |
| Node titles (large) | `.node-title-lg` | 22px | 600 |
| Node descriptions | `.node-desc` | 13px | 400 |
| Node descriptions (large) | `.node-desc-lg` | 15px | 400 |
| Badge/pill text | `.pill` | 12px | 500 |
| Phase labels | `.phase-label` | 13px | 600 |
| Phase names | `.phase-name` | 20px | 600 |
| Annotations | `.annotation` | 12px | 400 italic |

## Best Practices

### DO:
- Flow left-to-right (or top-to-bottom for hierarchies)
- Use consistent spacing between elements
- Color-code related components
- Include legends for complex diagrams
- Use builds to explain step-by-step
- Keep text concise (diagram, not documentation)

### DON'T:
- Overcrowd the diagram
- Use too many different colors
- Make arrows cross unnecessarily
- Mix flow directions
- Use tiny fonts (<11px)
- Add excessive detail (save for documentation)

## File Naming

Format: `{descriptive-name}.html`

For light theme variants, append `-light`:
```
architecture-overview.html        # Dark theme
architecture-overview-light.html  # Light theme
```

Examples:
```
architecture-overview.html
data-flow-pipeline.html
agent-interaction-sequence.html
oauth-handshake.html
system-layers.html
```

---

## Light Theme Variant

Use the light theme for diagrams published on white/light backgrounds (Medium, documentation sites, etc.).

### When to Use Light Theme

| Context | Theme |
|---------|-------|
| agenticmindset.ai (dark site) | Dark |
| Medium blog posts | **Light** |
| Documentation with light bg | **Light** |
| Presentations (dark slides) | Dark |
| White-background embeds | **Light** |

### Light Theme Template

Use `diagram-template.html` from `library/creative-dna/diagrams/` as your starting point.

### Light Theme Background

```css
.diagram {
    background: #F8FAFC;
    /* Subtle gradient - 6% opacity (not 15% like dark) */
    background:
        radial-gradient(ellipse at 20% 30%, rgba(139, 92, 246, 0.06) 0%, transparent 50%),
        radial-gradient(ellipse at 70% 70%, rgba(6, 182, 212, 0.06) 0%, transparent 45%),
        #F8FAFC;
    /* Border for definition against white backgrounds */
    border: 1px solid rgba(148, 163, 184, 0.3);
    border-radius: 8px;
}
```

### Light Theme Text Colors

| Element | Color | Value |
|---------|-------|-------|
| Titles | Primary | `#1E293B` |
| Descriptions | Secondary | `#64748B` |
| Labels/hints | Muted | `#94A3B8` |
| Subtitle | Secondary | `#64748B` |

```css
.subtitle {
    font-size: 20px;
    color: #64748B;  /* NOT rgba white */
}
```

### Light Theme Cards

Cards use **white backgrounds with shadows** instead of colored transparent backgrounds:

```css
.node {
    background: #FFFFFF;
    border-radius: 16px;
    padding: 20px 25px;
    /* Shadow replaces colored border */
    box-shadow:
        0 1px 3px rgba(0, 0, 0, 0.1),
        0 4px 16px rgba(0, 0, 0, 0.08);
    /* Colored accent border */
    border-top: 3px solid var(--color-teal);
}

.node-title {
    color: #1E293B;  /* Dark text */
}

.node-description {
    color: #64748B;
}
```

### Light Theme Accent Borders

Use colored accent borders to maintain color-coding:

```css
/* Top border (default for vertical layouts) */
.node-primary { border-top: 3px solid #0D9488; }
.node-secondary { border-top: 3px solid #0891B2; }
.node-tertiary { border-top: 3px solid #7C3AED; }
.node-green { border-top: 3px solid #059669; }
.node-orange { border-top: 3px solid #D97706; }

/* Left border (for horizontal/row layouts) */
.node-left-accent.node-primary { border-left: 3px solid #0D9488; border-top: none; }
```

### Light Theme Accent Colors

Use **deeper** accent colors for better contrast on light backgrounds:

| Color | Dark Theme | Light Theme |
|-------|------------|-------------|
| Teal | `#14B8A6` | `#0D9488` |
| Cyan | `#06B6D4` | `#0891B2` |
| Purple | `#8B5CF6` | `#7C3AED` |
| Green | `#10B981` | `#059669` |
| Orange | `#F59E0B` | `#D97706` |
| Red | `#EF4444` | `#DC2626` |

### Light Theme Badges

Same pattern - colored text on light colored background. Use `0.12` opacity (not `0.2`):

```css
.badge {
    background: rgba(8, 145, 178, 0.12);  /* 0.12 opacity */
    color: #0891B2;  /* Colored text */
    font-size: 12px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    padding: 6px 16px;
    border-radius: 20px;
}
```

### Light Theme Arrows

```css
.arrow-icon {
    font-size: 24px;
    color: #0D9488;  /* Teal */
    opacity: 0.6;
}
```

### Light Theme Typography

| Element | Size | Weight | Color |
|---------|------|--------|-------|
| Node titles | 16-20px | 500 | `#1E293B` |
| Node descriptions | 13-14px | 400 | `#64748B` |
| Badge/pill text | 12px | 600 | Accent color |
| Labels | 11-12px | 600 | `#94A3B8` |

### Light Theme Opacity Guide

| Element | Dark Theme | Light Theme |
|---------|------------|-------------|
| Card background | `rgba(color, 0.05)` | `#FFFFFF` (solid) |
| Card border | `rgba(color, 0.4)` | Shadow + accent border |
| Badge background | `0.2` | `0.12` |
| Icon container | `0.2` | `0.12` |
| Background glow | `0.15` / `0.10` | `0.06` / `0.06` |

### Light Theme initialBuild

For static export (screenshots), set `initialBuild` to show all builds:

```javascript
const totalBuilds = 5;
const initialBuild = 5;  // Show all for static export
```

---

## Shared Components

| File | Location | Purpose |
|------|----------|---------|
| `header.css` | `library/creative-dna/diagrams/components/` | Gradient title, subtitle, content wrapper |
| `typography.css` | `library/creative-dna/diagrams/components/` | Standard typography classes for diagram text |
| `typography-colors.css` | `library/themes/clean-slate/` | Theme-specific text colors (clean-slate) |
| `nodes.css` | `library/creative-dna/diagrams/components/` | Node styles |
| `connectors.css` | `library/creative-dna/diagrams/components/` | Arrows and connection lines |
| `layers.css` | `library/creative-dna/diagrams/components/` | Layered architecture diagrams |

## Diagram Templates

| Template | Use Case |
|----------|----------|
| `diagram-template.html` | Light theme (blogs, docs, Medium) |

The diagram template is in `library/creative-dna/diagrams/`. It links the clean-slate theme externally.
