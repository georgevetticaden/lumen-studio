# Video Standards

Standards for creating demo videos with Camtasia and associated scripts.

## Script Format

Scripts are written in Markdown with clear structure for recording.

### Script File Naming

- Single script: `script.md`
- Multi-part: `script-{section}.md`
  - `script-intro.md`
  - `script-demo.md`
  - `script-conclusion.md`

### Script Structure

```markdown
# Video Title

## Overview
- Duration target: X minutes
- Audience: [description]
- Key takeaway: [one sentence]

---

## Section 1: Introduction

### Visual
[Description of what's on screen]

### Script
[Exact words to speak]

### Notes
- [Recording notes]
- [Emphasis points]

---

## Section 2: Demo

### Visual
[Screen recording of application]

### Script
[Narration text]

### Actions
1. Click on [element]
2. Type [text]
3. Wait for [result]

---

## Section 3: Conclusion

### Visual
[Final slide or summary screen]

### Script
[Closing remarks]

### Call to Action
[What viewer should do next]
```

## Video Assets

### File Naming

- Recordings: `recording-{section}.mp4`
- Exports: `{project-name}-final.mp4`
- B-roll: `broll-{description}.mp4`
- Audio: `voiceover-{section}.mp3`

### Resolution

- **1920×1080** (1080p) - Standard export
- **3840×2160** (4K) - High quality master

## Camtasia Projects

### Project Structure

```
YYYY-MM-{project}/
├── script.md              # Recording script
├── assets/
│   ├── slides/            # HTML slides for video
│   ├── diagrams/          # Diagrams to include
│   └── audio/             # Music, sound effects
├── recordings/
│   ├── screen-capture/    # Raw screen recordings
│   └── camera/            # Webcam footage
├── exports/
│   └── {project}-final.mp4
└── project.tscproj        # Camtasia project file
```

### Recording Checklist

- [ ] Script finalized
- [ ] Screen resolution set (1920×1080)
- [ ] Notifications disabled
- [ ] Desktop cleaned
- [ ] Browser tabs closed
- [ ] Audio levels checked
- [ ] Recording area defined

## Slides for Video

Use HTML slides for intro/outro and key points:

1. Create slides using theme templates
2. Press `End` to show all builds
3. Import screenshot into Camtasia
4. Or record slide with builds as video

## Best Practices

### Script Writing
- Write conversationally (speak, don't read)
- Short sentences (15 words max)
- One idea per sentence
- Include pauses: [pause]
- Mark emphasis: **emphasized word**

### Recording
- Record in sections (easier to edit)
- Leave 2 seconds silence at start/end
- Speak slightly slower than normal
- Use consistent microphone position
- Record in quiet environment

### Editing
- Cut dead air (keep <0.5s pauses)
- Add zoom for UI details
- Use callouts for mouse clicks
- Add captions for accessibility
- Include intro/outro slides

## Duration Guidelines

| Content Type | Target Duration |
|--------------|-----------------|
| Quick tip | 1-2 minutes |
| Feature demo | 3-5 minutes |
| Tutorial | 8-15 minutes |
| Deep dive | 20-30 minutes |

## Export Settings

### YouTube/General
- Format: MP4
- Resolution: 1920×1080
- Frame rate: 30 fps
- Audio: AAC 192kbps

### High Quality Master
- Format: MP4
- Resolution: 3840×2160
- Frame rate: 60 fps
- Audio: AAC 320kbps
