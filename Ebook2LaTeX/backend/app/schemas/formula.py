"""
Pydantic schemas for the FormulaEntry resource.
"""
import uuid
from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict

FormulaStatus = Literal["pending", "reviewed", "submitted"]


# --------------------------------------------------------------------------- #
# Request schemas
# --------------------------------------------------------------------------- #
class FormulaUpdate(BaseModel):
    raw_latex: str
    status: FormulaStatus | None = None


class FormulaBatchUpdate(BaseModel):
    formulas: list["FormulaUpdateItem"]


class FormulaUpdateItem(BaseModel):
    id: uuid.UUID
    raw_latex: str
    status: FormulaStatus | None = None


# --------------------------------------------------------------------------- #
# Response schemas
# --------------------------------------------------------------------------- #
class FormulaResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    document_id: uuid.UUID
    raw_latex: str
    status: str
    updated_at: datetime


class PaginatedFormulaResponse(BaseModel):
    total: int
    page: int
    page_size: int
    items: list[FormulaResponse]


class BatchUpdateResponse(BaseModel):
    success: bool
    updated_count: int
