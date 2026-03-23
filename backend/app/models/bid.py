from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from bson import ObjectId

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

class Bid(BaseModel):
    id: Optional[PyObjectId] = Field(default=None, alias="_id")
    auction_id: str
    user_id: str
    amount: float = Field(gt=0)
    timestamp: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class BidCreate(BaseModel):
    amount: float = Field(gt=0)

class BidResponse(BaseModel):
    id: str
    auction_id: str
    user_id: str
    amount: float
    timestamp: datetime

    class Config:
        from_attributes = True
