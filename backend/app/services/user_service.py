from datetime import datetime
from typing import Optional, List
from passlib.context import CryptContext
from ..models.user import User, UserCreate, UserUpdate, UserResponse
from ..repositories.user_repository import UserRepository
from .exceptions import NotFoundException, ConflictException, ValidationException

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
    
    def _hash_password(self, password: str) -> str:
        return pwd_context.hash(password)
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)
    
    async def create_user(self, user_data: UserCreate) -> UserResponse:
        existing_email = await self.user_repository.find_by_email(user_data.email)
        if existing_email:
            raise ConflictException("Email already registered")
        
        existing_username = await self.user_repository.find_by_username(user_data.username)
        if existing_username:
            raise ConflictException("Username already taken")
        
        user = User(
            email=user_data.email,
            username=user_data.username,
            password_hash=self._hash_password(user_data.password)
        )
        
        created_user = await self.user_repository.create(user)
        return self._to_response(created_user)
    
    async def get_user(self, user_id: str) -> UserResponse:
        user = await self.user_repository.find_by_id(user_id)
        if not user:
            raise NotFoundException("User not found")
        return self._to_response(user)
    
    async def get_users(self, page: int = 1, limit: int = 20) -> tuple[List[UserResponse], int]:
        skip = (page - 1) * limit
        users = await self.user_repository.find_all(skip=skip, limit=limit)
        total = await self.user_repository.count()
        return [self._to_response(user) for user in users], total
    
    async def update_user(self, user_id: str, user_data: UserUpdate) -> UserResponse:
        user = await self.user_repository.find_by_id(user_id)
        if not user:
            raise NotFoundException("User not found")
        
        update_dict = {}
        
        if user_data.email and user_data.email != user.email:
            existing = await self.user_repository.find_by_email(user_data.email)
            if existing:
                raise ConflictException("Email already registered")
            update_dict["email"] = user_data.email
        
        if user_data.username and user_data.username != user.username:
            existing = await self.user_repository.find_by_username(user_data.username)
            if existing:
                raise ConflictException("Username already taken")
            update_dict["username"] = user_data.username
        
        if user_data.password:
            update_dict["password_hash"] = self._hash_password(user_data.password)
        
        if update_dict:
            update_dict["updated_at"] = datetime.utcnow()
            updated_user = await self.user_repository.update(user_id, update_dict)
            if not updated_user:
                raise NotFoundException("User not found")
            return self._to_response(updated_user)
        
        return self._to_response(user)
    
    async def delete_user(self, user_id: str) -> bool:
        deleted = await self.user_repository.delete(user_id)
        if not deleted:
            raise NotFoundException("User not found")
        return True
    
    async def authenticate(self, email: str, password: str) -> Optional[User]:
        user = await self.user_repository.find_by_email(email)
        if not user:
            return None
        
        if not self.verify_password(password, user.password_hash):
            return None
        
        return user
    
    def _to_response(self, user: User) -> UserResponse:
        return UserResponse(
            id=str(user.id),
            email=user.email,
            username=user.username,
            created_at=user.created_at,
            updated_at=user.updated_at
        )
