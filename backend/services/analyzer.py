from fastapi import HTTPException

from ..config import MAX_CHARS
from ..workflow import graph

def analyze_text(text:str) -> dict:
    if not text:
        raise HTTPException(status_code=400, detail ="No text content extracted,")
    
    if len(text) > MAX_CHARS:
        text = text[:MAX_CHARS]

    try: 
        result_state = graph.invoke({"content": text})
    except Exception as e:
        raise HTTPException(status_code=500,detail=f"Graph execution failed: {e}",)
    
    return {
        "summary": result_state.get("summary", ""),
        "metadata": result_state.get("metadata",{}),
    }
