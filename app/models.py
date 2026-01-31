from app.database import Base
from sqlalchemy import func
from sqlalchemy import Column, Integer, String, Text, ARRAY, DateTime


class Articles(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200))
    content = Column(Text, nullable=False)
    author = Column(String(100), nullable=False)
    tags = Column(ARRAY(String), default=[])
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
