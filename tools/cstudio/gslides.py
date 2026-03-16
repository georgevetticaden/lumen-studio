"""Google Slides and Drive API operations.

Provides functions for creating presentations, uploading screenshots,
managing slides, and exporting to PDF. All operations use the credentials
from utils.load_google_credentials().
"""

import io
from pathlib import Path

import structlog

from cstudio.exceptions import PublishError
from cstudio.utils import SLIDE_HEIGHT_EMU, SLIDE_WIDTH_EMU, load_google_credentials

log = structlog.get_logger()


# ── API service builders ─────────────────────────────────────────────────────


def _build_services():
    """Build Google Slides and Drive API service objects.

    Returns (slides_service, drive_service) tuple.
    """
    from googleapiclient.discovery import build

    creds = load_google_credentials()
    slides_service = build("slides", "v1", credentials=creds)
    drive_service = build("drive", "v3", credentials=creds)
    return slides_service, drive_service


def _build_slides_service():
    """Build Google Slides API service only."""
    from googleapiclient.discovery import build

    creds = load_google_credentials()
    return build("slides", "v1", credentials=creds)


def _build_drive_service():
    """Build Google Drive API service only."""
    from googleapiclient.discovery import build

    creds = load_google_credentials()
    return build("drive", "v3", credentials=creds)


# ── Presentation management ─────────────────────────────────────────────────


def create_presentation(title: str, folder_id: str | None = None) -> str:
    """Create a blank Google Slides presentation.

    Args:
        title: Presentation title.
        folder_id: Optional Google Drive folder ID to move the deck into.

    Returns:
        The presentation ID.
    """
    slides_svc, drive_svc = _build_services()

    # Create blank presentation with correct page size
    body = {
        "title": title,
        "pageSize": {
            "width": {"magnitude": SLIDE_WIDTH_EMU, "unit": "EMU"},
            "height": {"magnitude": SLIDE_HEIGHT_EMU, "unit": "EMU"},
        },
    }
    presentation = slides_svc.presentations().create(body=body).execute()
    presentation_id = presentation["presentationId"]
    log.info("[GSLIDES] created presentation", id=presentation_id, title=title)

    # Delete the default blank slide
    default_slides = presentation.get("slides", [])
    if default_slides:
        default_id = default_slides[0]["objectId"]
        slides_svc.presentations().batchUpdate(
            presentationId=presentation_id,
            body={"requests": [{"deleteObject": {"objectId": default_id}}]},
        ).execute()
        log.debug("[GSLIDES] deleted default blank slide")

    # Move to folder if specified
    if folder_id:
        try:
            # Get current parents to remove
            file_meta = (
                drive_svc.files()
                .get(fileId=presentation_id, fields="parents")
                .execute()
            )
            previous_parents = ",".join(file_meta.get("parents", []))
            drive_svc.files().update(
                fileId=presentation_id,
                addParents=folder_id,
                removeParents=previous_parents,
                fields="id, parents",
            ).execute()
            log.info("[GSLIDES] moved to folder", folder_id=folder_id)
        except Exception as e:
            log.warning("[GSLIDES] failed to move to folder", error=str(e))

    return presentation_id


# ── Screenshot upload ────────────────────────────────────────────────────────


def upload_screenshot(
    file_path: Path, folder_id: str | None = None
) -> str:
    """Upload a PNG screenshot to Google Drive and make it publicly readable.

    Args:
        file_path: Path to the PNG file.
        folder_id: Optional Drive folder ID.

    Returns:
        The public URL for the uploaded image.
    """
    from googleapiclient.http import MediaFileUpload

    drive_svc = _build_drive_service()

    file_metadata = {"name": file_path.name, "mimeType": "image/png"}
    if folder_id:
        file_metadata["parents"] = [folder_id]

    media = MediaFileUpload(str(file_path), mimetype="image/png")
    uploaded = (
        drive_svc.files()
        .create(body=file_metadata, media_body=media, fields="id, webContentLink")
        .execute()
    )
    file_id = uploaded["id"]

    # Make publicly readable (required for Slides image insertion)
    drive_svc.permissions().create(
        fileId=file_id,
        body={"type": "anyone", "role": "reader"},
        fields="id",
    ).execute()

    # Build direct-access URL
    image_url = f"https://drive.google.com/uc?id={file_id}"
    log.debug("[GSLIDES] uploaded screenshot", file=file_path.name, id=file_id)
    return image_url


# ── Slide operations ─────────────────────────────────────────────────────────


def add_slides(
    presentation_id: str,
    image_urls: list[str],
    insert_at: int | None = None,
) -> list[dict]:
    """Add slides with full-bleed images to a presentation.

    Each image_url becomes one slide with the image covering the entire
    slide area (10" x 5.625" at EMU dimensions).

    Args:
        presentation_id: Google Slides presentation ID.
        image_urls: List of publicly accessible image URLs.
        insert_at: Optional 0-based index to insert slides at.
                   If None, appends to the end.

    Returns:
        List of dicts with 'slide_id' and 'image_id' for each created slide.
    """
    import uuid

    slides_svc = _build_slides_service()

    requests = []
    slide_info = []

    for i, url in enumerate(image_urls):
        slide_id = f"slide_{uuid.uuid4().hex[:12]}"
        image_id = f"image_{uuid.uuid4().hex[:12]}"

        # Create blank slide
        create_req = {
            "createSlide": {
                "objectId": slide_id,
                "slideLayoutReference": {"predefinedLayout": "BLANK"},
            }
        }

        # Insert at specific position if requested
        if insert_at is not None:
            create_req["createSlide"]["insertionIndex"] = insert_at + i

        requests.append(create_req)

        # Add full-bleed image
        requests.append(
            {
                "createImage": {
                    "objectId": image_id,
                    "url": url,
                    "elementProperties": {
                        "pageObjectId": slide_id,
                        "size": {
                            "width": {
                                "magnitude": SLIDE_WIDTH_EMU,
                                "unit": "EMU",
                            },
                            "height": {
                                "magnitude": SLIDE_HEIGHT_EMU,
                                "unit": "EMU",
                            },
                        },
                        "transform": {
                            "scaleX": 1,
                            "scaleY": 1,
                            "translateX": 0,
                            "translateY": 0,
                            "unit": "EMU",
                        },
                    },
                }
            }
        )

        slide_info.append({"slide_id": slide_id, "image_id": image_id})

    if requests:
        slides_svc.presentations().batchUpdate(
            presentationId=presentation_id, body={"requests": requests}
        ).execute()

    log.info(
        "[GSLIDES] added slides",
        count=len(image_urls),
        insert_at=insert_at,
    )
    return slide_info


def replace_slide_image(
    presentation_id: str,
    slide_id: str,
    old_image_id: str,
    new_image_url: str,
) -> str:
    """Replace the image on an existing slide.

    Deletes the old image and creates a new full-bleed image.

    Args:
        presentation_id: Google Slides presentation ID.
        slide_id: The page/slide object ID.
        old_image_id: The existing image object ID to delete.
        new_image_url: URL of the replacement image.

    Returns:
        The new image object ID.
    """
    import uuid

    slides_svc = _build_slides_service()
    new_image_id = f"image_{uuid.uuid4().hex[:12]}"

    requests = [
        # Delete old image
        {"deleteObject": {"objectId": old_image_id}},
        # Create new full-bleed image
        {
            "createImage": {
                "objectId": new_image_id,
                "url": new_image_url,
                "elementProperties": {
                    "pageObjectId": slide_id,
                    "size": {
                        "width": {"magnitude": SLIDE_WIDTH_EMU, "unit": "EMU"},
                        "height": {"magnitude": SLIDE_HEIGHT_EMU, "unit": "EMU"},
                    },
                    "transform": {
                        "scaleX": 1,
                        "scaleY": 1,
                        "translateX": 0,
                        "translateY": 0,
                        "unit": "EMU",
                    },
                },
            }
        },
    ]

    slides_svc.presentations().batchUpdate(
        presentationId=presentation_id, body={"requests": requests}
    ).execute()

    log.debug(
        "[GSLIDES] replaced image",
        slide_id=slide_id,
        old_image=old_image_id,
        new_image=new_image_id,
    )
    return new_image_id


def delete_slides(presentation_id: str, slide_ids: list[str]) -> None:
    """Delete slides from a presentation.

    Args:
        presentation_id: Google Slides presentation ID.
        slide_ids: List of slide object IDs to delete.
    """
    if not slide_ids:
        return

    slides_svc = _build_slides_service()

    requests = [{"deleteObject": {"objectId": sid}} for sid in slide_ids]
    slides_svc.presentations().batchUpdate(
        presentationId=presentation_id, body={"requests": requests}
    ).execute()

    log.info("[GSLIDES] deleted slides", count=len(slide_ids))


def get_slide_index(presentation_id: str, slide_id: str) -> int:
    """Get the 0-based index of a slide in the presentation.

    Args:
        presentation_id: Google Slides presentation ID.
        slide_id: The slide object ID to find.

    Returns:
        0-based index of the slide.

    Raises:
        PublishError if slide not found.
    """
    slides_svc = _build_slides_service()
    presentation = (
        slides_svc.presentations()
        .get(presentationId=presentation_id)
        .execute()
    )
    for i, slide in enumerate(presentation.get("slides", [])):
        if slide["objectId"] == slide_id:
            return i
    raise PublishError(f"Slide {slide_id} not found in presentation {presentation_id}")


# ── Export ───────────────────────────────────────────────────────────────────


def export_as_pdf(presentation_id: str, output_path: Path) -> Path:
    """Export a Google Slides presentation as PDF.

    Args:
        presentation_id: Google Slides presentation ID.
        output_path: Local path to save the PDF.

    Returns:
        The output path.
    """
    drive_svc = _build_drive_service()

    request = drive_svc.files().export(
        fileId=presentation_id, mimeType="application/pdf"
    )
    pdf_data = request.execute()

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_bytes(pdf_data)

    log.info(
        "[GSLIDES] exported PDF",
        path=str(output_path),
        size_kb=len(pdf_data) // 1024,
    )
    return output_path
