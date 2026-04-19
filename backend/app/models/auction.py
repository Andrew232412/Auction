from datetime import datetime
from typing import Optional
from enum import Enum

from bson import ObjectId
from pydantic import BaseModel, ConfigDict, Field, field_validator

from .objectid import coerce_object_id


class AuctionStatus(str, Enum):
    ACTIVE = "active"
    CLOSED = "closed"
    CANCELLED = "cancelled"


class Auction(BaseModel):
    model_config = ConfigDict(populate_by_name=True, arbitrary_types_allowed=True)

    id: Optional[ObjectId] = Field(default=None, alias="_id")
    title: str
    description: str
    category: str
    starting_price: float = Field(gt=0)
    current_price: float = Field(gt=0)
    start_date: datetime
    end_date: datetime
    owner_id: str
    status: AuctionStatus = AuctionStatus.ACTIVE
    created_at: datetime = Field(default_factory=datetime.utcnow)

    @field_validator("id", mode="before")
    @classmethod
    def validate_id(cls, v: object) -> ObjectId | None:
        return coerce_object_id(v)


class AuctionCreate(BaseModel):
    title: str
    description: str
    category: str
    starting_price: float = Field(gt=0)
    start_date: datetime
    end_date: datetime


class AuctionUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    starting_price: Optional[float] = Field(default=None, gt=0)
    end_date: Optional[datetime] = None
    status: Optional[AuctionStatus] = None


class AuctionResponse(BaseModel):
    id: str
    title: str
    description: str
    category: str
    starting_price: float
    current_price: float
    start_date: datetime
    end_date: datetime
    owner_id: str
    status: AuctionStatus
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
