# Content Studio Automation — Design Document

**Version:** 9.0
**Date:** 2026-02-14
**Author:** George + Claude

---

## 1. Vision

Content Studio is a **Claude Code-native content creation pipeline** where the entire workflow — from research to published deliverable — is driven through natural language conversations with Claude Code in VS Code.

### 1.1 The Content Creation Workflow

Every content project — whether a blog, a presentation, or a standalone image — follows the same two-phase pattern. This is the workflow that Content Studio exists to automate and streamline:

```
┌─────────────────────────────────────────────────────────────────────────┐
│                                                                         │
│              PHASE 1: RESEARCH & CONTEXT CREATION                       │
│              ─────────────────────────────────────                       │
│              Iterates on UNDERSTANDING                                  │
│              (angle, audience, narrative arc)                            │
│                                                                         │
│   ┌──────────┐    ┌────────────┐    ┌──────────┐    ┌──────────────┐   │
│   │  GATHER   │───▶│ SYNTHESIZE │───▶│ DISCUSS  │───▶│   OUTLINE    │   │
│   │           │    │            │    │          │    │              │   │
│   │ Videos    │    │ Claude     │    │ You +    │    │ Structured   │   │
│   │ Articles  │    │ reads all  │    │ Claude   │    │ plan of the  │   │
│   │ PDFs      │    │ sources,   │    │ shape    │    │ content —    │   │
│   │ Docs      │    │ surfaces   │    │ the      │    │ iterated     │   │
│   │ Code      │    │ themes     │    │ angle    │    │ v1 ... vN    │   │
│   └──────────┘    └────────────┘    └──────────┘    └──────────────┘   │
│        ▲                                                   │            │
│        └────────────── ↺ repeat until vision captured ─────┘            │
│                                                                         │
│   Output: ✦ GOLD CONTEXT DOCUMENTS ✦                                   │
│   (the refined outline — the bridge to Phase 2)                         │
│                                                                         │
└─────────────────────────────────┬───────────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                                                                         │
│              PHASE 2: CREATIVE ITERATION                                │
│              ───────────────────────────                                 │
│              Iterates on EXECUTION                                      │
│              (prose, visuals, scripts, slides)                           │
│                                                                         │
│    ┌─────────────────────────────┐        ┌─────────────────────────────┐│
│    │    BLOG PATH                │        │   PRESENTATION PATH          ││
│    │                             │        │                              ││
│    │  Blog Draft    ←→  ↺       │        │  Outline      ←→  ↺        ││
│    │    ▸ blog-writing           │        │    ▸ outline-writing         ││
│    │       ↓                     │        │       ↓                      ││
│    │  Diagrams      ←→  ↺       │        │  HTML Slides  ←→  ↺        ││
│    │    ▸ diagram-conventions    │        │    ▸ slide-conventions       ││
│    │       ↓                     │        │       ↓                      ││
│    │  Video Script  ←→  ↺       │        │  AI Images    ←→  ↺        ││
│    │    ▸ video-script           │        │       ↓                      ││
│    │       ↓                     │        │  Google Deck  ←→  ↺        ││
│    │  LinkedIn Post ←→  ↺       │        │       ↓                      ││
│    │    ▸ linkedin-writing       │        │  Talk Track   ←→  ↺        ││
│    │                             │        │    ▸ talk-track-writing      ││
│    │  ──────────────────────     │        │       ↓                      ││
│    │  BLOG PACKAGE:              │        │  Audio        ←→  ↺        ││
│    │  • Blog markdown            │        │       ↓                      ││
│    │  • Diagram PNGs             │        │  PDF Export                  ││
│    │  • Demo video script        │        │  ──────────────────────      ││
│    │  • LinkedIn post            │        │  PRESO PACKAGE:              ││
│    │                             │        │  • Google Slides deck        ││
│    │                             │        │  • Talk track                ││
│    │                             │        │  • Audio MP3                 ││
│    │                             │        │  • PDF export                ││
│    └─────────────────────────────┘        └─────────────────────────────┘│
│                                                                         │
│              IMAGE PATH (lightweight):                                   │
│              Brief → HTML Diagrams ←→ ↺ → /screenshot → PNGs           │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

**Key properties of this workflow:**

- **Phase 1 is universal.** The same research-and-synthesis loop regardless of what you're building. Gold context documents are reusable — a presentation outline could seed a blog, or vice versa.
- **Phase 2 deliverables cascade.** Each deliverable becomes context for the next. Blog text feeds diagrams, which feed the video script, which feeds the LinkedIn post. Slides feed the talk track, which feeds audio. This is why they live in one project.
- **Both phases are deeply iterative.** Phase 1 iterates on understanding ("focus on the practitioner angle", "the arc should build from fear to freedom"). Phase 2 iterates on execution ("make the title bigger on slide 3", "this section needs a diagram"). The `↺` loops are where the creative work happens.
- **Every iteration loop is style-aware.** The `▸ skill-name` annotations in the diagram show that each deliverable auto-loads its style guide — the creator's voice, structure, and conventions — so Claude never falls back to generic AI output. This is the Style Layer in action (see Section 1.4).
- **The outline is the bridge.** It's the last thing produced in Phase 1 and the first thing consumed in Phase 2. A Reconciliation presentation outline went through 14 versions before a single slide was created.

> For the complete workflow specification including iteration loops, deliverable cascades, and auto-loading intelligence, see `docs/design/content-creation-workflow.md`.

### 1.2 What Content Studio Automates

Content Studio doesn't replace the creative process — it **streamlines every mechanical step** so the human can focus on the creative decisions. Here's how automation maps to each workflow step:

```
WORKFLOW STEP          YOU DO                          CONTENT STUDIO DOES
─────────────────────  ──────────────────────────────  ─────────────────────────────────────

Phase 1:

  Gather sources       Paste a URL or drop a file      /add-youtube → transcript extracted
                                                       /add-webpage → content extracted
                                                       Lands in context/sources/

  Synthesize           "What themes do you see?"       Claude reads ALL sources, surfaces
                                                       themes, tensions, connections

  Discuss              "Focus on the practitioner       Claude proposes angles, refines
                       angle, not the theory"          framing, identifies narrative arcs

  Outline              "More personal in section 3"    Claude creates + iterates outline
                       "Add a film reference"          versions → context/gold/
                                                       Auto-loads outline-writing conventions
                                                       (narrative architecture, composition
                                                       patterns, outline document format)

Phase 2:

  Create content       Review output, give feedback    Auto-loads the right conventions:
                                                        • slide-conventions (slide HTML)
                                                        • outline-writing (outline markdown)
                                                        • blog-writing (blog markdown)
                                                        • diagram-conventions (diagram HTML)
                                                        • talk-track-writing (talk track md)
                                                        • video-script (demo script md)

  Capture visuals      Review the PNG                  /screenshot → Selenium → retina PNG

  Generate images      "Make it warmer, more abstract" /image → Gemini API → PNG

  Publish deck         Review in Google Slides         /publish → creates full deck
                       "Tweak slide 3"                 /sync 3 → just slide 3 updates
                                                       First time? Paste a Drive folder URL
                                                        → folder ID extracted automatically
                                                       First time? Browser opens for OAuth
                                                        → token cached, never asked again

  Narrate              Listen and approve              /narrate → ElevenLabs TTS → MP3

  Export               Approve                         /export → Google Drive API → PDF
```

The pattern: **you make creative decisions, Content Studio handles execution.** You never leave VS Code. You never manually copy files, run scripts, or switch tools. Every action is a natural language command or a `/skill`.

**The publish experience is deliberately frictionless.** The first time you `/publish`, the skill detects that no Drive folder is configured and asks you to paste a folder URL — not a raw ID, just the URL from your browser. It extracts the folder ID, saves it to `project.yaml`, and proceeds. OAuth opens a browser once for authorization, then caches the token. From that point on, `/publish` and `/sync` are single-command operations — the mechanical steps (screenshot, upload, create deck, map slides) happen invisibly. The goal: going from "I edited slide 3" to seeing the update in Google Slides should feel as fast as saving a file.

### 1.3 The Four-Layer Architecture

Four complementary layers make this possible:

```
┌─────────────────────────────────────────────────────────────────────┐
│                                                                     │
│   STYLE GUIDES (knowledge — your voice as code)                     │
│   ─────────────────────────────────────────────                     │
│   Style guides and standards that capture how YOU create — your     │
│   narrative architecture, visual conventions, writing voice,        │
│   delivery style. This is what makes the output sound like you      │
│   instead of generic AI. Every deliverable has a guide.             │
│                                                                     │
│   Content creation:  blog-style-guide, presentation-deck-style-     │
│                      guide, talk-track-style-guide, demo-script-    │
│                      style-guide                                    │
│   Technical impl:    slide-standards, diagram-standards             │
│                                                                     │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│   SKILLS (orchestration — context injection)                        │
│   ──────────────────────────────────────────                        │
│   SKILL.md files that teach Claude WHEN and HOW to run workflows.   │
│   Auto-loaded skills detect what you're editing and inject the      │
│   relevant style guide into Claude's context — no manual "read      │
│   the style guide first" needed. User-invoked skills (/screenshot,  │
│   /publish, /sync, /narrate, /export) trigger CLI commands.         │
│                                                                     │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│   CLI (execution)                                                   │
│   ───────────────                                                   │
│   cstudio commands that do the actual work: screenshot, publish,    │
│   sync, image, audio, export. Driven by project.yaml config.       │
│   Deterministic, testable, callable from skills or directly.        │
│                                                                     │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│   APIs (external services)                                          │
│   ────────────────────────                                          │
│   Google Slides API    — publish/sync decks                         │
│   Google Drive API     — export PDF                                 │
│   Gemini API           — generate images from prompts               │
│   ElevenLabs TTS API   — generate audio narration                   │
│   YouTube Transcript   — extract video transcripts                  │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

Style guides are the knowledge layer — they hold your creative DNA. Skills are the injection layer — they deliver that knowledge to Claude at the right moment. The CLI is the muscle. APIs are the external reach. Together they give Claude Code deep, project-aware automation where every piece of output reflects the creator's voice and style.

### 1.4 The Style Layer — Voice as Code

The most important architectural insight: **if the agent produces it, teach the agent how you produce it.**

Every content creator has a signature — the way they structure a narrative, the pacing of a talk track, the visual grammar of their slides. Without explicit style guides, Claude produces content using generic AI best practices: competent but impersonal. It sounds like "an AI wrote this." With style guides loaded, the output reflects the creator's specific patterns, voice, and design sensibility. It sounds like *you*.

This is what separates Content Studio from a blank-slate AI assistant. Claude doesn't just know *what* to create — it knows *how you create it*.

**The Completeness Principle:** Every key creative deliverable must have three things:

1. **A style guide** — the rules, voice, structure, and patterns that define how *you* do it
2. **An auto-loaded skill** — context injection that loads the guide automatically when that deliverable is being created
3. **A clear trigger pattern** — file type + project context so the skill loads without user intervention

If any deliverable is missing its style guide or skill, the agent falls back to generic output for that artifact — even if every other artifact is perfectly styled. The chain is only as strong as its weakest link.

**The complete map** (see Section 13 for full rationale):

| Deliverable | Style Guide | Auto-Loaded Skill |
|---|---|---|
| Presentation outline | `presentation-deck-style-guide.md` | `outline-writing` |
| Blog post | `blog-style-guide.md` | `blog-writing` |
| Talk track | `talk-track-style-guide.md` | `talk-track-writing` |
| Demo script | `demo-script-style-guide.md` | `video-script` |
| Slide HTML | `slide-standards.md` | `slide-conventions` |
| Diagram HTML | `diagram-standards.md` | `diagram-conventions` |

Style guides split into two natural categories that mirror the workflow: **content creation guides** (`{thing}-writing`) teach voice and narrative structure; **technical implementation guides** (`{thing}-conventions`) teach layout, CSS, and visual patterns. This distinction reflects a real difference — writing outlines and talk tracks requires understanding of narrative arc and emotional pacing, while building slides and diagrams requires understanding of grid systems, component CSS, and build animations.

The style layer is what makes the four-layer architecture more than mechanical automation. Skills, CLI, and APIs handle *execution*. Style guides handle *identity*.

### 1.5 Project Types

Content Studio supports **three project types**, each producing its own deliverable package:

| Project Type | Visual Deliverable | Written Deliverable | Published To |
|---|---|---|---|
| **Presentation** | HTML slides → Google Slides deck | Outline, talk track, audio, PDF | Google Slides |
| **Blog** | HTML diagrams → PNGs for blog | Blog markdown, demo video script | WordPress, Medium, YouTube |
| **Image** | HTML diagrams/visuals → PNGs | (none) | README, social media, docs |

**Theme is a project-level choice**, not a project-type binding. Currently sacred-gold is used for OCIA presentations and clean-slate for blog diagrams and images, but any project can use any theme.

All three project types share the same foundation: 1280×720 HTML canvas, `cstudio screenshot` for PNG generation, `project.yaml` for configuration, and skills for Claude Code orchestration.

### 1.6 The Goal

Say "Create a new blog about [topic]" or "Create a new presentation on [topic]" — and Claude Code orchestrates everything: project setup, context gathering, content iteration, visual creation, screenshot generation, publishing — all without leaving VS Code.

### 1.7 Validation

- **Presentations:** The Reconciliation presentation (16 slides, talk track, Google Slides deck) serves as the acceptance test.
- **Blogs + diagrams:** The "Launching Agentic Mindset" blog (4 diagrams, demo video script) serves as the blog acceptance test.
- **Images:** First standalone image project (e.g., README diagrams for a GitHub repo) serves as the image acceptance test.

---

## 2. Current State

### What's Been Accomplished

| Phase | Status | What Was Done |
|-------|--------|---------------|
| Phase 0: Directory restructure | **Complete** | Repo reorganized to `library/`, `projects/`, `docs/`, `tools/` layout |
| Phase 0: Theme extraction (sacred-gold) | **Complete** | `theme-base.css`, `header.css`, `build-system.css`, `builds.js` extracted from reconciliation slides |
| Phase 0: Reconciliation refactor | **Complete** | All 16 slides refactored to use shared CSS/JS |
| Phase 0: Beatitudes refactor | **Complete** | All 24 content slides refactored (net -1,806 lines) |
| Phase 1: CLI (`cstudio`) | **Complete** | `cstudio status`, `cstudio screenshot`, `cstudio init` working |
| Phase 1: Project config | **Complete** | `project.yaml` for reconciliation + beatitudes |
| Phase 1: Skills | **Complete** | `/screenshot`, `/new-project`, `slide-conventions` skills created |
| Phase 1: CLAUDE.md | **Complete** | Updated with CLI reference and skills overview |

### Phase 1.5 Progress (In Progress)

Phase 1.5 is partially complete. Several tasks were implemented with deviations from this design doc that need to be corrected. See the implementation guide for the full correction plan.

| Step | Status | Notes |
|------|--------|-------|
| Remove `agentic-mindset` theme | **Done** | Directory deleted, no HTML ever referenced it |
| Clean-slate theme extraction | **Done** | `theme-base.css` extracted. `diagram-template.html` updated. `theme.md` created. `typography.css` (structural) + `typography-colors.css` (theme-specific colors) split complete |
| Blog diagram refactoring | **Done (needs correction)** | 4 diagrams refactored to shared CSS. But directory is `images/` — needs rename to `diagrams/` per this doc |
| Blog project config | **Done (needs correction)** | `project.yaml` exists but uses `slides_dir: images` instead of `diagrams_dir: diagrams`. Missing `blog` and `demo_video` sections |
| Image project type in CLI | **Done (needs correction)** | `cstudio init --type image` works. But config.py doesn't resolve `diagrams_dir`/`images_dir` — uses `slides_dir` for all types |
| Style guide organization | **Done** | Moved to `library/creative-dna/writing/` and `library/creative-dna/videos/` |
| Reference blogs | **Partially done** | 1 blog in `library/creative-dna/writing/reference-blogs/`. Needs: add remaining published blog markdown files |
| Auto-loaded skills | **Done** | `diagram-conventions`, `blog-writing`, `video-script` created |
| Context gathering skills | **Done** | `/add-youtube` and `/add-webpage` skills created |
| CLAUDE.md update | **Done (needs correction)** | Updated for all 3 types, but uses wrong field names (`slides_dir` instead of `diagrams_dir`) |
| `/new-project` (renamed from `/new-presentation`) | **Done** | Supports all 3 project types + theme selection |

### What Remains (Phase 2+)

| Step | Current State | Target |
|------|-------------|--------|
| Google Slides API | Not started | `cstudio publish`, `cstudio sync --slide N` |
| Gemini image generation | Not started | `cstudio image <slide>` |
| ElevenLabs audio | Not started | `cstudio audio` |

---

## 3. Project Types & Workflows

### 3.0 Two-Phase Workflow & Gold Context (All Project Types)

Every content project — whether a blog or a presentation — follows the same two-phase pattern:

- **Phase 1: Research & Context Creation** → produces **Gold Context Documents**
- **Phase 2: Creative Iteration** → produces finished content assets

Phase 1 is universal — the same research and synthesis loop regardless of what you're building. Phase 2 forks into different creative paths depending on the content type. Both phases are iterative.

> For the complete workflow description including iteration loops, deliverable cascades, and auto-loading intelligence, see `docs/design/content-creation-workflow.md`.

#### Phase 1: Research & Context Creation

This is the **intake, sense-making, and shaping** phase. You gather raw materials, synthesize them with Claude, and iterate until you arrive at refined context that becomes the foundation for everything that follows.

**What goes into `context/sources/` (raw materials):**

| Source Type | How It Gets There | Example |
|---|---|---|
| PDFs, articles | User drops file directly | `reconciliation-article.pdf` |
| Markdown docs | User drops file directly | `backend-architecture.md`, `rag-system-analysis.md` |
| Code files | User drops file directly | `agent.py`, `config.ts` |
| Screenshots, demo flows | User drops file directly | `demo-flow.pdf`, `ui-screenshot.png` |
| YouTube transcripts | `/add-youtube <url>` skill | Auto-extracted to `context/sources/transcripts/` |
| Web page content | `/add-webpage <url>` skill | Auto-extracted to `context/sources/web/` |

**The iteration loop:**

```
1. GATHER        Assemble source materials into context/sources/
                 Mix of /add-youtube, /add-webpage, and manual drops

2. SYNTHESIZE    Claude reads all sources and surfaces:
                 → Key themes and tensions
                 → Potential angles and narratives

3. DISCUSS       You and Claude shape the direction:
                 → "Focus on the practitioner angle"
                 → "The narrative arc should build from fear to freedom"

4. OUTLINE       Claude creates a structured outline from the synthesis
                 You iterate: "Make section 3 more personal"
                 Multiple versions → {topic}-outline-v1.md ... vN.md

     ↺ Repeat steps 2–4 until the outline captures your vision
```

#### Gold Context Documents

The output of Phase 1 isn't raw materials — it's the **refined understanding**: the iterated outline, the agreed-upon angle, the narrative arc, the key takeaways. These are the **Gold Context Documents** — the bridge between research and creation.

| Content Type | Primary Gold Context Output |
|---|---|
| **Presentation** | Detailed deck outline — sections, slide concepts, build sequences, key quotes |
| **Blog** | Detailed blog structure outline — sections, key points, diagram placement, narrative flow |
| **Image** | Brief — what to create, visual approach, composition notes |

Gold context lives in `context/gold/`, explicitly separated from raw source materials:

**Context directory standard:**

```
context/
├── sources/                    # Phase 1 INPUTS — raw materials
│   ├── transcripts/            #   Auto-created by /add-youtube
│   │   └── {video-title}.txt
│   ├── web/                    #   Auto-created by /add-webpage
│   │   └── {page-title}.md
│   └── (user files)            #   PDFs, markdown, code, images — flat
├── gold/                       # Phase 1 OUTPUTS — refined understanding
│   ├── {topic}-outline-v4.md   #   The iterated outline (primary gold artifact)
│   └── archive/                #   Previous outline versions
└── prompts/                    # Saved AI prompts (image generation, etc.)
```

- `context/sources/` = what you feed IN (raw materials)
- `context/gold/` = what comes OUT of research iteration (refined understanding)
- `context/prompts/` = saved AI prompts for image generation experiments

User-provided files go directly into `context/sources/`. Skill-extracted content goes into typed subfolders (`transcripts/`, `web/`) so it's easy to distinguish auto-generated from user-provided material.

> **Legacy note:** The reconciliation project (2026-03) was created before this standard was established. It uses `context/sources/videos/` and `context/sources/articles/` instead of `transcripts/` and `web/`, and has `outline/` at the project root instead of `context/gold/`. New projects should use the standard names above. Existing projects will not be renamed — they work fine as-is.

**Demo moment:** User pastes a YouTube URL → `/add-youtube` extracts the transcript → Claude reads it and summarizes the key points — all visible in VS Code.

### 3.1 Presentation Projects (`type: presentation`)

**Standards:** `slide-conventions` (auto-loaded when editing slide HTML)
**Theme:** Project-configurable (e.g., sacred-gold for OCIA, clean-slate for professional/technical)

**Current primary use:** OCIA presentations (~15 candidates, highly visual, narrative-driven, ~60 minutes).

**Full lifecycle:**

```
Phase 1: Context & Research
├── Assemble source materials into context/sources/
│   ├── Drop PDFs, articles, transcripts
│   ├── /add-youtube <conference-talk-url>       → transcript extracted
│   └── /add-webpage <article-url>               → content extracted
├── Claude reads all context sources
├── "I've read 6 sources. Here are the key themes I see..."
└── User + Claude discuss angle, narrative arc, audience

Phase 2: Outline
├── "Create an outline for a 60-minute presentation on Reconciliation"
├── Claude creates structured outline from context
├── User iterates: "Make section 3 more personal"
│                  "Add a film reference in the opening"
│                  "The ending should build to a call to action"
├── Multiple versions → outline/{topic}-outline-v1.md ... vN.md
└── Final outline approved

Phase 3: HTML Slides
├── "Create slides 1-5 from the outline"
├── Claude creates slides using project theme + slide-conventions
│   ├── Components from library/creative-dna/slides/components/
│   ├── Build animations with data-build attributes
│   └── Image placeholders with AI prompts where needed
├── /screenshot → verify visuals in PNG
├── User iterates: "Make the title bigger on slide 3"
│                  "Add a build step for the Augustine quote"
│                  "The four-column grid needs more spacing"
├── Continue through all slides
└── All slides created: slides/slide-01-title.html ... slide-NN-closing.html

Phase 4: Image Generation
├── /image slide-04 → reads prompt file → Gemini generates image
├── User reviews: "Make it warmer" / "More abstract"
├── Lumen updates prompt file → regenerates → re-screenshots
└── Generated images embedded in HTML: slides/images/*.png

Phase 5: Publish to Google Slides
├── /publish → creates Google Slides deck from all screenshots
│   ├── First time only: "Paste your Google Drive folder URL" → ID extracted
│   ├── First time only: browser opens for OAuth → token cached
│   └── After setup: single command, no prompts
├── User reviews deck in Google Slides
├── Need to tweak slide 3? Edit HTML → /sync --slide 3
│   (only slide 3 re-screenshots and updates in Google Slides)
├── Build count changed on slide 9? /sync --slide 9
│   (old Google Slides removed, new ones inserted at same position)
└── Deck ready for presenting

Phase 6: Talk Track + Audio
├── "Generate a talk track from the outline and slides"
├── Claude creates natural speaking script
│   └── talk-track-writing skill auto-loaded when editing talk track markdown
│       (voice, structure, delivery style, emotional calibration)
├── User iterates: "The opening should feel more conversational"
│                  "Add a pause before the Aquinas quote"
├── /narrate → ElevenLabs generates MP3
└── Audio ready: talk-track/audio/*.mp3

Phase 7: Export
├── /export → Google Drive API exports deck as PDF
└── PDF saved: exports/{topic}-deck.pdf
```

**Demo moments:**
- `/add-youtube <url>` → transcript appears in context/
- "Create slides 1-5" → HTML files appear in file explorer, `/screenshot` → PNGs render
- Edit slide 3 → `/sync 3` → single slide updates in Google Slides deck

**Example projects:**
- `projects/personal/ocia/2025-12-beatitudes/` (24 content slides + placeholders, "Life is Beautiful" film clips)
- `projects/personal/ocia/2026-03-reconciliation/` (16 slides, "From Fear to Freedom" arc)

### 3.2 Blog Projects (`type: blog`)

**Standards:** `blog-writing` (auto-loaded for markdown), `diagram-conventions` (auto-loaded for diagram HTML), `video-script` (auto-loaded for script markdown), `linkedin-writing` (auto-loaded for linkedin-post markdown)
**Theme:** Project-configurable (currently clean-slate for diagrams)

A blog project can include up to four deliverables: the **blog post**, **diagrams**, a **demo video script**, and a **LinkedIn post**. Each builds on the previous — the blog is context for the diagrams, both are context for the video script, and the finished blog + demo video are context for the LinkedIn post.

**Full lifecycle:**

```
Phase 1: Context & Research
├── Assemble source materials into context/sources/
│   ├── Architecture docs, design documents, code files
│   ├── /add-youtube <conference-talk-url>       → transcript extracted
│   ├── /add-webpage <competitor-blog-url>       → content extracted
│   └── Demo flow PDF (screenshots of the demo sequence)
├── Claude reads all context + blog-style-guide + reference blogs
├── "I see 3 main themes: the RAG architecture, the agent framework,
│    and the deployment story. Which angle resonates?"
└── User + Claude agree on angle, audience, key takeaways

Phase 2: Blog Draft + Diagrams (iterative, section by section)
├── "Write the first section — lead with the real-world problem"
├── Claude creates draft using blog-style-guide voice
│   ├── blog-writing skill auto-loaded when editing markdown
│   └── References published blogs for voice consistency
├── Blog versions live in blog/ subdirectory: blog/{slug}-v1.md ... vN.md
├── User iterates section by section:
│   ├── "Rewrite the intro with a concrete scenario, not abstract"
│   ├── "This section needs a diagram to explain the architecture"
│   │   → Claude creates HTML diagram → /screenshot → PNG
│   │   → diagram-conventions auto-loaded for HTML editing
│   ├── "The tone is too formal here — make it more conversational"
│   ├── "Add a code example for the RAG pipeline config"
│   └── "This diagram needs a 5th node for the cache layer"
│       → Edit diagram HTML → /screenshot → updated PNG
├── Diagrams created alongside: diagrams/*.html
└── /screenshot → all diagram PNGs ready: diagrams/screenshots/*.png

Phase 3: Blog Finalization
├── All sections polished, all diagrams created
├── Final review pass for voice consistency across entire post
├── Embed diagram PNGs into blog markdown (image references)
└── Blog ready for publishing

Phase 4: Demo Video Script (optional — after blog is finalized)
├── User provides demo flow PDF (screenshots showing the demo sequence)
├── Claude reads blog + diagrams + demo flow + demo-script-style-guide
│   └── video-script skill auto-loaded when editing script markdown
├── "Write a 5-minute demo script following the demo flow"
├── User iterates: "Make the opening hook shorter"
│                  "Add a callout when the config file is shown"
│                  "The closing should reference the blog for details"
└── Final script: demo-video/{slug}-demo-script-vN.md

Phase 5: LinkedIn Post (optional — after demo video is finalized)
├── Claude reads finished blog + demo video URL + linkedin-post-style-guide + reference posts
│   └── linkedin-writing skill auto-loaded when editing linkedin-post markdown
├── User selects post category (usually Category A: Build Post for blog announcements)
├── "Write the LinkedIn post for this blog"
├── Claude drafts post: hook → context → proof → insight → human landing → resources
├── User iterates: "Make the hook more personal"
│                  "Name the pattern in the insight section"
│                  "The closing line needs to be punchier"
└── Final post: linkedin-post/{slug}-linkedin-v1.md ... vN.md

Phase 6: Publish
├── Blog → WordPress/Medium (manual copy or future /publish-blog)
├── Diagram PNGs uploaded as blog images
├── Record demo in Camtasia following script → export MP4
├── Upload to YouTube → link in blog post
├── Publish LinkedIn post → link in project.yaml
└── Published: blog URL + video URL + LinkedIn post URL in project.yaml
```

**Demo moments:**
- "This section needs a diagram" → Claude creates HTML → `/screenshot` → PNG appears — all in one conversation
- Blog voice consistency: Claude auto-loads blog-style-guide and references published blogs
- Demo script: Claude reads the finished blog + demo flow PDF → produces a structured script

**Example project:** `projects/professional/blogs/2026-01-mindset-agent-launch/`

### 3.3 Image Projects (`type: image`)

**Standards:** `diagram-conventions` (auto-loaded when editing diagram HTML)
**Theme:** Project-configurable

An image project produces standalone HTML diagrams/visuals → PNGs. These aren't tied to a blog — they're for READMEs, social media, documentation, slide decks, or any context where you need polished technical visuals.

**Full lifecycle:**

```
Phase 1: Context & Brief
├── User describes what images they need:
│   ├── "I need 3 architecture diagrams for my project README"
│   ├── "Create social media graphics for the product launch"
│   └── "I need a system overview diagram for the design doc"
├── User provides context: architecture docs, existing visuals, references
│   └── /add-webpage <reference-url> for design inspiration
└── Claude + user agree on the visual approach, layout, color scheme

Phase 2: Create Visuals
├── Claude creates HTML diagrams/visuals
│   ├── Uses project theme + diagram-conventions
│   ├── Same 1280×720 canvas
│   ├── Builds for progressive reveal (optional)
│   └── Left-to-right flow for architecture diagrams
├── /screenshot → capture PNGs
├── User iterates: "Add the cache layer between API and DB"
│                  "Use purple for the agent nodes"
│                  "Make the title shorter"
└── All visuals finalized: images/*.html

Phase 3: Export
├── /screenshot → final PNGs: images/screenshots/*.png
└── User copies PNGs to target (README, social media, docs, etc.)
```

**Demo moment:** "I need an architecture diagram for my README" → Claude creates HTML → `/screenshot` → clean PNG ready to embed.

**Example use cases:**
- Architecture diagrams for a GitHub README
- Social media graphics for a product launch
- Technical illustrations for documentation
- Conference talk visuals (without a full presentation project)

---

## 4. Project Structure

### 4.1 Repository Layout

```
content-studio/
│
├── tools/                              # ── ALL TOOLING CODE ──
│   ├── cstudio/                        # CLI package (python -m cstudio)
│   │   ├── __init__.py
│   │   ├── __main__.py                 # Entry point
│   │   ├── cli.py                     # CLI argument parsing + command routing
│   │   ├── config.py                   # project.yaml loading + validation
│   │   ├── screenshots.py             # Selenium screenshot engine
│   │   ├── init.py                    # Project scaffolding
│   │   ├── scrape.py                  # Web content extraction via headless Chrome
│   │   ├── transcribe.py             # YouTube audio download + Whisper transcription
│   │   ├── utils.py                   # Credential loading, helpers
│   │   ├── exceptions.py             # Custom error types
│   │   ├── logging_config.py         # Structured logging setup
│   │   ├── gslides.py                 # Google Slides + Drive API wrapper (Phase 2)
│   │   ├── publish.py                # Publish/sync/export orchestration (Phase 2)
│   │   ├── images.py                  # Gemini image generation (Phase 3)
│   │   └── audio.py                   # TTS narration — ElevenLabs (Phase 4)
│   └── pyproject.toml
│
├── library/                            # ── SHARED CREATIVE ASSETS ──
│   │
│   ├── themes/                         # Visual themes (project-level choice)
│   │   ├── clean-slate/               # Light, technical (off-white canvas, white cards)
│   │   │   ├── theme-base.css          #   Base CSS (reset, body, off-white bg, border, fonts)
│   │   │   └── theme.md                #   Theme documentation (Phase 1.5 — to create)
│   │   │
│   │   └── sacred-gold/               # Church/personal (gold + dark)
│   │       ├── theme-base.css          #   Slide base (reset, body, background, noise)
│   │       ├── typography-colors.css   #   Text colors for typography classes
│   │       ├── slide-template.html
│   │       ├── title-slide-template.html
│   │       └── theme.md
│   │
│   ├── standards/                      # Design rules and content standards
│   │   ├── core/                       #   Shared across all content types
│   │   │   ├── dimensions.md           #     1280x720, 16:9
│   │   │   ├── builds.md              #     Build animation system
│   │   │   ├── builds.js             #     Reusable build JS (keyboard nav + showBuild)
│   │   │   └── file-naming.md         #     Naming conventions
│   │   ├── slides/                     #   Presentation slide standards
│   │   │   ├── slide-standards.md
│   │   │   └── components/            #     Reusable CSS components
│   │   │       ├── header.css
│   │   │       ├── typography.css     #     Standard text classes (sizes/weights)
│   │   │       ├── build-system.css
│   │   │       ├── two-column.css
│   │   │       ├── card.css
│   │   │       ├── quote-block.css
│   │   │       ├── stat-display.css
│   │   │       └── image-placeholder.css
│   │   ├── diagrams/                   #   Blog diagram standards
│   │   │   ├── diagram-standards.md
│   │   │   ├── diagram-template.html  #     Generic diagram template (links clean-slate)
│   │   │   └── components/
│   │   │       ├── header.css         #     Diagram header (gradient title, centered)
│   │   │       ├── nodes.css
│   │   │       ├── connectors.css
│   │   │       └── layers.css
│   │   ├── writing/                    #   Blog + video writing standards
│   │   │   ├── blog-style-guide.md    #     George's blog voice + structure rules
│   │   │   ├── demo-script-style-guide.md  # Demo video script voice + structure
│   │   │   └── reference-blogs/       #     Published blogs as voice exemplars
│   │   │       └── (markdown versions)
│   │   └── videos/                     #   Video production standards
│   │       └── video-standards.md     #     Recording, editing, export rules
│   │
│   └── project-templates/              # Scaffolding for cstudio init
│       ├── presentation/               #   Each template has a project.yaml.template.
│       │   └── project.yaml.template   #   Directory structure is created by init.py
│       ├── blog/                       #   code, not by template .gitkeep files.
│       │   └── project.yaml.template
│       └── image/
│           └── project.yaml.template
│
├── projects/                           # ── ALL CONTENT PROJECTS ──
│   │
│   ├── personal/
│   │   └── ocia/
│   │       ├── 2025-12-beatitudes/
│   │       │   ├── project.yaml
│   │       │   └── slides/ (24 content slides + placeholders)
│   │       └── 2026-03-reconciliation/
│   │           ├── project.yaml
│   │           ├── outline/
│   │           ├── slides/ (16 slides)
│   │           ├── talk-track/
│   │           ├── context/
│   │           └── final-preso/
│   │
│   └── professional/
│       ├── blogs/
│       │   └── 2026-01-mindset-agent-launch/
│       │       ├── project.yaml
│       │       ├── mindset-agent-blog-v4.md
│       │       ├── diagrams/ (4 HTML diagrams)    # Currently named images/ — rename pending
│       │       │   ├── screenshots/
│       │       │   └── archive/
│       │       ├── demo-video/
│       │       │   └── demo-script-v1.md
│       │       └── context/
│       └── presentations/                         # Created on first use
│
├── docs/                               # ── DOCUMENTATION ──
│   ├── design/
│   │   ├── content-studio-automation-design.md  # This document
│   │   ├── implementation-guide.md
│   │   └── standards/
│   │       └── logging-standards.md
│   ├── blog/
│   │   ├── design-decisions-and-learnings.md
│   │   └── images/
│   ├── completed-tasks/                #   Historical task records
│   ├── guides/                         #   (Phase 5 — to create)
│   │   ├── getting-started.md
│   │   ├── creating-a-presentation.md
│   │   ├── creating-a-blog.md
│   │   └── creating-images.md
│   └── reference/                      #   (Phase 5 — to create)
│       ├── cstudio-cli.md
│       └── project-yaml-spec.md
│
├── .claude/                            # ── CLAUDE CODE INTEGRATION ──
│   └── skills/
│       ├── screenshot/SKILL.md         #   /screenshot command
│       ├── new-project/SKILL.md        #   /new-project — scaffold any project type
│       ├── add-youtube/SKILL.md        #   /add-youtube — extract transcript
│       ├── add-webpage/SKILL.md        #   /add-webpage — extract web content
│       ├── publish/SKILL.md            #   /publish command (Phase 2)
│       ├── sync/SKILL.md               #   /sync command (Phase 2)
│       ├── image/SKILL.md              #   /image command (Phase 3)
│       ├── narrate/SKILL.md            #   /narrate command (Phase 4)
│       ├── export/SKILL.md             #   /export command (Phase 2)
│       ├── slide-conventions/SKILL.md  #   Auto: slide editing rules
│       ├── diagram-conventions/SKILL.md #  Auto: diagram editing rules
│       ├── outline-writing/SKILL.md   #   Auto: presentation outline rules
│       ├── blog-writing/SKILL.md       #   Auto: blog writing rules
│       ├── video-script/SKILL.md       #   Auto: demo script rules
│       └── talk-track-writing/SKILL.md #   Auto: talk track writing rules
│
├── CLAUDE.md                           # Claude Code project instructions
├── README.md
├── .env                               # Local credential config (gitignored)
└── .gitignore
```

### 4.2 Presentation Project Structure

```
projects/{personal|professional}/{category}/YYYY-MM-{topic}/
├── project.yaml                    # type: presentation, theme: <any theme>
│
├── context/                        # ── PHASE 1: RESEARCH ──
│   ├── sources/                    #   Raw materials (inputs)
│   │   ├── transcripts/            #     /add-youtube extracts
│   │   ├── web/                    #     /add-webpage extracts
│   │   └── (user files)            #     PDFs, articles, code — flat
│   ├── gold/                       #   Refined understanding (outputs)
│   │   ├── {topic}-outline-v4.md   #     THE bridge to Phase 2
│   │   └── archive/                #     Previous outline versions
│   └── prompts/                    #   Saved AI prompts
│
├── slides/                         # ── PHASE 2: SLIDES ──
│   ├── slide-01-title.html
│   ├── slide-02-intro.html
│   ├── ...
│   ├── images/                     #   Gemini-generated images
│   ├── screenshots/                #   Auto-generated PNGs (cstudio)
│   └── archive/                    #   Previous slide versions
│
├── talk-track/                     # ── PHASE 2: TALK TRACK ──
│   ├── {topic}-talk-track-v4.md    #   Master speaking script
│   ├── {topic}-tts-script.txt      #   Plain text for ElevenLabs input
│   ├── audio/                      #   Generated MP3s (ElevenLabs)
│   └── archive/                    #   Previous talk track versions
│
├── materials/                      # ── SUPPLEMENTARY (standard) ──
│   └── (handouts, table exercises, printouts, etc.)
│
└── exports/                        # ── PUBLISHED OUTPUT ──
    └── {title}.pdf                 #   PDF export of Google Slides deck
```

> **Legacy note:** The reconciliation project (2026-03) was created before this standard. It has `outline/` at root (→ `context/gold/`), `final-preso/` (→ `exports/`), `table-exercise/` (→ `materials/`), and a legacy `generate-slides.py` (replaced by `cstudio`). Existing projects will not be restructured.

### 4.3 Blog Project Structure

```
projects/professional/blogs/YYYY-MM-{slug}/
├── project.yaml                    # type: blog, theme: <any theme>
│
├── context/                        # ── PHASE 1: RESEARCH ──
│   ├── sources/                    #   Raw materials (inputs)
│   │   ├── transcripts/            #     /add-youtube extracts
│   │   ├── web/                    #     /add-webpage extracts
│   │   └── (user files)            #     PDFs, architecture docs, demo flow
│   ├── gold/                       #   Refined understanding (outputs)
│   │   ├── {slug}-outline-v3.md    #     Blog structure outline
│   │   └── archive/                #     Previous outline versions
│   └── prompts/                    #   Saved AI prompts
│
├── blog/                           # ── PHASE 2: BLOG POST ──
│   ├── {slug}-v4.md                #   Blog markdown (iterated)
│   └── archive/                    #   Previous blog versions
│
├── diagrams/                       # ── PHASE 2: DIAGRAMS ──
│   ├── architecture-overview.html
│   ├── data-pipeline-light.html
│   ├── screenshots/                #   Auto-generated PNGs (cstudio)
│   └── archive/                    #   Previous diagram versions
│
├── demo-video/                     # ── PHASE 2: DEMO VIDEO SCRIPT ──
│   ├── demo-script-v1.md           #   Demo video script
│   └── archive/                    #   Previous script versions
│
└── linkedin-post/                  # ── PHASE 2: LINKEDIN POST ──
    ├── {slug}-linkedin-v1.md       #   Post draft (iterated)
    └── archive/                    #   Previous post versions
```

> **Legacy note:** The mindset-agent-launch blog project (2026-01) was created before this standard. It has the blog markdown at the project root (→ `blog/`), `images/` (→ `diagrams/`), and flat `context/` without `sources/`/`gold/` subdirs. Existing projects will not be restructured.

### 4.4 Image Project Structure

```
projects/{personal|professional}/{category}/YYYY-MM-{slug}/
├── project.yaml                    # type: image, theme: <any theme>
│
├── context/                        # ── PHASE 1: BRIEF ──
│   ├── sources/                    #   Reference materials
│   │   └── (user files)            #     Docs, existing visuals, references
│   ├── gold/                       #   Agreed approach
│   │   └── brief-v1.md             #     What to create, style, composition
│   └── prompts/                    #   Saved AI prompts
│
└── images/                         # ── PHASE 2: VISUALS ──
    ├── architecture-overview.html
    ├── system-diagram.html
    ├── screenshots/                #   Auto-generated PNGs (cstudio)
    └── archive/                    #   Previous versions
```

### 4.5 Why Blog + Diagrams + Video = One Project

A blog post, its diagrams, and its demo video are a single creative effort:
- The **diagrams** are created FOR the blog — they visualize concepts from the blog text
- The **demo video script** is written FROM the blog — the blog + diagrams become context for the script
- The **context** materials serve all three — architecture docs inform the blog, which informs the diagrams, which inform the script

Splitting them into separate projects would create unnecessary cross-referencing and lose the natural lifecycle: write blog → create diagrams → record demo.

---

## 5. Library Organization

### 5.1 Themes

Themes define the **visual identity** of content. Each theme provides CSS, templates, and documentation. **Theme is a project-level choice** — any project can use any theme.

| Theme | Visual Identity | Key Elements |
|-------|----------------|-------------|
| `sacred-gold` | Dark, reverent, warm | Gold accent `rgba(218,165,32,0.9)`, Cormorant Garamond + Montserrat, dark layered background with noise |
| `clean-slate` | Light, technical, clean | Off-white canvas (`#F8FAFC`), white cards with shadows, teal/cyan/purple accents, Space Grotesk + DM Sans, subtle border |

**Current usage:** sacred-gold for OCIA presentations, clean-slate for blog diagrams. But this is convention, not constraint — a professional presentation could use clean-slate, and the architecture supports adding new themes.

**Each theme provides a `theme-base.css`** that extracts the CSS common to all content using that theme:
- Reset rules (`*`, `body`)
- Canvas/container sizing and background
- Background treatment (noise texture for dark themes, border for light themes)
- Font imports

This eliminates CSS duplication across content files, just as `sacred-gold/theme-base.css` eliminated ~960 lines of duplication across presentation slides.

> **History:** The original `library/themes/agentic-mindset/` directory (variables.css, theme.md, templates) was aspirational documentation that no HTML file ever linked to. It was removed in Phase 1.5. The clean-slate theme was extracted from the **actual inline CSS in the blog diagram HTML files** — the source of truth for the diagram visual identity.

### 5.2 Standards

Standards define **rules and patterns** that Claude follows when creating content. They're organized by content type:

```
library/creative-dna/
├── core/                   # Shared across ALL content types
│   ├── dimensions.md       #   1280x720 canvas, 16:9 ratio
│   ├── builds.md          #   Build animation system (data-build, keyboard nav)
│   ├── builds.js          #   Universal build JS (used by slides AND diagrams)
│   └── file-naming.md     #   Naming conventions for all project types
│
├── slides/                 # Presentation-specific
│   ├── slide-standards.md #   Title alignment (left), font sizes, layout rules
│   ├── slide-template.html #  Generic slide template
│   └── components/        #   Reusable CSS (header.css, card.css, etc.)
│
├── diagrams/               # Diagram-specific
│   ├── diagram-standards.md  # Title alignment (centered), gradient text, flow direction
│   ├── diagram-template.html # Generic diagram template (links clean-slate)
│   └── components/        #   Reusable CSS (header.css, nodes.css, connectors.css, etc.)
│
├── writing/                # Writing standards for all written artifacts
│   ├── blog-style-guide.md           # Blog voice, structure, editing process
│   ├── presentation-deck-style-guide.md  # Narrative architecture, slide composition patterns, outline conventions
│   ├── demo-script-style-guide.md    # Demo video script structure, narration techniques
│   ├── talk-track-style-guide.md     # Presentation talk track voice, structure, delivery
│   └── reference-blogs/              # Published blogs as voice exemplars
│       └── (markdown versions)       #   Claude reads these to calibrate voice
│
└── videos/                 # Video production standards
    └── video-standards.md  # Recording, editing, export settings (Camtasia)
```

**Key insight:** Writing standards are not themes — they don't define visual CSS. They define **how Claude should write** when creating content. They sit alongside visual standards because they serve the same purpose: rules that Claude follows to produce consistent, high-quality output. Each written artifact type has its own style guide: `blog-style-guide.md`, `presentation-deck-style-guide.md`, `demo-script-style-guide.md`, and `talk-track-style-guide.md`.

**Reference blogs** live under `writing/reference-blogs/` alongside the style guide, since they are voice exemplars tightly coupled to the blog writing conventions. Claude reads `blog-style-guide.md` for rules and references published blogs for voice consistency and structural patterns.

---

## 6. Project Configuration: `project.yaml`

### 6.1 Presentation Project

```yaml
# projects/personal/ocia/2026-03-reconciliation/project.yaml

name: "The Sacrament of Reconciliation"
type: presentation
theme: sacred-gold
date: 2026-03-08

# Phase 1: Gold Context
gold:
  outline: context/gold/reconciliation-outline-v4.md

# Phase 2: Slides
slides_dir: slides
screenshots_dir: slides/screenshots
slides:
  - slide-01-title.html
  - slide-02-the-big-three.html
  - slide-03-the-question.html
  # ... (ordered list of all slides)

# Phase 2: Talk Track
talk_track:
  file: talk-track/reconciliation-talk-track-v4.md
  tts_script: talk-track/reconciliation-tts-script.txt

# Audio Narration (Phase 4 — ElevenLabs)
audio:
  voice_id: null
  output_dir: talk-track/audio/

# Google Slides (Phase 2)
google:
  presentation_id: null
  drive_folder_id: "1F5cTtZeld0cM3CLDLvAdeYAUMjPsjmhZ"
  presentation_title: "Reconciliation - Generated"
  slide_mapping: null

# Exports
exports_dir: exports
```

> **Legacy note:** The reconciliation project currently has `audio.voice` and `audio.style` (early placeholders), `outline/` at root instead of `context/gold/`, and `final-preso/` instead of `exports/`. When Phase 4 (ElevenLabs) is implemented, audio fields will be standardized to `voice_id` and `output_dir` as shown above.

### 6.2 Blog Project

```yaml
# projects/professional/blogs/2026-01-mindset-agent-launch/project.yaml

name: "Launching Agentic Mindset"
type: blog
theme: clean-slate
date: 2026-01-30

# Phase 1: Gold Context
gold:
  outline: context/gold/mindset-agent-outline-v3.md

# Phase 2: Blog
blog:
  file: blog/mindset-agent-blog-v4.md
  published_url: "https://agenticmindset.ai/blog/launching-agentic-mindset-..."

# Phase 2: Diagrams
diagrams_dir: diagrams
screenshots_dir: diagrams/screenshots
slides:
  - architecture-overview-light.html
  - first-class-citizen-pillars-light.html
  - embedding-pipeline-light.html
  - streaming-context-pipeline-light.html

# Phase 2: Demo Video
demo_video:
  script: demo-video/demo-script-v1.md
  published_url: "https://youtu.be/p302Vvq-PWs"

# Phase 2: LinkedIn Post
linkedin_post:
  file: linkedin-post/mindset-agent-linkedin-v1.md
  published_url: "https://www.linkedin.com/posts/..."
```

**How directory fields and `slides:` work together:**

The `project.yaml` has two related but distinct concepts:

1. **Directory field** — tells the CLI *where* HTML files live on disk. The field name is type-specific for semantic clarity:
   - `slides_dir` (presentations) — default: `slides`
   - `diagrams_dir` (blogs) — default: `diagrams`
   - `images_dir` (images) — default: `images`

2. **`slides:` list** — tells the CLI *which* HTML files to process (and in what order). This is always called `slides:` regardless of project type, because `cstudio screenshot` processes the list identically for all types.

The CLI resolves the correct directory field based on `type`, then looks for the files listed in `slides:` within that directory. Internally, config.py exposes a single `content_dir` path — the type-specific resolution is transparent to the screenshot engine.

### 6.3 Image Project

```yaml
# projects/professional/images/2026-02-readme-diagrams/project.yaml

name: "Project README Diagrams"
type: image
theme: clean-slate
date: 2026-02-15

# Phase 2: Images
images_dir: images
screenshots_dir: images/screenshots
slides:
  - architecture-overview.html
  - system-diagram.html
  - deployment-flow.html
```

**Note:** Image projects are lightweight — no gold context, blog, or talk track sections needed. Just the HTML files and their screenshots.

### 6.4 Config Field Reference

**Core fields (all project types):**

| Field | Required | Type | Description |
|-------|----------|------|-------------|
| `name` | Yes | string | Human-readable project name |
| `type` | Yes | `presentation` \| `blog` \| `image` | Project type — drives directory resolution and skill loading |
| `theme` | Yes | string | Theme directory name in `library/themes/` |
| `date` | No | date | Project date (e.g., `2026-03-08`) |
| `slides` | Yes | list | Ordered list of HTML files to process — always called `slides:` regardless of type |
| `screenshots_dir` | No | string | Directory for generated PNGs |

**Gold context (all project types, Claude-consumed):**

| Field | Required | Type | Description |
|-------|----------|------|-------------|
| `gold.outline` | No | string | Path to the current outline — the Phase 1 gold context artifact |

**Type-specific directory fields** (CLI resolves based on `type`):

| Field | Project Type | Default | Description |
|-------|-------------|---------|-------------|
| `slides_dir` | `presentation` | `slides` | Directory containing slide HTML files |
| `diagrams_dir` | `blog` | `diagrams` | Directory containing diagram HTML files |
| `images_dir` | `image` | `images` | Directory containing visual HTML files |

**Talk track (presentation projects):**

| Field | Required | Type | Description |
|-------|----------|------|-------------|
| `talk_track.file` | No | string | Path to the current talk track markdown |
| `talk_track.tts_script` | No | string | Path to the plain text TTS input file |

**Blog metadata (blog projects):**

| Field | Required | Type | Description |
|-------|----------|------|-------------|
| `blog.file` | No | string | Blog markdown file path (e.g., `blog/mindset-agent-blog-v4.md`) |
| `blog.published_url` | No | string | Published blog URL |
| `demo_video.script` | No | string | Demo script file path |
| `demo_video.published_url` | No | string | Published video URL |

**Google Slides (presentation projects, Phase 2):**

| Field | Required | Type | Description |
|-------|----------|------|-------------|
| `google.presentation_id` | No | string | Auto-set by `cstudio publish` — the Google Slides presentation ID |
| `google.drive_folder_id` | No | string | Google Drive folder for screenshots and deck. If null when `/publish` is invoked, the skill prompts for a Drive folder URL and extracts the ID automatically |
| `google.presentation_title` | No | string | Deck title (defaults to `name`) |
| `google.slide_mapping` | No | list | Auto-generated by `cstudio publish` — maps HTML slides to Google Slide pages with build states (see Section 9.1) |

**Exports (presentation projects, Phase 2):**

| Field | Required | Type | Description |
|-------|----------|------|-------------|
| `exports_dir` | No | string | Directory for exported files (PDF of deck, etc.) |

**Audio narration (presentation projects, Phase 4):**

| Field | Required | Type | Description |
|-------|----------|------|-------------|
| `audio.voice_id` | No | string | ElevenLabs voice identifier |
| `audio.output_dir` | No | string | Directory for generated MP3 files (default: `talk-track/audio/`) |

---

## 7. Theme & Standards Extraction

### 7.1 Sacred-Gold Theme Extraction (Complete)

**Status: Done** (Phase 0, completed for both Reconciliation and Beatitudes)

Extracted from 16 reconciliation slides + 24 beatitudes content slides:
- `library/themes/sacred-gold/theme-base.css` — reset, body, `.slide` background, noise texture
- `library/creative-dna/slides/components/header.css` — `.content`, `.title`, `.subtitle`, `.cross-accent`
- `library/creative-dna/slides/components/build-system.css` — `.build-item` animation
- `library/creative-dna/slides/components/typography.css` — standard text classes (sizes, weights, families)
- `library/themes/sacred-gold/typography-colors.css` — theme-specific text colors for typography classes
- `library/creative-dna/slides/components/two-column.css` — two-column layout
- `library/creative-dna/core/builds.js` — universal keyboard navigation + `showBuild()`

Typography uses a standard/theme split: `typography.css` defines structural properties (font-family, size, weight) shared across all themes, while each theme provides its own `typography-colors.css` with appropriate text colors.

**Result:** ~3,900 lines of duplicated CSS eliminated across 39 slides, plus ~88 redundant `font-family` declarations removed via typography standardization.

### 7.2 Clean-Slate Theme Extraction (In Progress)

**Status: Partially complete** (Phase 1.5)

Clean-slate is a **light-only theme** extracted from the actual inline CSS in the 4 blog diagram HTML files — the same "build first, extract second" approach used for sacred-gold.

**What's done:**
- `library/themes/agentic-mindset/` removed (aspirational docs that no HTML ever linked to)
- `library/themes/clean-slate/theme-base.css` extracted with: :root variables, reset, body, `.diagram` container (1280×720, off-white `#F8FAFC`, subtle purple/cyan glows at 6%, border), fade-only build animations, Google Fonts import
- `library/creative-dna/diagrams/components/header.css` created (gradient title, centered layout)
- `library/creative-dna/diagrams/diagram-template.html` updated to link clean-slate theme
- All 4 blog diagrams refactored to use shared `theme-base.css` and `builds.js` (inline duplication eliminated)
- Dark diagram variant (`architecture-overview.html`) removed (unused)

**What remains:**
- `library/themes/clean-slate/theme.md` — theme documentation (to create)
- Rename blog project's `images/` directory to `diagrams/` (see migration note below)
- Fix blog `project.yaml` to use `diagrams_dir: diagrams` instead of `slides_dir: images`
- Update `config.py` to resolve type-specific directory fields

> **Migration note:** The existing blog project at `projects/professional/blogs/2026-01-mindset-agent-launch/` uses `images/` for its diagram directory. This predates the design decision to use `diagrams/`. The directory needs to be renamed to `diagrams/` and the `project.yaml` updated to use `diagrams_dir: diagrams`. All internal `<link>` paths in the 4 diagram HTML files remain unchanged (same directory depth).

### 7.3 Shared Foundations

Both themes share the same build system and canvas dimensions:

| Shared Asset | File | Used By |
|---|---|---|
| Build animation CSS (slides) | `library/creative-dna/slides/components/build-system.css` | Presentation slides — fade + translateY(20px) |
| Build animation CSS (diagrams) | `library/themes/clean-slate/theme-base.css` | Blog diagrams — fade-only (opacity 0→1, no translate) |
| Build keyboard JS | `library/creative-dna/core/builds.js` | Both slides and diagrams |
| Canvas dimensions | 1280×720px, 16:9 | Both |

**Build animation difference (resolved):** Slide builds use `translateY(20px)` + fade. Diagram builds use opacity-only fade (no vertical movement). This is handled by having the fade-only animation in `clean-slate/theme-base.css` and the translate animation in `slides/components/build-system.css`. There is no separate `diagrams/components/build-system.css` — it's not needed.

---

## 8. Architecture

### 8.1 Three-Layer Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     USER / CLAUDE CODE                       │
│                                                              │
│   Natural language: "Update slide 5 in Google Slides"        │
│   Skill invocation: /sync 5                                  │
│                                                              │
├──────────────────────────────────────────────────────────────┤
│  SKILLS (Orchestration)            .claude/skills/           │
│                                                              │
│  SKILL.md files that teach Claude:                           │
│  • When to use each workflow                                 │
│  • Multi-step orchestration logic                            │
│  • Error handling and recovery                               │
│  • Which tools to auto-approve                               │
│  • Dynamic context injection (!`cstudio status`)             │
│                                                              │
│  User-invocable:                                             │
│    /screenshot, /publish, /sync, /image, /narrate,           │
│    /new-project, /add-youtube, /add-webpage                  │
│                                                              │
│  Auto-loaded (Claude invokes when relevant):                 │
│    slide-conventions, diagram-conventions,                    │
│    blog-writing, video-script                                │
│                                                              │
├──────────────────────────────────────────────────────────────┤
│  CLI (Execution)                   tools/cstudio/            │
│                                                              │
│  Python commands that do the actual work:                    │
│  • cstudio screenshot    • cstudio publish                   │
│  • cstudio sync          • cstudio image                     │
│  • cstudio audio         • cstudio init                      │
│  • cstudio status                                            │
│                                                              │
├──────────────────────────────────────────────────────────────┤
│  APIs (External Services)                                    │
│                                                              │
│  • Google Slides API     • Google Drive API                  │
│  • Gemini API            • ElevenLabs API                    │
│  • Selenium (Chrome)                                         │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

### 8.2 Skills Inventory

**User-invocable skills** (user types `/name`):

| Skill | Phase | What It Does |
|-------|-------|-------------|
| `/screenshot` | 1 (done) | Screenshots slides or diagrams via `cstudio screenshot` |
| `/new-project` | 1 (done) | Scaffolds a new project via `cstudio init` |
| `/publish` | 2 (done) | Creates Google Slides deck from all screenshots. Prompts for Drive folder URL if `drive_folder_id` is null |
| `/sync` | 2 (done) | Updates specific slides in existing Google Slides deck |
| `/image` | 3 | Generates image from external prompt file via Gemini API. Supports per-slide iteration loop |
| `/narrate` | 4 | Generates audio narration via ElevenLabs TTS |
| `/add-youtube` | 1.5 | Extracts YouTube transcript → `context/sources/transcripts/` |
| `/add-webpage` | 1.5 | Extracts web page content → `context/sources/web/` |
| `/export` | 2 (done) | Exports Google Slides deck as PDF → `exports/` |
| `/projects` | 2 (done) | Lists all projects and switches to selected one. Enables fast session resume |

**Auto-loaded skills** (Claude loads when relevant):

Auto-loaded skills trigger based on **project type** (from `project.yaml`) + **file pattern**:

| Project Type | File Being Edited | Skill Loaded | What Claude Gets |
|---|---|---|---|
| `presentation` | Any `*.html` slide file | `slide-conventions` | Slide layout rules, component CSS paths, build patterns, Google Slides workflow |
| `presentation` | `*outline*.md` | `outline-writing` | Narrative architecture, slide composition patterns (A-J), outline document conventions |
| `presentation` | Talk track markdown | `talk-track-writing` | Talk track voice, structure, delivery style, emotional calibration, formatting |
| `blog` | `*.html` diagram file | `diagram-conventions` | Flow direction rules, node colors, gradient titles, diagram layout patterns |
| `blog` | `*blog*.md` | `blog-writing` | Voice rules, structure patterns, editing process, reference blog links |
| `blog` | `*script*.md` or `*demo*.md` | `video-script` | Script structure, narration techniques, timing rules |
| `blog` | `linkedin-post/*.md` | `linkedin-writing` | Post categories, hook patterns, named pattern rules, Build Post template, closing signature |
| `image` | `*.html` visual file | `diagram-conventions` | Same diagram rules as blog diagrams (flow direction, node colors, layout) |

The project type disambiguates which rules to load for HTML files — presentations have different conventions than diagrams (title alignment, build animation style, component library). Writing standards load based on file naming patterns within blog and presentation projects. Image projects share `diagram-conventions` with blog diagrams since the visual standards are the same.

### 8.3 CLI Commands

```bash
# ── Project Management ──
cstudio init <path> --theme <name> [--type presentation|blog|image]
cstudio status                          # Show project state
cstudio projects                        # List all projects in the repo

# ── Screenshots (works for slides AND diagrams) ──
cstudio screenshot                      # All content in current project
cstudio screenshot slide-05             # One specific file
cstudio screenshot --slide 5            # By position in order list

# ── Context Gathering ──
cstudio scrape <url> -o <path>          # Extract webpage content via headless Chrome
cstudio transcribe <youtube-url> -o <path>  # Download audio + Whisper transcription

# ── Google Slides (Phase 2 — working) ──
cstudio publish                         # Create NEW Google Slides deck
cstudio sync                            # Re-sync ALL slides
cstudio sync --slide 5                  # Update JUST slide 5
cstudio export                          # Export deck as PDF → exports/

# ── Image Generation (Phase 3 — planned) ──
cstudio image slide-04                  # Generate from prompt file linked in placeholder
cstudio image slide-04 --prompt "custom prompt"  # Override prompt inline
cstudio image slide-04 --quality high   # Higher-quality model

# ── Audio Narration (Phase 4 — planned) ──
cstudio audio                           # Generate from script
cstudio audio --list-voices             # Browse voices
```

### 8.4 Credential Management

Credentials live outside the repo, with the directory configurable via environment variable.

#### Configuration

The credential directory is resolved in this order:
1. `CSTUDIO_CREDENTIALS_DIR` environment variable (if set)
2. `.env` file in the repository root (loaded by `python-dotenv`)
3. Default: `~/.content-studio/`

**`.env` file (repo root, gitignored):**

```bash
# Content Studio credentials directory
# Points to the directory containing Google OAuth client secret and API keys
CSTUDIO_CREDENTIALS_DIR=/Users/you/path/to/credentials
```

This approach means:
- **No hardcoded paths** in source code (only a sensible default)
- **Portable** across machines (each developer sets their own `.env`)
- **Secure** — `.env` is gitignored, credentials never enter the repo
- **Simple** — `python-dotenv` is the only new dependency

#### Credential Directory Contents

```
$CSTUDIO_CREDENTIALS_DIR/     # (or ~/.content-studio/ by default)
├── client_secret*.json        # Google OAuth client secret (glob pattern — any matching file)
├── token.pickle               # Google OAuth token (auto-generated, auto-refreshed)
├── gemini.key                 # Gemini API key
└── elevenlabs.key             # ElevenLabs API key
```

**Google OAuth client secret:** Google's Cloud Console generates client secret files with long auto-generated names like `client_secret_672772065866-fenn9r7505lrv3vv8can9736nkj44f3p.apps.googleusercontent.com.json`. Rather than requiring the user to rename this file, `cstudio` uses a glob pattern (`client_secret*.json`) to find any matching file in the credential directory. If multiple files match, it uses the first one found and logs a warning.

**Token caching:** `token.pickle` is auto-generated on first OAuth flow and auto-refreshed when expired. It's saved in the same credential directory as the client secret.

#### OAuth Scopes

| Scope | Purpose |
|-------|---------|
| `presentations` | Create and edit Google Slides presentations |
| `drive.file` | Upload screenshots to Drive, move files to folders, export as PDF |

The `drive.file` scope follows the principle of least privilege — it only grants access to files that the application itself creates, not the user's entire Drive. This is sufficient because `cstudio` creates the presentation and uploads the screenshots, so it inherently has access to move them into user-specified folders.

#### First-Time Setup

1. Create an OAuth 2.0 Client ID in Google Cloud Console (Desktop application type)
2. Enable the Google Slides API and Google Drive API
3. Download the client secret JSON file
4. Set `CSTUDIO_CREDENTIALS_DIR` in `.env` to point to the directory containing the downloaded file
5. On first `cstudio publish`, the OAuth flow opens a browser for authorization
6. The resulting `token.pickle` is cached — subsequent runs reuse it automatically

---

## 9. API Integrations

### 9.1 Google Slides API — Publish, Sync, and Export

The publish/sync workflow enables the iterate-one-slide pattern: edit HTML → `/sync 5` → only slide 5 updates in Google Slides.

#### Smart Folder ID Workflow

When `cstudio publish` is called and `google.drive_folder_id` is null in `project.yaml`, the CLI:

1. **Detects** the missing folder ID and raises a `PublishError` with a clear message
2. The `/publish` **skill** (orchestration layer) catches this and **prompts the user** for their Google Drive folder URL
3. The user pastes a URL like `https://drive.google.com/drive/folders/1HKrKNJuo0cmEDihz8RXxjuVZv8lS046x`
4. The skill **extracts the folder ID** from the URL using a regex (`/folders/([a-zA-Z0-9_-]+)`)
5. The skill **updates `project.yaml`** with the extracted folder ID
6. The skill **re-runs** `cstudio publish` — which now succeeds

This keeps the CLI simple (it just checks for null and fails fast) while the skill provides the interactive UX. The user never needs to manually find or paste folder IDs into YAML.

**URL patterns supported:**
- `https://drive.google.com/drive/folders/{id}`
- `https://drive.google.com/drive/folders/{id}?usp=sharing`
- `https://drive.google.com/drive/u/0/folders/{id}`

#### Slide Mapping

Each HTML slide with N builds produces N Google Slides pages (one per build state). After `cstudio publish`, the mapping is stored in `project.yaml`:

```yaml
google:
  presentation_id: "1abc..."
  drive_folder_id: "1HKr..."
  presentation_title: "Sin & Virtue - Generated"
  slide_mapping:
    - html_file: slide-01-title.html
      builds:
        - screenshot: slide-01-title-full.png
          slide_id: g_abc1
          image_id: img_abc1
    - html_file: slide-05-five-names.html
      builds:
        - screenshot: slide-05-five-names-build-0.png
          slide_id: g_abc5
          image_id: img_abc5
        - screenshot: slide-05-five-names-build-1.png
          slide_id: g_abc6
          image_id: img_abc6
```

The mapping is a **list of entries** (one per HTML slide), each containing a **list of builds** (one per Google Slides page). Each build tracks:
- `screenshot` — the PNG filename (for reference)
- `slide_id` — the Google Slides page object ID (used for deletion and positioning)
- `image_id` — the image element ID on that page (used for in-place image replacement)

#### `cstudio sync --slide 5` flow

1. Re-screenshot just slide 5 (all build states)
2. Upload new PNGs to Drive
3. **Same build count** → replace images in-place on existing Google Slides (fast, no reordering)
4. **Build count changed** → delete old Google Slides, insert new ones at the same position
5. Update the mapping with new image/slide IDs
6. Save updated mapping to `project.yaml`

#### `cstudio export` flow

1. Load `presentation_id` from `project.yaml`
2. Call Google Drive API to export as PDF
3. Save to `{exports_dir}/{slug}-deck.pdf`

### 9.2 Gemini Image Generation API

**SDK:** `google-genai` (current SDK)

**Models** (configurable via `.env`, with hardcoded fallbacks):
- `gemini-2.5-flash-image` — fast, free tier friendly (default for `--quality standard`)
- `gemini-3-pro-image-preview` — higher quality, text rendering (default for `--quality high`)

Model selection is centralized — configured via `CSTUDIO_IMAGE_MODEL_STANDARD` and `CSTUDIO_IMAGE_MODEL_HIGH` environment variables in `.env`. Prompt files do not specify models. Users control quality tier conversationally through Lumen (which passes `--quality standard|high` to the CLI).

#### 9.2.1 Core Design: Externalized Prompts

Image generation prompts are **external files**, not inline HTML text. This is because:
- Real prompts are 30–60+ lines with detailed style, composition, and content instructions
- Prompts need iteration (v1, v2, v3...) with full git history
- The same placeholder dimensions should work with different prompt versions
- Prompt editing shouldn't require touching slide HTML

**Prompt files** live alongside generated images:

```
slides/
├── slide-03-question-v3.html
├── images/
│   ├── slide-03-books-collage.png          ← generated image
│   └── prompts/
│       ├── slide-03-books-collage-v1.md    ← first attempt
│       └── slide-03-books-collage-v2.md    ← final prompt
├── screenshots/
```

For blog diagrams: `diagrams/images/prompts/`. For image projects: `images/prompts/`.

**Prompt file format** — YAML frontmatter + prompt body:

```markdown
---
aspect_ratio: "9:16"
---

Create a realistic photograph of popular self-help and happiness books
arranged in an OVERLAPPING COLLAGE on a cork board background. Portrait
orientation (9:16 aspect ratio for vertical placement).

CRITICAL ARRANGEMENT STYLE:
- Books should be PILED and OVERLAPPING each other...

[full detailed prompt continues]
```

Frontmatter fields:

- `aspect_ratio` — Gemini API aspect ratio (default: `16:9`). Common values: `16:9`, `9:16`, `1:1`, `4:3`, `3:4`
- `size` — desired pixel dimensions (informational only)

Model is **not** specified in prompt files. It is configured via `.env` (`CSTUDIO_IMAGE_MODEL_STANDARD`, `CSTUDIO_IMAGE_MODEL_HIGH`) and selected at runtime via `--quality standard|high`.

#### 9.2.2 HTML Placeholder Pattern

Placeholders in slide HTML serve two purposes: (1) visual hint while designing the slide layout, and (2) link to the external prompt file via `data-prompt`.

```html
<div class="image-placeholder" data-prompt="images/prompts/slide-03-books-collage-v2.md">
    <div class="placeholder-icon">📚</div>
    <div class="placeholder-text">
        <strong>IMAGE:</strong> Collage of popular self-help books<br><br>
        Suggestions: Atomic Habits, The Power of Now, 7 Habits, etc.
    </div>
</div>
```

- `data-prompt` — relative path (from the slide file) to the prompt file
- The inline text is a visual hint only — not used for generation when `data-prompt` is present
- If no `data-prompt` attribute, `cstudio image` falls back to the inline placeholder text (for simple one-liner images)

#### 9.2.3 Generation Flow

`cstudio image slide-03`:

1. Parse the slide HTML, find `.image-placeholder`
2. Read `data-prompt` attribute → load the prompt file
3. Parse YAML frontmatter for `aspect_ratio`
4. Call Gemini API with prompt body and aspect ratio
5. Save PNG to `images/` (e.g., `slide-03-books-collage.png`)
6. Update slide HTML: replace the `<div class="image-placeholder">` with `<img src="images/...">`

#### 9.2.4 Per-Slide Image Iteration Workflow

Image generation happens as an **inner loop within slide creation**. The user builds a slide, gets the image right, then moves to the next slide. This is the core creative workflow:

**Step 1: Create the slide.** User asks Lumen to build the slide HTML with text, layout, and a placeholder positioned/sized where the image should go.

**Step 2: Draft the prompt.** Lumen drafts an initial prompt file based on the placeholder description and saves it to `images/prompts/slide-03-books-collage-v1.md`. User can review/edit before generating.

**Step 3: Generate.** `/image slide-03` → reads prompt file → calls Gemini → places image in slide → takes screenshot so user can see the result in context.

**Step 4: Iterate.** User gives feedback:
- **Content/style feedback** ("books too neat, need more overlap", "too dark") → Lumen updates the prompt file (saves as v2), regenerates, re-screenshots
- **Positioning/sizing feedback** ("shift it left", "make it smaller") → Lumen edits slide CSS only, re-screenshots (no regeneration)

**Step 5: Confirm.** User approves. Move to next slide.

Example conversation flow:

```
User:   Generate the image for slide 3, let's see what we get.
Lumen:  [generates, screenshots] Here's the result. Books are in a neat grid.
User:   Too organized. Pile them on top of each other, chaotic, on a cork board.
        Make it portrait 9:16.
Lumen:  [updates prompt v2, regenerates] Better — overlapping on cork board now.
User:   Add Ikigai and Man's Search for Meaning. Make titles legible.
Lumen:  [updates prompt v3, regenerates] All 12 books, titles readable.
User:   That's the image. But shrink it in the slide and add padding.
Lumen:  [edits CSS only, re-screenshots] Adjusted. Here's the updated slide.
User:   Perfect. Let's move to slide 4.
```

The `/image` skill orchestrates this loop: it knows to screenshot after generating, to version prompt files on iteration, and to distinguish content feedback (regenerate) from layout feedback (CSS edit only).

### 9.3 ElevenLabs TTS

**Why not Camtasia Audiate?** Audiate has zero programmatic access (no CLI, no API, no SDK).

**ElevenLabs flow:** Read script text → call TTS API → save MP3. Generated MP3s can be imported into Audiate for manual polish if needed.

---

## 10. Claude Code Integration

### 10.1 Primary Workspace: VS Code + Claude Code

VS Code handles the entire workflow for all content types:

| Workflow Phase | Presentations | Blogs + Diagrams | Images | Demo Videos |
|---|---|---|---|---|
| Context gathering | `/add-youtube`, `/add-webpage`, drop files | Same | Same | Read blog + demo flow |
| Content creation | HTML slides with builds | Markdown blog + HTML diagrams | HTML visuals | Script markdown |
| Visual generation | `/image` (Gemini) — per-slide iteration loop | HTML diagram creation | HTML visual creation | N/A (Camtasia) |
| Screenshot | `/screenshot` (Selenium) | `/screenshot` (Selenium) | `/screenshot` (Selenium) | N/A |
| Publishing | `/publish`, `/sync` (Google Slides API) | Manual (WordPress/Medium) | Manual (copy PNGs) | Manual (YouTube) |
| Talk track/script | Conversational (auto: `talk-track-writing`) | N/A | N/A | Conversational (auto: `video-script`) |
| Audio | `/narrate` (ElevenLabs) | N/A | N/A | Camtasia recording |

### 10.2 Auto-Loaded Skills — Context-Aware Assistance

When Claude detects you're working on a specific content type, it automatically loads the relevant skill. The trigger is **project type** (from `project.yaml`) + **file pattern**:

| Project Type | You're Editing | Claude Auto-Loads | What Claude Gets |
|---|---|---|---|
| `presentation` | Any slide HTML | `slide-conventions` | Slide layout rules, component CSS, build patterns |
| `presentation` | Outline markdown | `outline-writing` | Narrative architecture, slide composition patterns (A-J), outline document conventions |
| `presentation` | Talk track markdown | `talk-track-writing` | Talk track voice, structure, delivery style, emotional calibration, formatting |
| `blog` | Any diagram HTML | `diagram-conventions` | Flow direction, node colors, gradient titles, card patterns |
| `blog` | Blog markdown | `blog-writing` | Voice rules, structure patterns, editing process, reference blogs |
| `blog` | Demo script markdown | `video-script` | Narration techniques, section structure, timing rules |
| `image` | Any visual HTML | `diagram-conventions` | Same diagram conventions (shared with blog diagrams) |

This means Claude always has the right rules loaded for the content type being created — without the user needing to explicitly request them. The project type is critical: both presentations and diagrams are HTML files, but they follow different conventions (title alignment, build animation style, layout patterns). Image projects reuse `diagram-conventions` since they share the same visual standards as blog diagrams. The `outline-writing` skill loads the presentation deck style guide — covering George's narrative architecture, slide composition patterns (A-J), outline document conventions, and the "foundation before feelings" principle. The `talk-track-writing` skill loads the comprehensive talk track style guide — covering George's presentation voice, the universal talk track architecture (Hook→Framework→Activity→Demo→Climax→Closing), vulnerability guidelines, emotional calibration, and formatting standards.

---

## 11. Acceptance Tests

### 11.1 Presentation Pipeline (Reconciliation Project)

| # | Test | Pass Condition |
|---|------|---------------|
| 1 | Project config | `project.yaml` with all 16 slides, theme, Google IDs |
| 2 | Screenshots | `cstudio screenshot` generates 45 PNGs at 2560x1440 |
| 3 | Skills work | `/screenshot`, `/publish`, `/sync` invoke CLI with no approval prompts |
| 4 | Publish | `cstudio publish` creates Google Slides deck with full-bleed slides |
| 5 | Single-slide update | Edit slide-02 HTML → `/sync 2` → only slide 2 updated |
| 6 | Build count change | Add build to slide-09 → `/sync 9` → new Google Slide inserted |
| 7 | Image generation | `/image 4` → reads prompt file → Gemini API → image placed in HTML → screenshot |
| 8 | Audio narration | `/narrate` → MP3 from talk track TTS script |
| 9 | Talk track skill | Claude auto-loads `talk-track-writing` when editing talk track markdown |
| 10 | Export | `/export` → PDF saved to `exports/` via Google Drive API |
| 11 | Natural language | "Update slide 5" → Claude auto-loads sync skill → correct execution |
| 12 | Full E2E | Outline + context → complete deck with talk track + audio + PDF |

### 11.2 Blog Pipeline (Mindset Agent Launch Project)

| # | Test | Pass Condition |
|---|------|---------------|
| 1 | Project config | `project.yaml` with 4 light diagrams, theme, published URLs |
| 2 | Screenshots | `cstudio screenshot` generates PNG for each diagram |
| 3 | Blog writing skill | Claude auto-loads `blog-writing` when editing blog markdown |
| 4 | Diagram skill | Claude auto-loads `diagram-conventions` when editing diagram HTML |
| 5 | Video script skill | Claude auto-loads `video-script` when editing demo script |
| 6 | Theme extraction | Diagrams link to shared clean-slate `theme-base.css`, no inline duplication |

### 11.3 Image Pipeline

| # | Test | Pass Condition |
|---|------|---------------|
| 1 | Project config | `project.yaml` with type `image`, theme, and HTML visual list |
| 2 | Screenshots | `cstudio screenshot` generates PNG for each visual |
| 3 | Diagram skill | Claude auto-loads `diagram-conventions` when editing visual HTML |
| 4 | Init scaffolding | `cstudio init --type image` creates correct directory structure |

### 11.4 Context Gathering (All Project Types)

| # | Test | Pass Condition |
|---|------|---------------|
| 1 | YouTube extraction | `/add-youtube <url>` → transcript saved to `context/sources/transcripts/` |
| 2 | Webpage extraction | `/add-webpage <url>` → content saved to `context/sources/web/` |
| 3 | Directory structure | Typed subfolders created automatically; user files stay flat in `sources/` |
| 4 | Context reading | Claude reads all sources in `context/sources/` and summarizes |

---

## 12. Implementation Plan

### Phase Overview

```
Phase 0 ──► Phase 1 ──► Phase 1.5 ──► Phase 2 ──────► Phase 5
(Restructure) (Foundation)  (Multi-      (Google Slides) (Integration
               ✓             Content)          │          + Blog)
                                          Phase 3 ──────┤
                                          (Gemini)      │
                                                        │
                                          Phase 4 ──────┘
                                          (Audio)
```

| Phase | Goal | Status |
|-------|------|--------|
| **Phase 0** | Directory restructure + sacred-gold theme extraction | **Complete** |
| **Phase 1** | CLI + Skills + Project Config + Screenshot | **Complete** |
| **Phase 1.5** | Multi-content support: clean-slate theme extraction, remove agentic-mindset directory, blog + image project config, style guide organization, reference blogs, auto-loaded skills, context gathering skills (`/add-youtube`, `/add-webpage`) | **In Progress** — most tasks done, config.py type-specific dir resolution + blog directory rename remaining |
| **Phase 2** | Google Slides publish + sync + export, credential management (.env), smart folder ID workflow, `/projects` session resume | **In Progress** — initial implementation complete (gslides.py, publish.py, CLI wiring, skills, `/projects`), credential management and folder ID improvements in design review |
| **Phase 3** | Gemini image generation — externalized prompts, per-slide iteration loop, `/image` skill | Planned |
| **Phase 4** | ElevenLabs audio narration | Planned |
| **Phase 5** | Integration, documentation, blog post | Planned |

See `implementation-guide.md` for detailed task breakdowns.

---

## 13. Key Design Decisions

### Multi-Content-Type Architecture

**Decision:** One project structure, one CLI, multiple content types — rather than separate tools per content type.

**Rationale:** All content types share the same foundation:
- 1280×720 HTML canvas with builds
- `cstudio screenshot` for visual capture
- `project.yaml` for configuration
- Skills for Claude Code orchestration

The differences (theme, title alignment, build defaults) are handled by the theme system and project type field, not by separate tools.

### Blog + Diagrams + Video = One Project

**Decision:** Keep blog, diagrams, and demo video in a single project directory.

**Rationale:** They share a lifecycle (blog → diagrams → video). The blog content becomes context for the diagrams. The blog + diagrams become context for the video script. Splitting them would create unnecessary cross-project references.

### Theme Is a Project-Level Choice (Not a Content-Type Binding)

**Decision:** Theme is set per project in `project.yaml`, not hardcoded to content types. Any project can use any theme.

**Rationale:** Sacred-gold is currently used for OCIA presentations, clean-slate for blog diagrams. But a professional conference presentation could use clean-slate. Binding themes to content types would create artificial constraints. The project configuration should be the single place where theme is chosen.

### Style Guides as Standards (Not Themes)

**Decision:** Blog writing style guide and demo video script guide live in `library/creative-dna/writing/` and `library/creative-dna/videos/`, not in themes.

**Rationale:** Style guides define how Claude *writes*, not how content *looks*. They're analogous to visual standards (`slide-standards.md`, `diagram-standards.md`) but for textual content. Themes define CSS and visual identity; standards define rules and patterns.

### Skills + CLI (Three-Layer Architecture)

**Decision:** Skills (orchestration) → CLI (execution) → APIs (external services). No custom MCP servers.

**Rationale:** Skills provide workflow intelligence (when to act, what steps, error handling). The CLI provides execution muscle. Together they deliver better UX than MCP servers with less code. See `design-decisions-and-learnings.md` for detailed analysis.

### Screenshots-as-Images for Google Slides

**Decision:** Render HTML → screenshot → full-bleed image in Google Slides.

**Rationale:** Pixel-perfect reproduction. Full CSS power. 2x retina (2560x1440) is sharp on any display.

### All Visual Content Uses the Same Tooling

**Decision:** `cstudio screenshot` processes presentation slides, blog diagrams, and standalone image visuals. All are listed as `slides:` in `project.yaml`.

**Rationale:** All three are 1280×720 HTML files with build animations and keyboard navigation. There's no technical reason for separate tooling. The CLI uses `slides_dir`, `diagrams_dir`, or `images_dir` to find the files, and `slides:` to know which files to process. The `type` field in `project.yaml` drives which auto-loaded skill (and therefore which conventions) apply.

### Style Guide Completeness Principle

**Decision:** Every key creative deliverable that Claude Code produces must have a corresponding **style guide** and **auto-loaded skill**. If the agent produces it, the agent should know how to produce it *your way*.

**The complete deliverable → style guide → skill map:**

| Deliverable | Style Guide | Auto-Loaded Skill | Triggers When |
|---|---|---|---|
| Blog post (.md) | `blog-style-guide.md` | `blog-writing` | Editing blog markdown |
| LinkedIn post (.md) | `linkedin-post-style-guide.md` | `linkedin-writing` | Editing linkedin-post markdown in blog projects |
| Demo script (.md) | `demo-script-style-guide.md` | `video-script` | Editing demo script markdown |
| Talk track (.md) | `talk-track-style-guide.md` | `talk-track-writing` | Editing talk track markdown |
| Presentation outline (.md) | `presentation-deck-style-guide.md` | `outline-writing` | Editing outline markdown in presentation projects |
| Slide HTML (.html) | `slide-standards.md` | `slide-conventions` | Editing slide HTML in presentation projects |
| Diagram HTML (.html) | `diagram-standards.md` | `diagram-conventions` | Editing diagram HTML in blog/image projects |

**Rationale:** Style guides capture the creator's voice and structural preferences — narrative architecture, slide composition patterns, the "foundation before feelings" principle, the reframe technique. Without an auto-loaded skill, Claude writes using generic best practices instead of the creator's specific patterns. The difference is the difference between "an AI wrote this" and "this sounds like me."

This principle was discovered during Phase 1 testing when the presentation outline — arguably the most important Phase 1 output — had a style guide (`presentation-deck-style-guide.md`) but no auto-loaded skill. Claude was creating outlines without any context about the creator's narrative architecture, slide composition patterns (A-J), or outline document conventions.

**The two categories of style guides:**

| Category | Naming Pattern | What It Teaches |
|---|---|---|
| **Content creation** (writing prose) | `{thing}-writing` | Voice, narrative structure, emotional arc |
| **Technical implementation** (building HTML) | `{thing}-conventions` | Layout, CSS, theme rules, component patterns |

**Coupled but distinct guides:** The `presentation-deck-style-guide.md` (the architect — story structure, slide content) and `talk-track-style-guide.md` (the performer — delivery voice, pacing) are tightly coupled but serve different phases. The outline is consumed by both: slide creation reads it for content/layout decisions, talk track creation reads it for spoken key points and transitions.

---

## 14. API Keys & Costs

| Service | Purpose | Cost | Status |
|---------|---------|------|--------|
| Google Slides API | Create/update decks | Free | Enabled — OAuth client "Claude Content Studio" configured |
| Google Drive API | Upload screenshots, export PDF | Free | Enabled — same OAuth client |
| Gemini API | Image generation | Free tier (~5-10 images/deck) | Needs setup |
| ElevenLabs | Audio narration | Free tier or $5/month | Needs setup |
| Claude Code (Max) | AI-powered content creation | Already paying | Active |
| **Total** | | **$0–$5/month** | |

---

## 15. Open Questions

1. **Voice cloning:** Record samples for a custom ElevenLabs clone of George's voice?
2. **Speaker notes:** Auto-populate Google Slides speaker notes from talk track?
3. **Blog publishing automation:** Could `cstudio` publish directly to WordPress via API?
4. **YouTube metadata:** Could `cstudio` generate YouTube descriptions with timestamps from demo scripts?
5. **Cross-project search:** Should `cstudio` support searching across all published blogs for reference?
