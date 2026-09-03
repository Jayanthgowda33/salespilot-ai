"""
CRUD for leads and activities. Every single query here filters by
current_user.company_id — that one line is what keeps Company A
from ever seeing Company B's data. If you add new routes later,
copy this pattern every time.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.models.lead import Lead
from app.models.activity import Activity
from app.schemas.lead import LeadCreate, LeadOut, ActivityCreate

router = APIRouter(prefix="/api/leads", tags=["leads"])


@router.post("", response_model=LeadOut)
def create_lead(payload: LeadCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    lead = Lead(
        company_id=current_user.company_id,
        workspace_id=current_user.workspace_id,
        owner_id=current_user.id,
        **payload.model_dump(),
    )
    db.add(lead)
    db.commit()
    db.refresh(lead)
    return lead


@router.get("", response_model=List[LeadOut])
def list_leads(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return (
        db.query(Lead)
        .filter(Lead.company_id == current_user.company_id)
        .order_by(Lead.ai_score.desc().nullslast(), Lead.created_at.desc())
        .all()
    )


@router.get("/{lead_id}", response_model=LeadOut)
def get_lead(lead_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    lead = db.query(Lead).filter(Lead.id == lead_id, Lead.company_id == current_user.company_id).first()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    return lead


@router.post("/activities")
def add_activity(payload: ActivityCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # confirm the lead belongs to this company before attaching an activity to it
    lead = db.query(Lead).filter(Lead.id == payload.lead_id, Lead.company_id == current_user.company_id).first()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")

    activity = Activity(
        lead_id=payload.lead_id,
        user_id=current_user.id,
        type=payload.type,
        content=payload.content,
    )
    db.add(activity)
    db.commit()
    db.refresh(activity)
    return {"id": str(activity.id), "message": "Activity logged"}
