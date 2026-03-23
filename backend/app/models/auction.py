from datetime import datetime
from typing import Optional
from enum import Enum
from pydantic import BaseModel, Field
from bson import ObjectId

class AuctionStatus(str, Enum):
    ACTIVE = "active"
    CLOSED = "closed"
    CANCELLED = "cancelled"

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    @classmethod
    def __get_pydantic_json_schema__(cls, field_schema):
        field_schema.update(type="string")

class Auction(BaseModel):
    id: Optional[PyObjectId] = Field(default=None, alias="_id")
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

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

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

    class Config:
        from_attributes = True
