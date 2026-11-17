import re
import zipfile
import io
from fastapi import HTTPException, status
from app.core.config import settings

# Magic byte signatures
PDF_MAGIC = b"%PDF-"
DOCX_ZIP_MAGIC = b"PK\x03\x04"

ALLOWED_EXTENSIONS = {".pdf", ".docx"}


def sanitize_text(text: str) -> str:
    """
    Sanitize untrusted text extracted from files or user inputs:
    - Strips dangerous null bytes
    - Escapes/strips HTML script tags and javascript pseudo-protocols
    - Normalizes excessive whitespace
    """
    if not text:
        return ""

    # Remove null bytes
    cleaned = text.replace("\x00", "")

    # Strip script and dangerous tags
    cleaned = re.sub(r"<\s*script[^>]*>.*?<\s*/\s*script\s*>", "", cleaned, flags=re.IGNORECASE | re.DOTALL)
    cleaned = re.sub(r"<\s*iframe[^>]*>.*?<\s*/\s*iframe\s*>", "", cleaned, flags=re.IGNORECASE | re.DOTALL)
    cleaned = re.sub(r"javascript\s*:", "", cleaned, flags=re.IGNORECASE)

    return cleaned.strip()


def validate_file_content(filename: str, content: bytes) -> str:
    """
    Inspects file extension, file size, and magic byte signatures to prevent
    untrusted or malicious file execution.
    Returns: 'pdf' or 'docx'
    Raises: HTTPException 400 on validation failure
    """
    if not filename or "." not in filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File has no name or extension."
        )

    ext = "." + filename.rsplit(".", 1)[-1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported file format '{ext}'. Only .pdf and .docx are supported."
        )

    # Size validation
    max_bytes = settings.MAX_UPLOAD_SIZE_MB * 1024 * 1024
    if len(content) > max_bytes:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File exceeds maximum allowed size of {settings.MAX_UPLOAD_SIZE_MB}MB."
        )

    if len(content) < 32:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Uploaded file is too small or empty."
        )

    # Magic byte verification
    if ext == ".pdf":
        if not content.startswith(PDF_MAGIC):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid PDF file. Header signature does not match PDF specification."
            )
        return "pdf"

    elif ext == ".docx":
        if not content.startswith(DOCX_ZIP_MAGIC):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid DOCX file. File is not a valid OpenXML ZIP archive."
            )
        # Deep inspection of zip archive structure to ensure word/document.xml exists
        try:
            with zipfile.ZipFile(io.BytesIO(content)) as z:
                names = z.namelist()
                if "word/document.xml" not in names:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Corrupted DOCX archive. Missing required word/document.xml structure."
                    )
        except zipfile.BadZipFile:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Corrupted DOCX archive. Failed to decompress."
            )
        return "docx"

    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Unsupported file format."
    )
