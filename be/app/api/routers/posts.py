from datetime import datetime, timezone
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.place import Place
from app.models.post import Post

router = APIRouter(prefix="/api/posts", tags=["posts"])


class PostCreate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    category: Optional[str] = None
    location_name: Optional[str] = None
    place_id: Optional[int] = None
    password: Optional[str] = None


class PostUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    category: Optional[str] = None
    location_name: Optional[str] = None
    place_id: Optional[int] = None
    password: Optional[str] = None


class PostDelete(BaseModel):
    password: Optional[str] = None


class PostOut(BaseModel):
    id: int
    title: str
    content: str
    category: str
    location_name: str

    view_count: int
    like_count: int

    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class PostListResponse(BaseModel):
    items: List[PostOut]
    total: int
    page: int
    size: int

    model_config = ConfigDict(from_attributes=True)


class PasswordPayload(BaseModel):
    password: Optional[str] = None


def resolve_place_id(
    db: Session,
    place_id: Optional[int],
    location_name: str,
) -> Optional[int]:
    if place_id is not None:
        place = db.query(Place).filter(Place.id == place_id).first()
        if not place:
            raise HTTPException(status_code=400, detail="place_id not found")
        return place_id

    if location_name:
        place = db.query(Place).filter(Place.title == location_name).first()
        if place:
            return place.id

    return None


@router.get("", response_model=PostListResponse)
def list_posts(
    keyword: Optional[str] = None,
    category: Optional[str] = None,
    page: int = 1,
    size: int = 10,
    db: Session = Depends(get_db),
):
    page = max(page, 1)
    size = max(size, 1)

    query = db.query(Post)

    if keyword and keyword.strip():
        keyword_value = keyword.strip()
        query = query.filter(
            or_(
                Post.title.ilike(f"%{keyword_value}%"),
                Post.content.ilike(f"%{keyword_value}%"),
            )
        )

    if category and category.strip():
        category_value = category.strip()
        query = query.filter(Post.category == category_value)

    total = query.count()
    posts = (
        query.order_by(Post.created_at.desc(), Post.id.desc())
        .offset((page - 1) * size)
        .limit(size)
        .all()
    )

    return {"items": posts, "total": total, "page": page, "size": size}


@router.get("/{post_id}", response_model=PostOut)
def get_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="post not found")

    post.view_count += 1
    db.commit()
    db.refresh(post)
    return post


@router.post("", response_model=PostOut, status_code=status.HTTP_201_CREATED)
def create_post(payload: PostCreate, db: Session = Depends(get_db)):
    title = (payload.title or "").strip()
    content = (payload.content or "").strip()
    category = (payload.category or "").strip()
    password = (payload.password or "").strip()
    location_name = (payload.location_name or "").strip()

    if not title or not content or not category or not password:
        raise HTTPException(
            status_code=400,
            detail="title, content, category, and password are required",
        )

    place_id = resolve_place_id(db, payload.place_id, location_name)

    post = Post(
        title=title,
        content=content,
        category=category,
        location_name=location_name,
        place_id=place_id,
        password=password,
    )
    db.add(post)
    db.commit()
    db.refresh(post)
    return post


@router.put("/{post_id}", response_model=PostOut)
def update_post(post_id: int, payload: PostUpdate, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="post not found")

    if payload.title is not None:
        title = payload.title.strip()
        if not title:
            raise HTTPException(status_code=400, detail="title is required")
        post.title = title

    if payload.content is not None:
        content = payload.content.strip()
        if not content:
            raise HTTPException(status_code=400, detail="content is required")
        post.content = content

    if payload.category is not None:
        category = payload.category.strip()
        if not category:
            raise HTTPException(status_code=400, detail="category is required")
        post.category = category

    if payload.location_name is not None:
        location_name = payload.location_name.strip()
        if not location_name:
            raise HTTPException(status_code=400, detail="location_name is required")
        post.location_name = location_name
        post.place_id = resolve_place_id(db, payload.place_id, location_name)
    elif payload.place_id is not None:
        post.place_id = resolve_place_id(db, payload.place_id, post.location_name)

    post.updated_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(post)
    return post


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int, payload: PostDelete, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="post not found")

    if payload.password is None or not payload.password.strip():
        raise HTTPException(status_code=400, detail="password is required")

    if payload.password != post.password:
        raise HTTPException(status_code=403, detail="password mismatch")

    db.delete(post)
    db.commit()
    return None

@router.post("/{post_id}/verify-password")
def verify_post_password(post_id: int, payload: PasswordPayload, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="post not found")

    if payload.password is None or not payload.password.strip():
        raise HTTPException(status_code=400, detail="password is required")

    if payload.password != post.password:
        raise HTTPException(status_code=403, detail="password mismatch")

    return {"ok": True}

@router.post("/{post_id}/like")
def like_post(
    post_id: int,
    db: Session = Depends(get_db),
):
    post = (
        db.query(Post)
        .filter(Post.id == post_id)
        .first()
    )

    if not post:
        raise HTTPException(
            status_code=404,
            detail="post not found",
        )

    post.like_count += 1

    db.commit()
    db.refresh(post)

    return {
        "post_id": post.id,
        "liked": True,
        "like_count": post.like_count,
    }



@router.delete("/{post_id}/like")
def unlike_post(
    post_id: int,
    db: Session = Depends(get_db),
):
    post = (
        db.query(Post)
        .filter(Post.id == post_id)
        .first()
    )

    if not post:
        raise HTTPException(
            status_code=404,
            detail="post not found",
        )

    post.like_count = max(
        0,
        post.like_count - 1,
    )

    db.commit()
    db.refresh(post)

    return {
        "post_id": post.id,
        "liked": False,
        "like_count": post.like_count,
    }