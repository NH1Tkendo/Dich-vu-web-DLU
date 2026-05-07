"""
POST /api/v1/upload
Upload a PDF file and save document to database.
"""
import os
import uuid
from datetime import datetime, timezone

from fastapi import APIRouter, File, HTTPException, UploadFile, status, Depends
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import get_db
from app.models import Document
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
    db: Session = Depends(get_db),
) -> DocumentResponse:
    """
    Accept a PDF file upload, save it locally, and store metadata in database.
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

    # --- Save document metadata to database ---
    try:
        db_document = Document(
            id=doc_id,
            file_name=file.filename or "unnamed.pdf",
            file_path_url=file_path,
            status="Pending",  # Status: Pending, Processed, Error
        )
        db.add(db_document)
        db.commit()
        db.refresh(db_document)
        
        return DocumentResponse(
            id=db_document.id,
            filename=db_document.file_name,
            created_at=db_document.upload_date,
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to save document to database: {str(e)}"
        )
