"""
Background tasks. Right now there's one example task: re-score
every lead for a company. This is the kind of thing you'd trigger
on a nightly schedule (via Celery beat) or after a bulk import.

This file uses asyncio.run because ai_service functions are async
but Celery tasks are sync — that's the standard bridge between them.
"""

import asyncio
from app.celery_app import celery_app
from app.database import SessionLocal
from app.models.lead import Lead
from app.models.activity import Activity
from app.services import ai_service


@celery_app.task
def rescore_all_leads(company_id: str):
    db = SessionLocal()
    try:
        leads = db.query(Lead).filter(Lead.company_id == company_id).all()
        for lead in leads:
            activities = db.query(Activity).filter(Activity.lead_id == lead.id).all()
            activity_texts = [f"[{a.type}] {a.content}" for a in activities]
            lead_data = {
                "name": lead.name,
                "company_name": lead.company_name,
                "source": lead.source,
                "status": lead.status.value if hasattr(lead.status, "value") else lead.status,
            }
            result = asyncio.run(ai_service.score_lead(lead_data, activity_texts))
            lead.ai_score = result["score"]
            lead.ai_summary = result["summary"]
            lead.deal_probability = result["deal_probability"]
            lead.next_best_action = result["next_best_action"]
        db.commit()
    finally:
        db.close()
