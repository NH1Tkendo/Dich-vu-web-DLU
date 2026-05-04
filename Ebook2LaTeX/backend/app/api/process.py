"""
POST /api/v1/process/{document_id}
Trigger OCR / formula extraction for a given document (mock in Phase 1).
"""
import os
import uuid
from datetime import datetime, timezone

from fastapi import APIRouter, Path, HTTPException, status

from app.schemas.formula import FormulaResponse
from app.core.config import settings
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
) -> list[FormulaResponse]:
    """
    Invoke PyMuPDF + pix2tex OCR pipeline for the given document.
    """
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
        
    # Tạo response và lưu tạm vào mock store (Phase 1)
    now = datetime.now(tz=timezone.utc)
    
    # Dùng _MOCK_STORE để lưu state tạm trong memory cho các API GET/PUT/Batch
    from app.api.formulas import _MOCK_STORE
    
    responses = []
    for idx, latex in enumerate(latex_results):
        f_id = uuid.uuid4()
        resp = FormulaResponse(
            id=f_id,
            document_id=document_id,
            raw_latex=latex or r"\text{Model failed to extract formula}",
            status="pending",
            updated_at=now,
        )
        responses.append(resp)
        _MOCK_STORE[str(f_id)] = resp
        
    return responses
