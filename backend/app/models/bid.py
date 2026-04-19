from datetime import datetime
from typing import Optional

from bson import ObjectId
from pydantic import BaseModel, ConfigDict, Field, field_validator

from .objectid import coerce_object_id


class Bid(BaseModel):
    model_config = ConfigDict(populate_by_name=True, arbitrary_types_allowed=True)

    id: Optional[ObjectId] = Field(default=None, alias="_id")
    auction_id: str
    user_id: str
    amount: float = Field(gt=0)
    timestamp: datetime = Field(default_factory=datetime.utcnow)

    @field_validator("id", mode="before")
    @classmethod
    def validate_id(cls, v: object) -> ObjectId | None:
        return coerce_object_id(v)


class BidCreate(BaseModel):
    amount: float = Field(gt=0)


class BidResponse(BaseModel):
    id: str
    auction_id: str
    user_id: str
    amount: float
    timestamp: datetime

    model_config = ConfigDict(from_attributes=True)
