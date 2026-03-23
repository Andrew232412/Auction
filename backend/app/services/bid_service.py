from typing import List
from ..models.bid import Bid, BidCreate, BidResponse
from ..repositories.bid_repository import BidRepository
from ..repositories.auction_repository import AuctionRepository
from .exceptions import NotFoundException, ValidationException, ForbiddenException

class BidService:
    def __init__(
        self,
        bid_repository: BidRepository,
        auction_repository: AuctionRepository
    ):
        self.bid_repository = bid_repository
        self.auction_repository = auction_repository
    
    async def place_bid(
        self,
        auction_id: str,
        bid_data: BidCreate,
        user_id: str
    ) -> BidResponse:
        auction = await self.auction_repository.find_by_id(auction_id)
        if not auction:
            raise NotFoundException("Auction not found")
        
        if auction.owner_id == user_id:
            raise ForbiddenException("Cannot bid on your own auction")
        
        if auction.status != "active":
            raise ValidationException("Auction is not active")
        
        if bid_data.amount <= auction.current_price:
            raise ValidationException(
                f"Bid amount must be higher than current price ({auction.current_price})"
            )
        
        bid = Bid(
            auction_id=auction_id,
            user_id=user_id,
            amount=bid_data.amount
        )
        
        created_bid = await self.bid_repository.create(bid)
        
        await self.auction_repository.update_current_price(auction_id, bid_data.amount)
        
        return self._to_response(created_bid)
    
    async def get_auction_bids(
        self,
        auction_id: str,
        page: int = 1,
        limit: int = 50
    ) -> tuple[List[BidResponse], int]:
        auction = await self.auction_repository.find_by_id(auction_id)
        if not auction:
            raise NotFoundException("Auction not found")
        
        skip = (page - 1) * limit
        bids = await self.bid_repository.find_by_auction(auction_id, skip=skip, limit=limit)
        total = await self.bid_repository.count_by_auction(auction_id)
        
        return [self._to_response(bid) for bid in bids], total
    
    async def get_user_bids(
        self,
        user_id: str,
        page: int = 1,
        limit: int = 20
    ) -> List[BidResponse]:
        skip = (page - 1) * limit
        bids = await self.bid_repository.find_by_user(user_id, skip=skip, limit=limit)
        return [self._to_response(bid) for bid in bids]
    
    def _to_response(self, bid: Bid) -> BidResponse:
        return BidResponse(
            id=str(bid.id),
            auction_id=bid.auction_id,
            user_id=bid.user_id,
            amount=bid.amount,
            timestamp=bid.timestamp
        )
