from typing import Optional, List, Dict, Any
from datetime import datetime
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase
from ..models.auction import Auction, AuctionStatus

class AuctionRepository:
    def __init__(self, database: AsyncIOMotorDatabase):
        self.collection = database.auctions
    
    async def create(self, auction: Auction) -> Auction:
        result = await self.collection.insert_one(auction.model_dump(by_alias=True, exclude={"id"}))
        auction.id = result.inserted_id
        return auction
    
    async def find_by_id(self, auction_id: str) -> Optional[Auction]:
        if not ObjectId.is_valid(auction_id):
            return None
        auction_dict = await self.collection.find_one({"_id": ObjectId(auction_id)})
        return Auction(**auction_dict) if auction_dict else None
    
    async def find_all(
        self,
        skip: int = 0,
        limit: int = 20,
        category: Optional[str] = None,
        status: Optional[AuctionStatus] = None,
        sort_by: str = "created_at",
        sort_order: int = -1
    ) -> List[Auction]:
        query: Dict[str, Any] = {}
        
        if category:
            query["category"] = category
        if status:
            query["status"] = status
        
        cursor = self.collection.find(query).sort(sort_by, sort_order).skip(skip).limit(limit)
        auctions = await cursor.to_list(length=limit)
        return [Auction(**auction) for auction in auctions]
    
    async def count(
        self,
        category: Optional[str] = None,
        status: Optional[AuctionStatus] = None
    ) -> int:
        query: Dict[str, Any] = {}
        
        if category:
            query["category"] = category
        if status:
            query["status"] = status
        
        return await self.collection.count_documents(query)
    
    async def update(self, auction_id: str, update_data: dict) -> Optional[Auction]:
        if not ObjectId.is_valid(auction_id):
            return None
        
        result = await self.collection.find_one_and_update(
            {"_id": ObjectId(auction_id)},
            {"$set": update_data},
            return_document=True
        )
        return Auction(**result) if result else None
    
    async def update_current_price(self, auction_id: str, new_price: float) -> Optional[Auction]:
        if not ObjectId.is_valid(auction_id):
            return None
        
        result = await self.collection.find_one_and_update(
            {"_id": ObjectId(auction_id)},
            {"$set": {"current_price": new_price}},
            return_document=True
        )
        return Auction(**result) if result else None
    
    async def delete(self, auction_id: str) -> bool:
        if not ObjectId.is_valid(auction_id):
            return False
        result = await self.collection.delete_one({"_id": ObjectId(auction_id)})
        return result.deleted_count > 0
    
    async def find_by_owner(self, owner_id: str, skip: int = 0, limit: int = 20) -> List[Auction]:
        cursor = self.collection.find({"owner_id": owner_id}).skip(skip).limit(limit)
        auctions = await cursor.to_list(length=limit)
        return [Auction(**auction) for auction in auctions]
    
    async def close_expired_auctions(self) -> int:
        result = await self.collection.update_many(
            {
                "end_date": {"$lt": datetime.utcnow()},
                "status": AuctionStatus.ACTIVE
            },
            {"$set": {"status": AuctionStatus.CLOSED}}
        )
        return result.modified_count
    
    async def create_indexes(self):
        await self.collection.create_index("owner_id")
        await self.collection.create_index("category")
        await self.collection.create_index("status")
        await self.collection.create_index("end_date")
        await self.collection.create_index([("created_at", -1)])
