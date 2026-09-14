from dataclasses import dataclass


SUPPORTED_TYPES = {
    "image/png": b"\x89PNG\r\n\x1a\n",
    "image/jpeg": b"\xff\xd8\xff",
    "image/webp": b"RIFF",
}


@dataclass(frozen=True)
class ImageValidation:
    valid: bool
    error: str | None = None


def validate_image(content_type: str | None, content: bytes, max_bytes: int) -> ImageValidation:
    if content_type not in SUPPORTED_TYPES:
        return ImageValidation(False, "Only PNG, JPEG, and WebP screenshots are supported.")
    if not content:
        return ImageValidation(False, "The uploaded screenshot is empty.")
    if len(content) > max_bytes:
        return ImageValidation(False, f"The screenshot exceeds the {max_bytes} byte limit.")
    signature = SUPPORTED_TYPES[content_type]
    if not content.startswith(signature):
        return ImageValidation(False, "The file content does not match its declared image type.")
    if content_type == "image/webp" and content[8:12] != b"WEBP":
        return ImageValidation(False, "The file is not a valid WebP image.")
    return ImageValidation(True)
