from sqlalchemy.orm import Session
from app import schemas, models
from typing import Optional, List

def create_article(db: Session, article: schemas.ArticleCreate):
    db_article = models.Articles(
        title=article.title,
        content=article.author,
        author=article.author,
        tags=article.tags
    )

    db.add(db_article)
    db.commit()
    db.refresh(db_article)
    return db_article

def get_article(db: Session, article_id: int):
    return db.query(models.Articles).filter(models.Articles.id == article_id).first()

def get_articles(
        db: Session,
        skip: int = 0,
        limit: int = 10,
        tag: Optional[str] = None,
        author: Optional[str] = None
):
    query = db.query(models.Articles)

    if tag:
        query = query.filter(models.Article.tags.contains([tag]))

    if author:
        query = query.filter(models.Article.author == author)
    
    return query.offset(skip).limit(limit).all()

def update_article(db: Session, article_id: int, article: schemas.ArticleUpdate):
    db_article = db.query(models.Article).filter(models.Article.id == article_id).first()

    if not db_article:
        return None
    
    update_data = article.model_dump(exclude_uset=True)

    for key, value in update_data.items():
        setattr(db_article, key, value)
    
    db.commit()
    db.refresh(db_article)
    return db_article

def delete_article(db: Session, article_id: int):
    db_article = db.query(models.Article).filter(models.Article.id == article_id).first()  

    if not db_article:
        return None
    
    db.delete(db_article)
    db.commit()
    return db_article