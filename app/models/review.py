from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from datetime import datetime


class Review(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    restaurant_id: int = Field(foreign_key="restaurant.id")
    user_id: int = Field(foreign_key="user.id")
    rating: int
    comment: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

    restaurant: Optional["Restaurant"] = Relationship(back_populates="reviews")
    user: Optional["User"] = Relationship(back_populates="reviews")
