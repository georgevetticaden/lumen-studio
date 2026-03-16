---
description: Auto-loaded reference for blog post writing conventions
user-invocable: false
---

# Blog Writing Conventions

This skill provides voice and style conventions to follow when writing or editing blog posts.

## Style Guide

Read the full style guide at: `library/creative-dna/writing/blog-style-guide.md`

Key rules:
- **Tone:** Conversational yet authoritative
- **Lead:** Start with a real-world scenario, not theory
- **Structure:** Problem → approach → implementation → learnings
- **Code blocks:** Include real code with comments, not pseudocode
- **Length:** 2000-3000 words for deep dives, 800-1200 for quick posts

## Reference Blogs

Before writing, read reference exemplars for voice and rhythm:
- `library/creative-dna/writing/reference-blogs/` — published posts that demonstrate the target voice

The style guide is the grammar. The reference blogs are the accent.

## Blog Project Structure

Blog projects use `type: blog` in `project.yaml`:

```
YYYY-MM-{slug}/
├── project.yaml          # type: blog, theme: clean-slate
├── {blog-post}.md        # Blog content
├── images/               # Diagrams (HTML → PNG)
│   ├── {diagram}.html
│   ├── screenshots/      # Generated PNGs
│   └── archive/          # Old versions
├── demo-video/           # Script + assets
└── context/              # Source materials
    ├── sources/
    └── prompts/
```

## Diagram Integration

When a blog needs diagrams:
1. Create HTML diagrams in `images/` using the clean-slate theme
2. Run `/screenshot` to generate PNGs
3. Reference PNGs in the blog markdown

## DO NOT

- Write generic introductions ("In today's world...")
- Use passive voice excessively
- Include code without context or explanation
- Skip the "why" — always explain the reasoning behind decisions
