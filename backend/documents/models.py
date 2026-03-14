from typing import List, Optional
from pydantic import BaseModel


class DocumentOut(BaseModel):
    doc_id: str
    user_id: str
    filename: str
    page_count: int
    chunk_count: int
    uploaded_at: str
    size_bytes: Optional[int] = None


class DocumentList(BaseModel):
    documents: List[DocumentOut]
