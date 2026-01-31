from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app import models, schemas, crud
from app.database import engine, get_db
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import os

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Blog API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Production'da specific domain bering
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/articles", response_model = schemas.ArticleResponse, status_code = 201)
def create_article(
    article: schemas.ArticleCreate,
    db: Session = Depends(get_db)
):
    return crud.create_article(db=db, article=article)

@app.get("/articles", response_model=List[schemas.ArticleResponse])
def get_articles(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    tag: Optional[str] = None,
    author: Optional[str] = None,
    db: Session = Depends(get_db)
):
    articles = crud.get_articles(db=db, skip=skip, limit=limit, tag=tag, author=author)
    return articles

@app.get("/articles/{article_id}", response_model=schemas.ArticleResponse)
def get_article(
    article_id: int,
    db: Session = Depends(get_db)
):
    article = crud.get_article(db=db, article_id=article_id)

    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    return article

@app.get("/articles/{article_id}", response_model=schemas.ArticleResponse)
def update_article(
    article_id: int,
    article: schemas.ArticleUpdate,
    db: Session = Depends(get_db)
):
    update_article = crud.update_article(db=db, article_id = article_id, article=article)
    if not update_article:
        raise HTTPException(status_code=404, detail="Article not found")
    return update_article

@app.delete("/articles/{article_id}", response_model=schemas.ArticleResponse)
def delete_article(
    article_id: int,
    db: Session = Depends(get_db)
):
    delete_article = crud.delete_article(db=db, article_id=article_id)
    if not delete_article:
        raise HTTPException(status_code=404, detail="Article not found")
    
    return delete_article

@app.get("/")
async def read_root():
    return FileResponse('frontend/index.html')

if os.path.exists('frontend'):
    app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")