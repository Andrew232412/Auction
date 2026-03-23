from fastapi import APIRouter, Depends, status, Query
from ..database import get_database
from ..repositories.bid_repository import BidRepository
from ..repositories.auction_repository import AuctionRepository
from ..services.bid_service import BidService
from ..models.bid import BidCreate, BidResponse
from ..models.common import PaginatedResponse
from ..auth.dependencies import get_current_user

router = APIRouter()

def get_bid_service():
    db = get_database()
    bid_repo = BidRepository(db)
    auction_repo = AuctionRepository(db)
    return BidService(bid_repo, auction_repo)

@router.post("/auctions/{auction_id}/bids", response_model=BidResponse, status_code=status.HTTP_201_CREATED)
async def place_bid(
    auction_id: str,
    bid_data: BidCreate,
    current_user: dict = Depends(get_current_user),
    bid_service: BidService = Depends(get_bid_service)
):
    return await bid_service.place_bid(auction_id, bid_data, current_user["user_id"])

@router.get("/auctions/{auction_id}/bids", response_model=PaginatedResponse[BidResponse])
async def get_auction_bids(
    auction_id: str,
    page: int = Query(1, ge=1),
    limit: int = Query(50, ge=1, le=100),
    bid_service: BidService = Depends(get_bid_service)
):
    bids, total = await bid_service.get_auction_bids(auction_id, page=page, limit=limit)
    pages = (total + limit - 1) // limit
    
    return PaginatedResponse(
        items=bids,
        total=total,
        page=page,
        pages=pages,
        limit=limit
    )
