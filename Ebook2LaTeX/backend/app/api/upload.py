"""
POST /api/v1/upload
Upload a PDF file and return document metadata (mock in Phase 1).
"""
import os
import uuid
from datetime import datetime, timezone

from fastapi import APIRouter, File, HTTPException, UploadFile, status

from app.core.config import settings
from app.schemas.document import DocumentResponse

router = APIRouter(prefix="/upload", tags=["upload"])


@router.post(
    "",
    response_model=DocumentResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Upload a PDF document",
)
async def upload_document(
    file: UploadFile = File(..., description="PDF file to upload"),
) -> DocumentResponse:
    """
    Accept a PDF file upload and save it locally.
    """
    if file.content_type not in ("application/pdf",):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error_code": "INVALID_FILE_TYPE",
                "message": "Only PDF files are accepted.",
            },
        )

    content = await file.read()
    if len(content) > settings.MAX_UPLOAD_SIZE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error_code": "FILE_TOO_LARGE",
                "message": f"File exceeds the maximum allowed size of {settings.MAX_UPLOAD_SIZE // (1024 * 1024)} MB.",
            },
        )

    # --- Save file locally ---
    doc_id = uuid.uuid4()
    upload_dir = os.path.abspath(settings.UPLOAD_DIR)
    os.makedirs(upload_dir, exist_ok=True)
    
    file_path = os.path.join(upload_dir, f"{doc_id}.pdf")
    with open(file_path, "wb") as f:
        f.write(content)

    return DocumentResponse(
        id=doc_id,
        filename=file.filename or "unnamed.pdf",
        created_at=datetime.now(tz=timezone.utc),
    )
