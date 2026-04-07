from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List

class Restaurant(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    location: str
    description: Optional[str] = None
    latitude: float
    longitude: float
    category: Optional[str] = Field(default="General")
    phone: Optional[str] = Field(default=None) 

    menu_items: List["MenuItem"] = Relationship(back_populates="restaurant")
    reviews: List["Review"] = Relationship(back_populates="restaurant")