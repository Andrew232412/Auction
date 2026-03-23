from typing import Optional, List
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase
from ..models.user import User

class UserRepository:
    def __init__(self, database: AsyncIOMotorDatabase):
        self.collection = database.users
    
    async def create(self, user: User) -> User:
        result = await self.collection.insert_one(user.model_dump(by_alias=True, exclude={"id"}))
        user.id = result.inserted_id
        return user
    
    async def find_by_id(self, user_id: str) -> Optional[User]:
        if not ObjectId.is_valid(user_id):
            return None
        user_dict = await self.collection.find_one({"_id": ObjectId(user_id)})
        return User(**user_dict) if user_dict else None
    
    async def find_by_email(self, email: str) -> Optional[User]:
        user_dict = await self.collection.find_one({"email": email})
        return User(**user_dict) if user_dict else None
    
    async def find_by_username(self, username: str) -> Optional[User]:
        user_dict = await self.collection.find_one({"username": username})
        return User(**user_dict) if user_dict else None
    
    async def find_all(self, skip: int = 0, limit: int = 20) -> List[User]:
        cursor = self.collection.find().skip(skip).limit(limit)
        users = await cursor.to_list(length=limit)
        return [User(**user) for user in users]
    
    async def count(self) -> int:
        return await self.collection.count_documents({})
    
    async def update(self, user_id: str, update_data: dict) -> Optional[User]:
        if not ObjectId.is_valid(user_id):
            return None
        
        result = await self.collection.find_one_and_update(
            {"_id": ObjectId(user_id)},
            {"$set": update_data},
            return_document=True
        )
        return User(**result) if result else None
    
    async def delete(self, user_id: str) -> bool:
        if not ObjectId.is_valid(user_id):
            return False
        result = await self.collection.delete_one({"_id": ObjectId(user_id)})
        return result.deleted_count > 0
    
    async def create_indexes(self):
        await self.collection.create_index("email", unique=True)
        await self.collection.create_index("username", unique=True)
