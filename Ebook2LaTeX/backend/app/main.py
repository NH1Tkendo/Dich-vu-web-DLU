"""
FastAPI application entry point for Ebook2LaTeX.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import formulas, process, upload
from app.core.config import settings

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description=(
        "Convert math-heavy PDF ebooks to LaTeX by extracting formulas via "
        "PyMuPDF + pix2tex OCR and providing an interactive review editor."
    ),
    docs_url="/docs",
    redoc_url="/redoc",
)

# ---------------------------------------------------------------------------
# CORS Middleware
# ---------------------------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# API Routers – all mounted under /api/v1
# ---------------------------------------------------------------------------
API_PREFIX = "/api/v1"

app.include_router(upload.router, prefix=API_PREFIX)
app.include_router(process.router, prefix=API_PREFIX)
app.include_router(formulas.router, prefix=API_PREFIX)


# ---------------------------------------------------------------------------
# Health check
# ---------------------------------------------------------------------------
@app.get("/health", tags=["health"], summary="Health check")
async def health() -> dict:
    return {"status": "ok", "version": settings.APP_VERSION}
