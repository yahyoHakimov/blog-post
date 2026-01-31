from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel


class ArticleCreate(BaseModel):
    title: str
    content: str
    author: str
    tags: List[str] = []

class ArticleUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    author: Optional[str] = None
    tags: Optional[List[str]] = None

class ArticleResponse(BaseModel):
    id: int
    title: str
    content: str
    author: str
    tags: str
    tags: List[str]
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True  
