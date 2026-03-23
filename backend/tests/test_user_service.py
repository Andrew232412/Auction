import pytest
from datetime import datetime
from app.models.user import User, UserCreate, UserUpdate
from app.services.user_service import UserService
from app.services.exceptions import NotFoundException, ConflictException
from app.repositories.user_repository import UserRepository

@pytest.mark.asyncio
async def test_create_user(test_db):
    user_repo = UserRepository(test_db)
    user_service = UserService(user_repo)
    
    user_data = UserCreate(
        email="test@example.com",
        username="testuser",
        password="password123"
    )
    
    user = await user_service.create_user(user_data)
    
    assert user.email == "test@example.com"
    assert user.username == "testuser"
    assert user.id is not None

@pytest.mark.asyncio
async def test_create_duplicate_email(test_db):
    user_repo = UserRepository(test_db)
    user_service = UserService(user_repo)
    
    user_data = UserCreate(
        email="duplicate@example.com",
        username="user1",
        password="password123"
    )
    
    await user_service.create_user(user_data)
    
    with pytest.raises(ConflictException):
        await user_service.create_user(user_data)

@pytest.mark.asyncio
async def test_authenticate_user(test_db):
    user_repo = UserRepository(test_db)
    user_service = UserService(user_repo)
    
    user_data = UserCreate(
        email="auth@example.com",
        username="authuser",
        password="password123"
    )
    
    await user_service.create_user(user_data)
    
    authenticated = await user_service.authenticate("auth@example.com", "password123")
    assert authenticated is not None
    assert authenticated.email == "auth@example.com"
    
    failed_auth = await user_service.authenticate("auth@example.com", "wrongpassword")
    assert failed_auth is None
