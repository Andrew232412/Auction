from fastapi import APIRouter
from .users import router as users_router
from .auctions import router as auctions_router
from .bids import router as bids_router
from .auth import router as auth_router

api_router = APIRouter(prefix="/api")

api_router.include_router(auth_router, prefix="/auth", tags=["Authentication"])
api_router.include_router(users_router, prefix="/users", tags=["Users"])
api_router.include_router(auctions_router, prefix="/auctions", tags=["Auctions"])
api_router.include_router(bids_router, prefix="/bids", tags=["Bids"])

__all__ = ["api_router"]
