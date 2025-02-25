from fastapi import APIRouter

from src.api.v1.endpoints import users
from src.api.v1.endpoints import tokens
from src.api.v1.endpoints import friends

api_router = APIRouter()

api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(tokens.router, prefix="/token", tags=["Token"])
api_router.include_router(friends.router, prefix="/friends", tags=["Friends"])