---
description: Auto-loaded reference for demo video script writing conventions
user-invocable: false
---

# Video Script Conventions

This skill provides conventions to follow when writing or editing demo video scripts.

## Style Guide

Read the full style guide at: `library/creative-dna/writing/demo-script-style-guide.md`

Key rules:
- **Tone:** Conversational, as if explaining to a colleague
- **Sentences:** Short (15 words max), one idea per sentence
- **Pacing:** Include [pause] markers, mark **emphasis**
- **Structure:** Intro → demo → conclusion with clear visual/script separation

## Reference Demo Scripts

Before writing, read 2-3 reference scripts for voice, pacing, and structure:
- `library/creative-dna/writing/reference-demo-scripts/` — published demo scripts that demonstrate the target style

The style guide is the grammar. The reference scripts are the accent.

Available references (read the markdown versions first — they're easier to parse):
- `ios-to-android-migration-script-part1.md` / `part2.md` — Multi-day journey demo (Type D)
- `federal-form-automation-script-part1.md` / `part2.md` — Multi-phase architecture demo (Type C)
- `mindset-agent-script-v1.md` — Agent capability demo (Type A)

Select references that match the demo type you're writing. For example, if writing an agent capability demo, read the mindset agent script. If writing a multi-phase demo, read the federal form scripts.

## Video Standards

Read technical standards at: `library/creative-dna/videos/video-standards.md`

## Script Structure

```markdown
## Section N: Title

### Visual
[What's on screen]

### Script
[Exact words to speak]

### Actions
1. [Click/type/wait instructions]
```

## Script File Naming

- Single script: `script.md`
- Multi-part: `script-intro.md`, `script-demo.md`, `script-conclusion.md`

## Recording Checklist

Before recording:
- [ ] Script finalized and reviewed
- [ ] Screen resolution set (1920x1080)
- [ ] Notifications disabled
- [ ] Desktop cleaned
- [ ] Audio levels checked

## DO NOT

- Write long paragraphs (this is spoken, not read)
- Skip visual descriptions (editor needs them)
- Use jargon without first explaining it
- Include more than 3 actions per section
