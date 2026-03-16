# Build Animation Standards

Builds allow content to appear progressively during presentations. This creates engagement and controls information flow.

## Build System Overview

The build system uses:
- `data-build="N"` attributes to mark build order
- `.visible` class to show elements
- JavaScript for keyboard navigation
- CSS transitions for smooth animations

## HTML Markup

### Build Items
```html
<!-- Items that build in sequentially -->
<div class="build-item" data-build="1">First item to appear</div>
<div class="build-item" data-build="2">Second item to appear</div>
<div class="build-item" data-build="3">Third item to appear</div>
```

### Always Visible Items
```html
<!-- Items visible from slide load (no data-build attribute) -->
<div class="always-visible visible">This is always shown</div>
```

### Pre-Visible Items
```html
<!-- Items visible at start but still part of build tracking -->
<div class="build-item visible" data-build="0">Visible from start</div>
```

## CSS Transitions

### Standard Fade + Slide Up
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

### Fade Only (for diagrams)
```css
.build-item {
    opacity: 0;
    transition: opacity 0.5s ease-out;
}

.build-item.visible {
    opacity: 1;
}
```

### Scale In (for emphasis)
```css
.build-item {
    opacity: 0;
    transform: scale(0.8);
    transition: all 0.5s ease-out;
}

.build-item.visible {
    opacity: 1;
    transform: scale(1);
}
```

### Slide from Side
```css
/* From left */
.build-item {
    opacity: 0;
    transform: translateX(-30px);
    transition: all 0.5s ease-out;
}

/* From right */
.build-item.from-right {
    transform: translateX(30px);
}

.build-item.visible {
    opacity: 1;
    transform: translateX(0);
}
```

## JavaScript Navigation

Include this script in every slide with builds:

```javascript
let currentBuild = 0;
const totalBuilds = X; // Set to your total number of builds
const buildItems = document.querySelectorAll('[data-build]');

function showBuild(buildNumber) {
    buildItems.forEach(item => {
        const itemBuild = parseInt(item.dataset.build);
        if (itemBuild <= buildNumber) {
            item.classList.add('visible');
        } else {
            item.classList.remove('visible');
        }
    });
}

document.addEventListener('keydown', (e) => {
    if (e.key === 'ArrowRight' || e.key === ' ') {
        if (currentBuild < totalBuilds) {
            currentBuild++;
            showBuild(currentBuild);
        }
    } else if (e.key === 'ArrowLeft') {
        if (currentBuild > 0) {
            currentBuild--;
            showBuild(currentBuild);
        }
    }
});

// Initialize - set to 0 for nothing shown, or higher for initial state
showBuild(0);
```

See `builds.js` for a copy-paste ready version.

## Keyboard Controls

| Key | Action |
|-----|--------|
| `→` (Right Arrow) | Advance to next build |
| `Space` | Advance to next build |
| `←` (Left Arrow) | Go back one build |

## Best Practices

### DO:
- Number builds sequentially (1, 2, 3...)
- Group related items on the same build number if they should appear together
- Use consistent transition timing across a presentation
- Test keyboard navigation before finalizing

### DON'T:
- Skip build numbers (1, 2, 4... - missing 3)
- Add visible build count indicators to the slide
- Make transitions too fast (<0.3s) or too slow (>0.8s)
- Use jarring transition effects

## Simultaneous Builds

Multiple items can appear on the same build:

```html
<div class="build-item" data-build="1">These appear</div>
<div class="build-item" data-build="1">at the same time</div>
<div class="build-item" data-build="2">This appears next</div>
```

## Staggered Builds

For staggered timing on same build, use CSS delays:

```css
.build-item[data-build="1"]:nth-child(1) { transition-delay: 0s; }
.build-item[data-build="1"]:nth-child(2) { transition-delay: 0.1s; }
.build-item[data-build="1"]:nth-child(3) { transition-delay: 0.2s; }
```
