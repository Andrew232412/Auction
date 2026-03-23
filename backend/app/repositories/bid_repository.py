from typing import Optional, List
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase
from ..models.bid import Bid

class BidRepository:
    def __init__(self, database: AsyncIOMotorDatabase):
        self.collection = database.bids
    
    async def create(self, bid: Bid) -> Bid:
        result = await self.collection.insert_one(bid.model_dump(by_alias=True, exclude={"id"}))
        bid.id = result.inserted_id
        return bid
    
    async def find_by_id(self, bid_id: str) -> Optional[Bid]:
        if not ObjectId.is_valid(bid_id):
            return None
        bid_dict = await self.collection.find_one({"_id": ObjectId(bid_id)})
        return Bid(**bid_dict) if bid_dict else None
    
    async def find_by_auction(self, auction_id: str, skip: int = 0, limit: int = 50) -> List[Bid]:
        cursor = self.collection.find({"auction_id": auction_id}).sort("timestamp", -1).skip(skip).limit(limit)
        bids = await cursor.to_list(length=limit)
        return [Bid(**bid) for bid in bids]
    
    async def find_highest_bid(self, auction_id: str) -> Optional[Bid]:
        bid_dict = await self.collection.find_one(
            {"auction_id": auction_id},
            sort=[("amount", -1)]
        )
        return Bid(**bid_dict) if bid_dict else None
    
    async def count_by_auction(self, auction_id: str) -> int:
        return await self.collection.count_documents({"auction_id": auction_id})
    
    async def find_by_user(self, user_id: str, skip: int = 0, limit: int = 20) -> List[Bid]:
        cursor = self.collection.find({"user_id": user_id}).sort("timestamp", -1).skip(skip).limit(limit)
        bids = await cursor.to_list(length=limit)
        return [Bid(**bid) for bid in bids]
    
    async def create_indexes(self):
        await self.collection.create_index("auction_id")
        await self.collection.create_index("user_id")
        await self.collection.create_index([("auction_id", 1), ("amount", -1)])
        await self.collection.create_index([("timestamp", -1)])
