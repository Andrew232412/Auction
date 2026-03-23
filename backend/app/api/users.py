from fastapi import APIRouter, Depends, status, Query
from typing import List
from ..database import get_database
from ..repositories.user_repository import UserRepository
from ..services.user_service import UserService
from ..models.user import UserUpdate, UserResponse
from ..models.common import PaginatedResponse
from ..auth.dependencies import get_current_user

router = APIRouter()

def get_user_service():
    db = get_database()
    user_repo = UserRepository(db)
    return UserService(user_repo)

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: str,
    user_service: UserService = Depends(get_user_service)
):
    return await user_service.get_user(user_id)

@router.get("", response_model=PaginatedResponse[UserResponse])
async def get_users(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    user_service: UserService = Depends(get_user_service)
):
    users, total = await user_service.get_users(page=page, limit=limit)
    pages = (total + limit - 1) // limit
    
    return PaginatedResponse(
        items=users,
        total=total,
        page=page,
        pages=pages,
        limit=limit
    )

@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: str,
    user_data: UserUpdate,
    current_user: dict = Depends(get_current_user),
    user_service: UserService = Depends(get_user_service)
):
    if current_user["user_id"] != user_id:
        from fastapi import HTTPException
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only update your own profile"
        )
    
    return await user_service.update_user(user_id, user_data)

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: str,
    current_user: dict = Depends(get_current_user),
    user_service: UserService = Depends(get_user_service)
):
    if current_user["user_id"] != user_id:
        from fastapi import HTTPException
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only delete your own account"
        )
    
    await user_service.delete_user(user_id)
