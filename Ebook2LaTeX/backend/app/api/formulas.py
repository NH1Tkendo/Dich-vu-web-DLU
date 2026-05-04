"""
Formulas router – GET / PUT / POST (batch) endpoints.
All responses are mock data in Phase 1.
"""
import uuid
from datetime import datetime, timezone

from fastapi import APIRouter, Path, Query, status

from app.schemas.formula import (
    BatchUpdateResponse,
    FormulaBatchUpdate,
    FormulaResponse,
    FormulaUpdate,
    PaginatedFormulaResponse,
)

router = APIRouter(prefix="/formulas", tags=["formulas"])

# ---------------------------------------------------------------------------
# In-memory mock store (Phase 1 only – replaced by DB in Phase 3+)
# ---------------------------------------------------------------------------
_MOCK_STORE: dict[str, FormulaResponse] = {}


def _seed_store(document_id: uuid.UUID) -> list[FormulaResponse]:
    """Lazily populate the mock store for a document_id."""
    now = datetime.now(tz=timezone.utc)
    seeds = [
        (uuid.uuid4(), r"a^2 + b^2 = c^2", "pending"),
        (uuid.uuid4(), r"\nabla \cdot \vec{E} = \frac{\rho}{\varepsilon_0}", "pending"),
        (uuid.uuid4(), r"F = G \frac{m_1 m_2}{r^2}", "reviewed"),
    ]
    entries = [
        FormulaResponse(
            id=fid,
            document_id=document_id,
            raw_latex=latex,
            status=st,
            updated_at=now,
        )
        for fid, latex, st in seeds
    ]
    for e in entries:
        _MOCK_STORE[str(e.id)] = e
    return entries


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
) -> PaginatedFormulaResponse:
    """
    Return paginated formula entries for a document.

    **Phase 1 – Mock:** Seeds 3 fake formulas if the store is empty.
    """
    # Seed if first call for this document
    if not _MOCK_STORE:
        _seed_store(document_id)

    all_items = list(_MOCK_STORE.values())
    start = (page - 1) * page_size
    end = start + page_size
    return PaginatedFormulaResponse(
        total=len(all_items),
        page=page,
        page_size=page_size,
        items=all_items[start:end],
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
) -> FormulaResponse:
    """
    Update `raw_latex` (and optionally `status`) for a single formula.

    **Phase 1 – Mock:** Updates the in-memory store.
    """
    key = str(formula_id)
    if key not in _MOCK_STORE:
        # Create a stub entry so the UI can still function
        _MOCK_STORE[key] = FormulaResponse(
            id=formula_id,
            document_id=uuid.uuid4(),
            raw_latex=payload.raw_latex,
            status=payload.status or "pending",
            updated_at=datetime.now(tz=timezone.utc),
        )
    else:
        existing = _MOCK_STORE[key]
        _MOCK_STORE[key] = existing.model_copy(
            update={
                "raw_latex": payload.raw_latex,
                "status": payload.status or existing.status,
                "updated_at": datetime.now(tz=timezone.utc),
            }
        )
    return _MOCK_STORE[key]


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
) -> BatchUpdateResponse:
    """
    Apply a batch of formula updates atomically.

    **Phase 1 – Mock:** Applies updates to the in-memory store and returns
    the count of affected records.
    """
    updated = 0
    now = datetime.now(tz=timezone.utc)
    for item in payload.formulas:
        key = str(item.id)
        if key in _MOCK_STORE:
            existing = _MOCK_STORE[key]
            _MOCK_STORE[key] = existing.model_copy(
                update={
                    "raw_latex": item.raw_latex,
                    "status": item.status or "submitted",
                    "updated_at": now,
                }
            )
        else:
            _MOCK_STORE[key] = FormulaResponse(
                id=item.id,
                document_id=uuid.uuid4(),
                raw_latex=item.raw_latex,
                status=item.status or "submitted",
                updated_at=now,
            )
        updated += 1

    return BatchUpdateResponse(success=True, updated_count=updated)
