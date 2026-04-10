from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

class Review(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    restaurant_id: int = Field(foreign_key="restaurant.id")
    user_id: int = Field(foreign_key="user.id")
    rating: int
    comment: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
    restaurant: Optional["Restaurant"] = Relationship(back_populates="reviews")
    user: Optional["User"] = Relationship(back_populates="reviews")
