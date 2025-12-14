from fastapi import APIRouter

from app.api.v1.endpoints import sessions_router, questions_router, groups_router

router = APIRouter(prefix="/api/v1")
router.include_router(sessions_router)
router.include_router(questions_router)
router.include_router(groups_router)
