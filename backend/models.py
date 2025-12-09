from typing import Dict, Any
from pydantic import BaseModel

class AnalysisResponse(BaseModel):
    summary:str
    metadata: Dict[str, Any]