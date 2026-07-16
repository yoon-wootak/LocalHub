import math
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func, or_
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.place import Place
from app.models.post import Post


router = APIRouter(
    prefix="/api/locations",
    tags=["locations"],
)


def build_description(place: Place) -> str:
    title = place.title or "이 지역의 장소"
    category = place.content_type or "명소"
    address = place.addr1 or "구미·경북 지역"

    return (
        f"{title}는 {category}로, {address}에 위치한 곳입니다. "
        "지역의 분위기와 함께 둘러보기 좋은 추천 장소입니다."
    )


def map_place(place: Place) -> dict:
    return {
        "id": place.id,
        "content_id": place.content_id,
        "content_type_id": place.content_type_id,
        "name": place.title,
        "category": place.content_type,
        "address": place.addr1,
        "phone": place.tel,
        "latitude": place.latitude,
        "longitude": place.longitude,
        "image_url": place.firstimage,
        "description": build_description(place),
        "short_description": build_description(place),
        "view_count": place.view_count,
        "like_count": place.like_count,
        "distance_km": None,
    }


def calculate_distance(
    lat1: float,
    lon1: float,
    lat2: float,
    lon2: float,
) -> float:
    radius_km = 6371.0

    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)

    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)

    a = (
        math.sin(dphi / 2) ** 2
        + math.cos(phi1)
        * math.cos(phi2)
        * math.sin(dlambda / 2) ** 2
    )

    c = 2 * math.atan2(
        math.sqrt(a),
        math.sqrt(1 - a),
    )

    return radius_km * c


@router.get("/ranking")
def get_location_ranking(
    limit: int = 5,
    db: Session = Depends(get_db),
):
    limit = max(1, min(limit, 100))

    places = db.query(Place).all()

    if not places:
        return {"items": []}

    explicit_counts = {
        place_id: count
        for place_id, count in (
            db.query(
                Post.place_id,
                func.count(Post.id),
            )
            .filter(Post.place_id.isnot(None))
            .group_by(Post.place_id)
            .all()
        )
    }

    title_to_id = {
        place.title: place.id
        for place in places
    }

    fallback_counts = {}

    fallback_rows = (
        db.query(
            Post.location_name,
            func.count(Post.id),
        )
        .filter(
            Post.place_id.is_(None),
            Post.location_name.isnot(None),
            Post.location_name != "",
        )
        .group_by(Post.location_name)
        .all()
    )

    for location_name, count in fallback_rows:
        place_id = title_to_id.get(location_name)

        if place_id:
            fallback_counts[place_id] = (
                fallback_counts.get(place_id, 0)
                + count
            )

    ranking = []

    for place in places:
        post_count = (
            explicit_counts.get(place.id, 0)
            + fallback_counts.get(place.id, 0)
        )

        score = (
            place.view_count
            + place.like_count
            + post_count
        )

        ranking.append(
            (
                score,
                post_count,
                place,
            )
        )

    ranking.sort(
        key=lambda item: (
            -item[0],
            -item[2].view_count,
            -item[2].like_count,
            item[2].id,
        )
    )

    items = [
        {
            **map_place(place),
            "post_count": post_count,
            "score": score,
        }
        for score, post_count, place
        in ranking[:limit]
    ]

    return {"items": items}


@router.get("")
def list_locations(
    keyword: Optional[str] = None,
    category: Optional[str] = None,
    district: Optional[str] = None,
    limit: int = 20,
    offset: int = 0,
    db: Session = Depends(get_db),
):
    limit = max(1, min(limit, 100))
    offset = max(offset, 0)

    query = db.query(Place)

    if keyword and keyword.strip():
        keyword_value = f"%{keyword.strip()}%"

        query = query.filter(
            or_(
                Place.title.ilike(keyword_value),
                Place.addr1.ilike(keyword_value),
            )
        )

    def normalize_category(value: str) -> str:
        if not value:
            return ""

        normalized = value.strip()

        aliases = {
            "축제·행사": "축제공연행사",
            "축제행사": "축제공연행사",
            "여행 코스": "여행코스",
            "여행코스": "여행코스",
        }

        return aliases.get(
            normalized,
            normalized,
        )

    if category and category.strip():
        normalized_category = normalize_category(
            category,
        )

        query = query.filter(
            Place.content_type
            == normalized_category
        )

    if district and district.strip():
        district_value = f"%{district.strip()}%"

        query = query.filter(
            Place.addr1.ilike(district_value)
        )

    total = query.count()

    places = (
        query
        .order_by(func.random())
        .offset(offset)
        .limit(limit)
        .all()
    )

    return {
        "items": [
            map_place(place)
            for place in places
        ],
        "total": total,
    }


@router.get("/{location_id}")
def get_location(
    location_id: int,
    db: Session = Depends(get_db),
):
    place = (
        db.query(Place)
        .filter(Place.id == location_id)
        .first()
    )

    if not place:
        raise HTTPException(
            status_code=404,
            detail="location not found",
        )

    place.view_count += 1

    db.commit()
    db.refresh(place)

    return map_place(place)


@router.post("/{location_id}/like")
def like_location(
    location_id: int,
    db: Session = Depends(get_db),
):
    place = (
        db.query(Place)
        .filter(Place.id == location_id)
        .first()
    )

    if not place:
        raise HTTPException(
            status_code=404,
            detail="location not found",
        )

    place.like_count += 1

    db.commit()
    db.refresh(place)

    return {
        "location_id": place.id,
        "liked": True,
        "like_count": place.like_count,
    }


@router.delete("/{location_id}/like")
def unlike_location(
    location_id: int,
    db: Session = Depends(get_db),
):
    place = (
        db.query(Place)
        .filter(Place.id == location_id)
        .first()
    )

    if not place:
        raise HTTPException(
            status_code=404,
            detail="location not found",
        )

    place.like_count = max(
        0,
        place.like_count - 1,
    )

    db.commit()
    db.refresh(place)

    return {
        "location_id": place.id,
        "liked": False,
        "like_count": place.like_count,
    }


@router.get("/{location_id}/nearby")
def get_location_nearby(
    location_id: int,
    limit: int = 3,
    lat: Optional[float] = None,
    lon: Optional[float] = None,
    db: Session = Depends(get_db),
):
    place = (
        db.query(Place)
        .filter(Place.id == location_id)
        .first()
    )

    if not place:
        raise HTTPException(
            status_code=404,
            detail="location not found",
        )

    reference_lat = lat
    reference_lon = lon

    if (
        reference_lat is None
        or reference_lon is None
    ):
        if (
            place.latitude is not None
            and place.longitude is not None
        ):
            reference_lat = place.latitude
            reference_lon = place.longitude
        else:
            reference_lat = 36.1173
            reference_lon = 128.3440

    nearby_places = (
        db.query(Place)
        .filter(
            Place.id != location_id,
            Place.latitude.isnot(None),
            Place.longitude.isnot(None),
        )
        .all()
    )

    nearby_places.sort(
        key=lambda other: calculate_distance(
            reference_lat,
            reference_lon,
            other.latitude,
            other.longitude,
        )
    )

    result = []

    for other in nearby_places[: max(1, limit)]:
        mapped = map_place(other)

        mapped["distance_km"] = round(
            calculate_distance(
                reference_lat,
                reference_lon,
                other.latitude,
                other.longitude,
            ),
            1,
        )

        result.append(mapped)

    return result