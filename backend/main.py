
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from .workflow import graph
from .config import MAX_CHARS
from .models import AnalysisResponse
from .services.document_io import extract_text_from_upload
from .services.analyzer import analyze_text

app = FastAPI(title="AI Document Analyzer (MVP)")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/analyze", response_model=AnalysisResponse)
async def analyze_document(file: UploadFile = File(...)):
    text = await extract_text_from_upload(file)
    result = analyze_text(text)
    
    return AnalysisResponse(**result)
