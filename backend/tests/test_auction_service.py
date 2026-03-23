import pytest
from datetime import datetime, timedelta
from app.models.auction import Auction, AuctionCreate, AuctionStatus
from app.services.auction_service import AuctionService
from app.services.exceptions import NotFoundException, ValidationException
from app.repositories.auction_repository import AuctionRepository

@pytest.mark.asyncio
async def test_create_auction(test_db):
    auction_repo = AuctionRepository(test_db)
    auction_service = AuctionService(auction_repo)
    
    start_date = datetime.utcnow() + timedelta(hours=1)
    end_date = start_date + timedelta(days=7)
    
    auction_data = AuctionCreate(
        title="Test Auction",
        description="Test Description",
        category="Electronics",
        starting_price=100.0,
        start_date=start_date,
        end_date=end_date
    )
    
    auction = await auction_service.create_auction(auction_data, "owner123")
    
    assert auction.title == "Test Auction"
    assert auction.starting_price == 100.0
    assert auction.current_price == 100.0
    assert auction.owner_id == "owner123"

@pytest.mark.asyncio
async def test_create_auction_invalid_dates(test_db):
    auction_repo = AuctionRepository(test_db)
    auction_service = AuctionService(auction_repo)
    
    start_date = datetime.utcnow() + timedelta(days=7)
    end_date = datetime.utcnow() + timedelta(hours=1)
    
    auction_data = AuctionCreate(
        title="Invalid Auction",
        description="Test",
        category="Test",
        starting_price=100.0,
        start_date=start_date,
        end_date=end_date
    )
    
    with pytest.raises(ValidationException):
        await auction_service.create_auction(auction_data, "owner123")
