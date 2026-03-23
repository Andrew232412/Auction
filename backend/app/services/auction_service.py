from datetime import datetime
from typing import List, Optional
from ..models.auction import Auction, AuctionCreate, AuctionUpdate, AuctionResponse, AuctionStatus
from ..repositories.auction_repository import AuctionRepository
from .exceptions import NotFoundException, ValidationException, ForbiddenException

class AuctionService:
    def __init__(self, auction_repository: AuctionRepository):
        self.auction_repository = auction_repository
    
    async def create_auction(self, auction_data: AuctionCreate, owner_id: str) -> AuctionResponse:
        if auction_data.end_date <= auction_data.start_date:
            raise ValidationException("End date must be after start date")
        
        if auction_data.start_date < datetime.utcnow():
            raise ValidationException("Start date cannot be in the past")
        
        auction = Auction(
            title=auction_data.title,
            description=auction_data.description,
            category=auction_data.category,
            starting_price=auction_data.starting_price,
            current_price=auction_data.starting_price,
            start_date=auction_data.start_date,
            end_date=auction_data.end_date,
            owner_id=owner_id,
            status=AuctionStatus.ACTIVE
        )
        
        created_auction = await self.auction_repository.create(auction)
        return self._to_response(created_auction)
    
    async def get_auction(self, auction_id: str) -> AuctionResponse:
        auction = await self.auction_repository.find_by_id(auction_id)
        if not auction:
            raise NotFoundException("Auction not found")
        return self._to_response(auction)
    
    async def get_auctions(
        self,
        page: int = 1,
        limit: int = 20,
        category: Optional[str] = None,
        status: Optional[AuctionStatus] = None,
        sort_by: str = "created_at",
        sort_order: int = -1
    ) -> tuple[List[AuctionResponse], int]:
        skip = (page - 1) * limit
        
        auctions = await self.auction_repository.find_all(
            skip=skip,
            limit=limit,
            category=category,
            status=status,
            sort_by=sort_by,
            sort_order=sort_order
        )
        
        total = await self.auction_repository.count(category=category, status=status)
        
        return [self._to_response(auction) for auction in auctions], total
    
    async def update_auction(
        self,
        auction_id: str,
        auction_data: AuctionUpdate,
        user_id: str
    ) -> AuctionResponse:
        auction = await self.auction_repository.find_by_id(auction_id)
        if not auction:
            raise NotFoundException("Auction not found")
        
        if auction.owner_id != user_id:
            raise ForbiddenException("You don't have permission to update this auction")
        
        if auction.status == AuctionStatus.CLOSED:
            raise ValidationException("Cannot update closed auction")
        
        update_dict = {}
        
        if auction_data.title:
            update_dict["title"] = auction_data.title
        
        if auction_data.description:
            update_dict["description"] = auction_data.description
        
        if auction_data.category:
            update_dict["category"] = auction_data.category
        
        if auction_data.starting_price:
            if auction.current_price > auction.starting_price:
                raise ValidationException("Cannot change starting price after bids have been placed")
            update_dict["starting_price"] = auction_data.starting_price
            update_dict["current_price"] = auction_data.starting_price
        
        if auction_data.end_date:
            if auction_data.end_date <= datetime.utcnow():
                raise ValidationException("End date must be in the future")
            update_dict["end_date"] = auction_data.end_date
        
        if auction_data.status:
            update_dict["status"] = auction_data.status
        
        if update_dict:
            updated_auction = await self.auction_repository.update(auction_id, update_dict)
            if not updated_auction:
                raise NotFoundException("Auction not found")
            return self._to_response(updated_auction)
        
        return self._to_response(auction)
    
    async def delete_auction(self, auction_id: str, user_id: str) -> bool:
        auction = await self.auction_repository.find_by_id(auction_id)
        if not auction:
            raise NotFoundException("Auction not found")
        
        if auction.owner_id != user_id:
            raise ForbiddenException("You don't have permission to delete this auction")
        
        if auction.current_price > auction.starting_price:
            raise ValidationException("Cannot delete auction with active bids")
        
        deleted = await self.auction_repository.delete(auction_id)
        return deleted
    
    async def is_auction_active(self, auction_id: str) -> bool:
        auction = await self.auction_repository.find_by_id(auction_id)
        if not auction:
            return False
        
        if auction.status != AuctionStatus.ACTIVE:
            return False
        
        if auction.end_date < datetime.utcnow():
            await self.auction_repository.update(auction_id, {"status": AuctionStatus.CLOSED})
            return False
        
        return True
    
    async def update_auction_price(self, auction_id: str, new_price: float) -> AuctionResponse:
        updated_auction = await self.auction_repository.update_current_price(auction_id, new_price)
        if not updated_auction:
            raise NotFoundException("Auction not found")
        return self._to_response(updated_auction)
    
    def _to_response(self, auction: Auction) -> AuctionResponse:
        return AuctionResponse(
            id=str(auction.id),
            title=auction.title,
            description=auction.description,
            category=auction.category,
            starting_price=auction.starting_price,
            current_price=auction.current_price,
            start_date=auction.start_date,
            end_date=auction.end_date,
            owner_id=auction.owner_id,
            status=auction.status,
            created_at=auction.created_at
        )
