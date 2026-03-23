from fastapi import APIRouter, Depends, status, Query
from typing import Optional
from ..database import get_database
from ..repositories.auction_repository import AuctionRepository
from ..services.auction_service import AuctionService
from ..models.auction import AuctionCreate, AuctionUpdate, AuctionResponse, AuctionStatus
from ..models.common import PaginatedResponse
from ..auth.dependencies import get_current_user

router = APIRouter()

def get_auction_service():
    db = get_database()
    auction_repo = AuctionRepository(db)
    return AuctionService(auction_repo)

@router.post("", response_model=AuctionResponse, status_code=status.HTTP_201_CREATED)
async def create_auction(
    auction_data: AuctionCreate,
    current_user: dict = Depends(get_current_user),
    auction_service: AuctionService = Depends(get_auction_service)
):
    return await auction_service.create_auction(auction_data, current_user["user_id"])

@router.get("/{auction_id}", response_model=AuctionResponse)
async def get_auction(
    auction_id: str,
    auction_service: AuctionService = Depends(get_auction_service)
):
    return await auction_service.get_auction(auction_id)

@router.get("", response_model=PaginatedResponse[AuctionResponse])
async def get_auctions(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    category: Optional[str] = None,
    status: Optional[AuctionStatus] = None,
    sort_by: str = Query("created_at", regex="^(created_at|current_price|end_date|title)$"),
    sort_order: int = Query(-1, ge=-1, le=1),
    auction_service: AuctionService = Depends(get_auction_service)
):
    auctions, total = await auction_service.get_auctions(
        page=page,
        limit=limit,
        category=category,
        status=status,
        sort_by=sort_by,
        sort_order=sort_order
    )
    pages = (total + limit - 1) // limit
    
    return PaginatedResponse(
        items=auctions,
        total=total,
        page=page,
        pages=pages,
        limit=limit
    )

@router.put("/{auction_id}", response_model=AuctionResponse)
async def update_auction(
    auction_id: str,
    auction_data: AuctionUpdate,
    current_user: dict = Depends(get_current_user),
    auction_service: AuctionService = Depends(get_auction_service)
):
    return await auction_service.update_auction(
        auction_id,
        auction_data,
        current_user["user_id"]
    )

@router.delete("/{auction_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_auction(
    auction_id: str,
    current_user: dict = Depends(get_current_user),
    auction_service: AuctionService = Depends(get_auction_service)
):
    await auction_service.delete_auction(auction_id, current_user["user_id"])
