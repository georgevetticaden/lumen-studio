"""Audio transcription engine — download YouTube audio and transcribe with Whisper.

Uses yt-dlp to download audio and OpenAI Whisper for local transcription.
Handles videos where YouTube captions are disabled.
"""

import os
import re
import subprocess
import tempfile
import time
from pathlib import Path

import structlog

log = structlog.get_logger()


def get_video_info(url: str) -> dict:
    """Get video title and duration via yt-dlp."""
    result = subprocess.run(
        ["python3", "-m", "yt_dlp", "--print", "title", "--print", "duration_string", url],
        capture_output=True,
        text=True,
    )
    lines = result.stdout.strip().split("\n")
    return {
        "title": lines[0] if lines else "Unknown",
        "duration": lines[1] if len(lines) > 1 else "Unknown",
    }


def download_audio(url: str, output_dir: str | None = None) -> Path:
    """Download audio track from YouTube as mp3.

    Returns path to the downloaded mp3 file.
    """
    if output_dir is None:
        output_dir = tempfile.mkdtemp(prefix="cstudio-audio-")

    output_template = os.path.join(output_dir, "audio.%(ext)s")

    log.info("[TRANSCRIBE] downloading audio", url=url)
    result = subprocess.run(
        [
            "python3", "-m", "yt_dlp",
            "-x",
            "--audio-format", "mp3",
            "--audio-quality", "5",
            "-o", output_template,
            url,
        ],
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        raise RuntimeError(f"yt-dlp failed: {result.stderr}")

    mp3_path = Path(output_dir) / "audio.mp3"
    if not mp3_path.exists():
        raise RuntimeError(f"Expected audio file not found: {mp3_path}")

    size_mb = mp3_path.stat().st_size / (1024 * 1024)
    log.info("[TRANSCRIBE] audio downloaded", size_mb=f"{size_mb:.1f}")
    return mp3_path


def transcribe_audio(audio_path: Path, model_name: str = "base") -> dict:
    """Transcribe audio file using OpenAI Whisper.

    Args:
        audio_path: Path to mp3/wav file.
        model_name: Whisper model size (tiny, base, small, medium, large).
                    base = good balance of speed and accuracy.

    Returns:
        dict with keys: text, language, segments
    """
    import whisper

    log.info("[TRANSCRIBE] loading model", model=model_name)
    model = whisper.load_model(model_name)

    log.info("[TRANSCRIBE] transcribing audio", path=str(audio_path))
    start = time.time()
    result = model.transcribe(str(audio_path))
    elapsed = time.time() - start

    text = result["text"].strip()
    word_count = len(text.split())

    log.info(
        "[TRANSCRIBE] complete",
        seconds=int(elapsed),
        words=word_count,
        language=result.get("language", "unknown"),
    )

    return {
        "text": text,
        "word_count": word_count,
        "language": result.get("language", "unknown"),
        "transcribe_seconds": int(elapsed),
    }


def transcribe_youtube(
    url: str, model_name: str = "base"
) -> dict:
    """Full pipeline: download YouTube audio → transcribe with Whisper.

    Returns dict with: title, duration, text, word_count, language, url
    """
    # Fix SSL cert issue on macOS
    try:
        import certifi
        os.environ.setdefault("SSL_CERT_FILE", certifi.where())
    except ImportError:
        pass

    info = get_video_info(url)
    log.info(
        "[TRANSCRIBE] starting",
        title=info["title"],
        duration=info["duration"],
    )

    audio_path = download_audio(url)
    try:
        result = transcribe_audio(audio_path, model_name)
    finally:
        # Clean up temp audio file
        audio_path.unlink(missing_ok=True)
        audio_path.parent.rmdir()

    return {
        "title": info["title"],
        "duration": info["duration"],
        "url": url,
        **result,
    }


def slugify(text: str, max_length: int = 60) -> str:
    """Convert text to a URL-friendly slug for filenames."""
    slug = text.lower()
    slug = re.sub(r"[^a-z0-9\s-]", "", slug)
    slug = re.sub(r"[\s_]+", "-", slug)
    slug = re.sub(r"-+", "-", slug).strip("-")
    if len(slug) > max_length:
        slug = slug[:max_length].rsplit("-", 1)[0]
    return slug or "transcript"
