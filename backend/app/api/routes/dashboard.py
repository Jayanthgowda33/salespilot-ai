"""
Powers the dashboard cards you sketched out: revenue, qualified
leads, conversion rate, average AI score, and open pipeline value.
All numbers are scoped to current_user.company_id.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.models.lead import Lead, LeadStatus
from app.models.deal import Deal, DealStage

router = APIRouter(prefix="/api/dashboard", tags=["dashboard"])


@router.get("/summary")
def dashboard_summary(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    company_id = current_user.company_id

    total_leads = db.query(func.count(Lead.id)).filter(Lead.company_id == company_id).scalar() or 0
    qualified_leads = (
        db.query(func.count(Lead.id))
        .filter(Lead.company_id == company_id, Lead.status == LeadStatus.qualified)
        .scalar() or 0
    )
    won_leads = (
        db.query(func.count(Lead.id))
        .filter(Lead.company_id == company_id, Lead.status == LeadStatus.won)
        .scalar() or 0
    )
    conversion_rate = round((won_leads / total_leads) * 100, 1) if total_leads else 0.0

    revenue = (
        db.query(func.coalesce(func.sum(Deal.value), 0))
        .filter(Deal.company_id == company_id, Deal.stage == DealStage.won)
        .scalar()
    )
    pipeline = (
        db.query(func.coalesce(func.sum(Deal.value), 0))
        .filter(Deal.company_id == company_id, Deal.stage == DealStage.open)
        .scalar()
    )
    avg_ai_score = (
        db.query(func.avg(Lead.ai_score))
        .filter(Lead.company_id == company_id, Lead.ai_score.isnot(None))
        .scalar()
    )

    return {
        "revenue": float(revenue or 0),
        "qualified_leads": qualified_leads,
        "conversion_rate": conversion_rate,
        "avg_ai_score": round(float(avg_ai_score), 1) if avg_ai_score else None,
        "pipeline": float(pipeline or 0),
        "total_leads": total_leads,
    }
