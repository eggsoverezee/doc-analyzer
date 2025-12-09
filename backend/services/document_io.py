from io import BytesIO

from fastapi import UploadFile, HTTPException
from pypdf import PdfReader

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