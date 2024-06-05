from fastapi import APIRouter

from app.user.adapter.input.api.v1.user import user_router as user_v1_router
from app.user.adapter.input.api.v1.user_file import user_file_router as user_file_v1_router
from app.user.adapter.input.api.v1.file import file_router as file_v1_router

router = APIRouter()
router.include_router(user_v1_router, prefix="/api/v1/user", tags=["User"])
router.include_router(user_file_v1_router, prefix="/api/v1/user", tags=["UserFile"])
router.include_router(file_v1_router, prefix="/api/v1", tags=["File"])


__all__ = ["router"]
