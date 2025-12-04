
import os
from io import BytesIO

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pypdf import PdfReader

from .workflow import graph


app = FastAPI(title="AI Document Analyzer (MVP)")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class AnalysisResponse(BaseModel):
    summary: str
    metadata: dict


async def extract_text_from_upload(upload: UploadFile) -> str:
    filename = upload.filename or ""
    content = await upload.read()

    if not content:
        raise HTTPException(status_code=400, detail="Empty file uploaded.")

    if filename.lower().endswith(".pdf"):
        try:
            pdf_reader = PdfReader(BytesIO(content))
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() or ""
            return text
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Failed to extract PDF text: {e}")
    else:
        try:
            return content.decode("utf-8", errors="ignore")
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Failed to decode text file: {e}")


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/analyze", response_model=AnalysisResponse)
async def analyze_document(file: UploadFile = File(...)):
    text = await extract_text_from_upload(file)

    if len(text) > 8000:
        text = text[:8000]

    try:
        result_state = graph.invoke({"content": text})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Graph execution failed: {e}")

    return AnalysisResponse(
        summary=result_state.get("summary", ""),
        metadata=result_state.get("metadata", {}),
    )
