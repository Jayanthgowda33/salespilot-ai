from pydantic import BaseModel, EmailStr
from typing import Optional
import uuid
import datetime


class LeadCreate(BaseModel):
    name: str
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    company_name: Optional[str] = None
    source: Optional[str] = None


class LeadOut(BaseModel):
    id: uuid.UUID
    name: str
    email: Optional[str]
    phone: Optional[str]
    company_name: Optional[str]
    status: str
    ai_score: Optional[float]
    ai_summary: Optional[str]
    deal_probability: Optional[float]
    next_best_action: Optional[str]
    created_at: datetime.datetime

    class Config:
        from_attributes = True


class ActivityCreate(BaseModel):
    lead_id: uuid.UUID
    type: str          # "email" | "call" | "meeting" | "note"
    content: str
