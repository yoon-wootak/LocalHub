from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.base import Base
from app.db.session import engine, get_db
from app.models.place import Place

router = APIRouter()

place = Place(
    title="테스트 장소",
    content_type="관광지",
    addr1="테스트 주소",
    latitude=36.1,
    longitude=128.4,
)

@router.get("/api/places")
def list_places(db: Session = Depends(get_db)):
    places = db.query(Place).limit(5).all()
    return [{"id": p.id, "title": p.title, "content_type": p.content_type} for p in places]

@router.get("/api/health")
def health():
    return {"status": "ok"}

@router.get("/api/db-test")
def db_test(db: Session = Depends(get_db)):
    Base.metadata.create_all(bind=engine)

    place = Place(
        title="테스트 장소",
        content_type="관광지",
        address="테스트 주소",
        latitude=36.1,
        longitude=128.4,
    )

    db.add(place)
    db.commit()
    db.refresh(place)

    return {
        "message": "db connected",
        "place_id": place.id
    }