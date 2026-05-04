"""
Pydantic schemas for the Document resource.
"""
import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict


# --------------------------------------------------------------------------- #
# Request schemas
# --------------------------------------------------------------------------- #
class DocumentCreate(BaseModel):
    filename: str


# --------------------------------------------------------------------------- #
# Response schemas
# --------------------------------------------------------------------------- #
class DocumentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    filename: str
    created_at: datetime
