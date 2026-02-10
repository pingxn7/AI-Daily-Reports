"""
API routes for managing monitored Twitter accounts.
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from app.database import get_db
from app.models.monitored_account import MonitoredAccount
from pydantic import BaseModel, Field


router = APIRouter(prefix="/api/accounts", tags=["accounts"])


# Schemas
class MonitoredAccountCreate(BaseModel):
    """Schema for creating a monitored account."""
    user_id: Optional[str] = Field(None, description="Twitter user ID (optional, will be fetched if not provided)")
    username: str = Field(..., description="Twitter username (without @)")
    display_name: Optional[str] = Field(None, description="Display name (optional, will be fetched if not provided)")
    is_active: bool = Field(True, description="Whether to actively monitor this account")


class MonitoredAccountUpdate(BaseModel):
    """Schema for updating a monitored account."""
    username: Optional[str] = Field(None, description="Twitter username")
    display_name: Optional[str] = Field(None, description="Display name")
    is_active: Optional[bool] = Field(None, description="Whether to actively monitor this account")


class MonitoredAccountResponse(BaseModel):
    """Schema for monitored account response."""
    id: int
    user_id: str
    username: str
    display_name: Optional[str]
    is_active: bool
    last_tweet_id: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


@router.get("", response_model=List[MonitoredAccountResponse])
async def list_accounts(
    is_active: Optional[bool] = Query(None, description="Filter by active status"),
    db: Session = Depends(get_db)
):
    """
    List all monitored accounts.
    """
    query = db.query(MonitoredAccount)

    if is_active is not None:
        query = query.filter(MonitoredAccount.is_active == is_active)

    accounts = query.order_by(MonitoredAccount.username).all()
    return accounts


@router.get("/{account_id}", response_model=MonitoredAccountResponse)
async def get_account(
    account_id: int,
    db: Session = Depends(get_db)
):
    """
    Get a specific monitored account by ID.
    """
    account = db.query(MonitoredAccount).filter(MonitoredAccount.id == account_id).first()

    if not account:
        raise HTTPException(status_code=404, detail="Account not found")

    return account


@router.post("", response_model=MonitoredAccountResponse, status_code=201)
async def create_account(
    account_data: MonitoredAccountCreate,
    db: Session = Depends(get_db)
):
    """
    Add a new monitored account.

    You can provide just the username, and the system will automatically fetch
    the user_id and display_name from Twitter API.
    """
    from app.services.twitter_collector import twitter_collector

    # If user_id is not provided, fetch it from Twitter API
    if not account_data.user_id:
        user_info = await twitter_collector.fetch_user_by_username(account_data.username)

        if not user_info:
            raise HTTPException(
                status_code=404,
                detail=f"Twitter user @{account_data.username} not found"
            )

        account_data.user_id = user_info["user_id"]

        # Also update display_name if not provided
        if not account_data.display_name:
            account_data.display_name = user_info["display_name"]

    # Check if account already exists
    existing = db.query(MonitoredAccount).filter(
        (MonitoredAccount.user_id == account_data.user_id) |
        (MonitoredAccount.username == account_data.username)
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail=f"Account already exists: @{existing.username}"
        )

    # Create new account
    account = MonitoredAccount(
        user_id=account_data.user_id,
        username=account_data.username,
        display_name=account_data.display_name,
        is_active=account_data.is_active
    )

    db.add(account)
    db.commit()
    db.refresh(account)

    return account


@router.put("/{account_id}", response_model=MonitoredAccountResponse)
async def update_account(
    account_id: int,
    account_data: MonitoredAccountUpdate,
    db: Session = Depends(get_db)
):
    """
    Update a monitored account.
    """
    account = db.query(MonitoredAccount).filter(MonitoredAccount.id == account_id).first()

    if not account:
        raise HTTPException(status_code=404, detail="Account not found")

    # Update fields
    if account_data.username is not None:
        # Check if username is already taken by another account
        existing = db.query(MonitoredAccount).filter(
            MonitoredAccount.username == account_data.username,
            MonitoredAccount.id != account_id
        ).first()
        if existing:
            raise HTTPException(
                status_code=400,
                detail=f"Username already taken: @{account_data.username}"
            )
        account.username = account_data.username

    if account_data.display_name is not None:
        account.display_name = account_data.display_name

    if account_data.is_active is not None:
        account.is_active = account_data.is_active

    account.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(account)

    return account


@router.delete("/{account_id}", status_code=204)
async def delete_account(
    account_id: int,
    db: Session = Depends(get_db)
):
    """
    Delete a monitored account.
    """
    account = db.query(MonitoredAccount).filter(MonitoredAccount.id == account_id).first()

    if not account:
        raise HTTPException(status_code=404, detail="Account not found")

    db.delete(account)
    db.commit()

    return None


@router.post("/batch", response_model=dict)
async def create_accounts_batch(
    accounts: List[MonitoredAccountCreate],
    db: Session = Depends(get_db)
):
    """
    Add multiple monitored accounts at once.

    You can provide just the usernames, and the system will automatically fetch
    the user_id and display_name from Twitter API.
    """
    from app.services.twitter_collector import twitter_collector

    added = []
    skipped = []
    errors = []

    for account_data in accounts:
        try:
            # If user_id is not provided, fetch it from Twitter API
            if not account_data.user_id:
                user_info = await twitter_collector.fetch_user_by_username(account_data.username)

                if not user_info:
                    errors.append({
                        "username": account_data.username,
                        "error": "Twitter user not found"
                    })
                    continue

                account_data.user_id = user_info["user_id"]

                # Also update display_name if not provided
                if not account_data.display_name:
                    account_data.display_name = user_info["display_name"]

            # Check if account already exists
            existing = db.query(MonitoredAccount).filter(
                (MonitoredAccount.user_id == account_data.user_id) |
                (MonitoredAccount.username == account_data.username)
            ).first()

            if existing:
                skipped.append({
                    "username": account_data.username,
                    "reason": "Already exists"
                })
                continue

            # Create new account
            account = MonitoredAccount(
                user_id=account_data.user_id,
                username=account_data.username,
                display_name=account_data.display_name,
                is_active=account_data.is_active
            )

            db.add(account)
            added.append(account_data.username)

        except Exception as e:
            errors.append({
                "username": account_data.username,
                "error": str(e)
            })

    db.commit()

    return {
        "added": len(added),
        "skipped": len(skipped),
        "errors": len(errors),
        "details": {
            "added": added,
            "skipped": skipped,
            "errors": errors
        }
    }
