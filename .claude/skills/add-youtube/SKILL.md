---
description: Extract a YouTube video transcript and save it as context for the current project
user-invocable: true
allowed-tools:
  - Bash(python3 *)
  - Bash(curl *)
  - Read
  - Write
---

# Add YouTube Transcript

Extracts a YouTube video transcript and saves it as a context source for the current project.

## Usage

The user says something like "add this youtube video" or "/add-youtube https://youtube.com/watch?v=..."

## Steps

### 1. Extract the video ID from the URL

Supports formats:
- `https://www.youtube.com/watch?v=VIDEO_ID`
- `https://youtu.be/VIDEO_ID`
- `https://youtube.com/watch?v=VIDEO_ID&t=123`

### 2. Get the video title first

Use curl to fetch the page title — this is needed for both the filename and the header:
```bash
curl -sL "https://www.youtube.com/watch?v=VIDEO_ID" -H "User-Agent: Mozilla/5.0" | sed -n 's/.*<title>\(.*\)<\/title>.*/\1/p' | sed 's/ - YouTube$//'
```

**IMPORTANT:** Do NOT use `grep -P` — it does not work on macOS. Use `sed` for text extraction.

### 3. Try YouTube captions first (fast)

```bash
python3 -m pip install -q youtube-transcript-api 2>/dev/null
python3 -c "
from youtube_transcript_api import YouTubeTranscriptApi
ytt = YouTubeTranscriptApi()
transcript = ytt.fetch('VIDEO_ID')
for snippet in transcript.snippets:
    print(snippet.text)
"
```

**IMPORTANT:** Always use `python3 -m pip`, never bare `pip` or `pip3`.

### 4. If captions are disabled — use Whisper transcription

If step 3 fails with `TranscriptsDisabled` or `NoTranscriptFound`, tell the user that captions aren't available and offer to transcribe with Whisper:

> "This video has captions disabled. I can transcribe the audio using Whisper — this downloads the audio track and runs local speech-to-text. It takes a few minutes for long videos. Want me to proceed?"

If the user agrees (or if they asked you to add the video, which implies yes):

```bash
python3 -m cstudio transcribe "YOUTUBE_URL" -o context/sources/transcripts/{slugified-title}.md
```

This command:
- Downloads the audio track via yt-dlp
- Transcribes with OpenAI Whisper (base model, runs locally)
- Saves as markdown with title, source URL, duration, and extraction date
- ~5 min for a 60-min video on Apple Silicon

**IMPORTANT:** Always use `python3 -m cstudio`, never bare `python` or `cstudio`.

### 5. Save with a descriptive filename

- Slugify the video title for the filename (lowercase, hyphens, no special chars)
- Example: `seven-deadly-sins-bishop-barron.md` (NOT `wG4VF0jU568.md`)
- Target directory: `context/sources/transcripts/`

If you used `cstudio transcribe -o`, the file is already saved. Otherwise save with the Write tool using this format:
```markdown
# YouTube Transcript: {Video Title}
Source: {full URL}
Extracted: {date}

---

{transcript text, joined into readable paragraphs}
```

### 6. Report results

- Video title
- File path
- Approximate word count
- Key themes (2-3 bullet points summarizing the content)
- If Whisper was used, note the transcription time

## Error Handling

- **No captions → use Whisper:** Don't give up — offer `cstudio transcribe` as the automatic fallback
- **Package not installed:** Install with `python3 -m pip install -q youtube-transcript-api`
- **Invalid URL:** Ask for a corrected URL
- **Whisper fails:** Check that `yt-dlp`, `openai-whisper`, and `ffmpeg` are installed
