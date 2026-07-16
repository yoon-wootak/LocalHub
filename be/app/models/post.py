from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func

from app.db.base import Base


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False, index=True)
    content = Column(Text, nullable=False)
    category = Column(String(50), nullable=False, index=True, server_default="기타")
    location_name = Column(String(200), nullable=False, server_default="")
    place_id = Column(Integer, ForeignKey("places.id"), nullable=True, index=True)
    password = Column(String(100), nullable=False)
    view_count = Column(Integer, nullable=False, default=0, server_default="0")
    like_count = Column(
    Integer,
    nullable=False,
    default=0,
    server_default="0",
)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())