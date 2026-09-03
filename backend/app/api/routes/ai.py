"""
The AI-powered endpoints. These are what turn this from a plain
CRUD app into an "AI sales intelligence" product. Each one loads
the relevant data from Postgres, hands it to app/services/ai_service.py,
and saves the AI's answer back onto the Lead/Activity row so the
frontend can just read it like any other field.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.models.lead import Lead
from app.models.activity import Activity
from app.services import ai_service

router = APIRouter(prefix="/api/ai", tags=["ai"])


@router.post("/score-lead/{lead_id}")
async def score_lead(lead_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    lead = db.query(Lead).filter(Lead.id == lead_id, Lead.company_id == current_user.company_id).first()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")

    activities = db.query(Activity).filter(Activity.lead_id == lead.id).order_by(Activity.created_at.desc()).all()
    activity_texts = [f"[{a.type}] {a.content}" for a in activities]

    lead_data = {
        "name": lead.name,
        "company_name": lead.company_name,
        "source": lead.source,
        "status": lead.status.value if hasattr(lead.status, "value") else lead.status,
    }

    result = await ai_service.score_lead(lead_data, activity_texts)

    lead.ai_score = result["score"]
    lead.ai_summary = result["summary"]
    lead.deal_probability = result["deal_probability"]
    lead.next_best_action = result["next_best_action"]
    db.commit()
    db.refresh(lead)

    return {
        "lead_id": str(lead.id),
        "score": lead.ai_score,
        "summary": lead.ai_summary,
        "deal_probability": lead.deal_probability,
        "next_best_action": lead.next_best_action,
    }


@router.post("/summarize-activity/{activity_id}")
async def summarize_activity(activity_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    activity = (
        db.query(Activity)
        .join(Lead, Activity.lead_id == Lead.id)
        .filter(Activity.id == activity_id, Lead.company_id == current_user.company_id)
        .first()
    )
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")

    result = await ai_service.summarize_meeting(activity.content)
    activity.ai_summary = result["summary"]
    activity.ai_sentiment = result["sentiment"]
    db.commit()
    db.refresh(activity)

    return {
        "activity_id": str(activity.id),
        "summary": activity.ai_summary,
        "sentiment": activity.ai_sentiment,
        "key_points": result.get("key_points", []),
    }


@router.post("/draft-email/{lead_id}")
async def draft_email(lead_id: str, context: str = "", db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    lead = db.query(Lead).filter(Lead.id == lead_id, Lead.company_id == current_user.company_id).first()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")

    lead_data = {"name": lead.name, "company_name": lead.company_name}
    email_body = await ai_service.generate_follow_up_email(lead_data, context or lead.ai_summary or "")
    return {"email_body": email_body}
