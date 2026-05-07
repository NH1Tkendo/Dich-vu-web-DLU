"""
POST /api/v1/process/{document_id}
Trigger OCR / formula extraction for a given document and save to database.
"""
import os
import uuid
from datetime import datetime, timezone

from fastapi import APIRouter, Path, HTTPException, status, Depends
from sqlalchemy.orm import Session

from app.schemas.formula import FormulaResponse
from app.core.config import settings
from app.core.database import get_db
from app.models import Document, FormulaEntry
from app.services.pdf_processor import extract_formula_images_from_pdf
from app.services.ocr_service import extract_latex_from_images

router = APIRouter(prefix="/process", tags=["process"])


@router.post(
    "/{document_id}",
    response_model=list[FormulaResponse],
    status_code=status.HTTP_200_OK,
    summary="Trigger formula extraction for a document",
)
async def process_document(
    document_id: uuid.UUID = Path(..., description="UUID of the target document"),
    db: Session = Depends(get_db),
) -> list[FormulaResponse]:
    """
    Invoke PyMuPDF + pix2tex OCR pipeline for the given document
    and save extracted formulas to database.
    """
    # Check if document exists
    doc = db.query(Document).filter(Document.id == document_id).first()
    if not doc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Document not found in database."
        )
    
    upload_dir = os.path.abspath(settings.UPLOAD_DIR)
    file_path = os.path.join(upload_dir, f"{document_id}.pdf")
    
    if not os.path.exists(file_path):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Document PDF not found on server."
        )
        
    try:
        # 1. Trích xuất ảnh từ PDF
        images = extract_formula_images_from_pdf(file_path)
        
        # 2. Đưa ảnh qua mô hình OCR pix2tex
        latex_results = extract_latex_from_images(images)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Processing failed: {str(e)}"
        )
    
    try:
        # 3. Delete old formulas for this document (if any)
        db.query(FormulaEntry).filter(
            FormulaEntry.document_id == document_id
        ).delete()
        
        # 4. Save extracted formulas to database
        responses = []
        now = datetime.now(timezone.utc)
        for idx, latex in enumerate(latex_results):
            formula_entry = FormulaEntry(
                id=uuid.uuid4(),
                document_id=document_id,
                latex_content=latex or r"\text{Model failed to extract formula}",
                status="pending",
                order_index=idx,
            )
            db.add(formula_entry)
            
            # Use 'now' since DB hasn't committed yet to provide a valid timestamp
            resp = FormulaResponse(
                id=formula_entry.id,
                document_id=formula_entry.document_id,
                raw_latex=formula_entry.latex_content,
                status=formula_entry.status,
                updated_at=now,
            )
            responses.append(resp)
        
        # Update document status to Processed
        doc.status = "Processed"
        db.commit()
        
        return responses
    except Exception as e:
        db.rollback()
        print(f"ERROR saving formulas: {str(e)}")  # In lỗi ra console để debug
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to save formulas to database: {str(e)}"
        )
