from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging
import os

from .database import connect_to_mongo, close_mongo_connection, get_database
from .repositories import UserRepository, AuctionRepository, BidRepository
from .api import api_router
from .services.exceptions import ServiceException

os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('logs/app.log')
    ]
)

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting application...")
    await connect_to_mongo()
    
    db = get_database()
    user_repo = UserRepository(db)
    auction_repo = AuctionRepository(db)
    bid_repo = BidRepository(db)
    
    await user_repo.create_indexes()
    await auction_repo.create_indexes()
    await bid_repo.create_indexes()
    
    logger.info("Database indexes created")
    
    yield
    
    logger.info("Shutting down application...")
    await close_mongo_connection()

app = FastAPI(
    title="Auction System API",
    description="REST API for online auction system",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(ServiceException)
async def service_exception_handler(request: Request, exc: ServiceException):
    logger.error(f"Service exception: {exc.message}")
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.__class__.__name__,
            "message": exc.message,
            "details": {}
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "InternalServerError",
            "message": "An unexpected error occurred",
            "details": {}
        }
    )

@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"{request.method} {request.url.path}")
    response = await call_next(request)
    logger.info(f"Response status: {response.status_code}")
    return response

app.include_router(api_router)

@app.get("/", tags=["Health"])
async def root():
    return {"message": "Auction System API", "status": "running"}

@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "healthy"}
