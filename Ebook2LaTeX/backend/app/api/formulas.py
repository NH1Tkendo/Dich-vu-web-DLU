"""
Formulas router – GET / PUT / POST (batch) endpoints.
Manages formula entries in the database.
"""
import uuid
from datetime import datetime, timezone

from fastapi import APIRouter, Path, Query, status, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models import FormulaEntry, Document
from app.schemas.formula import (
    BatchUpdateResponse,
    FormulaBatchUpdate,
    FormulaResponse,
    FormulaUpdate,
    PaginatedFormulaResponse,
)

router = APIRouter(prefix="/formulas", tags=["formulas"])


# ---------------------------------------------------------------------------
# GET /formulas/{document_id}
# ---------------------------------------------------------------------------
@router.get(
    "/{document_id}",
    response_model=PaginatedFormulaResponse,
    summary="List formulas for a document (paginated)",
)
async def list_formulas(
    document_id: uuid.UUID = Path(...),
    page: int = Query(1, ge=1, description="Page number (1-indexed)"),
    page_size: int = Query(10, ge=1, le=100, description="Items per page"),
    db: Session = Depends(get_db),
) -> PaginatedFormulaResponse:
    """
    Return paginated formula entries for a document from database.
    """
    # Verify document exists
    doc = db.query(Document).filter(Document.id == document_id).first()
    if not doc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )
    
    # Query formulas with pagination
    query = db.query(FormulaEntry).filter(
        FormulaEntry.document_id == document_id
    ).order_by(FormulaEntry.order_index)
    
    total = query.count()
    start = (page - 1) * page_size
    items = query.offset(start).limit(page_size).all()
    
    return PaginatedFormulaResponse(
        total=total,
        page=page,
        page_size=page_size,
        items=[
            FormulaResponse(
                id=item.id,
                document_id=item.document_id,
                raw_latex=item.latex_content,
                status=item.status,
                updated_at=item.updated_at,
            )
            for item in items
        ],
    )


# ---------------------------------------------------------------------------
# PUT /formulas/{formula_id}
# ---------------------------------------------------------------------------
@router.put(
    "/{formula_id}",
    response_model=FormulaResponse,
    summary="Update a single formula's LaTeX content",
)
async def update_formula(
    payload: FormulaUpdate,
    formula_id: uuid.UUID = Path(...),
    db: Session = Depends(get_db),
) -> FormulaResponse:
    """
    Update `raw_latex` (and optionally `status`) for a single formula.
    """
    formula = db.query(FormulaEntry).filter(FormulaEntry.id == formula_id).first()
    if not formula:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Formula not found"
        )
    
    try:
        formula.latex_content = payload.raw_latex
        if payload.status:
            formula.status = payload.status
        formula.updated_at = datetime.now(tz=timezone.utc)
        db.commit()
        db.refresh(formula)
        
        return FormulaResponse(
            id=formula.id,
            document_id=formula.document_id,
            raw_latex=formula.latex_content,
            status=formula.status,
            updated_at=formula.updated_at,
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update formula: {str(e)}"
        )


# ---------------------------------------------------------------------------
# POST /formulas/batch
# ---------------------------------------------------------------------------
@router.post(
    "/batch",
    response_model=BatchUpdateResponse,
    status_code=status.HTTP_200_OK,
    summary="Batch-update multiple formulas (final submit)",
)
async def batch_update_formulas(
    payload: FormulaBatchUpdate,
    db: Session = Depends(get_db),
) -> BatchUpdateResponse:
    """
    Apply a batch of formula updates atomically to database.
    """
    updated = 0
    try:
        for item in payload.formulas:
            formula = db.query(FormulaEntry).filter(
                FormulaEntry.id == item.id
            ).first()
            
            if formula:
                formula.latex_content = item.raw_latex
                if item.status:
                    formula.status = item.status
                formula.updated_at = datetime.now(tz=timezone.utc)
                updated += 1
        
        db.commit()
        return BatchUpdateResponse(success=True, updated_count=updated)
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Batch update failed: {str(e)}"
        )
