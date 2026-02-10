"""
Scheduler status API routes.
"""
from fastapi import APIRouter
from typing import Dict, Any

from app.tasks.scheduler import get_scheduler_status

router = APIRouter(prefix="/api/scheduler", tags=["scheduler"])


@router.get("/status")
async def scheduler_status() -> Dict[str, Any]:
    """
    Get scheduler status and job information.

    Returns:
        Dictionary with scheduler status and jobs
    """
    return get_scheduler_status()
