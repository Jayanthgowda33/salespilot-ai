"""
A Lead is a potential customer. This is the central object of the
whole product — AI scores leads, ranks them, and tells reps who to
call first.
"""

import uuid
import enum
from datetime import datetime
from sqlalchemy import Column, String, DateTime, ForeignKey, Enum, Float, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.database import Base


class LeadStatus(str, enum.Enum):
    new = "new"
    contacted = "contacted"
    qualified = "qualified"
    proposal_sent = "proposal_sent"
    won = "won"
    lost = "lost"


class Lead(Base):
    __tablename__ = "leads"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    company_id = Column(UUID(as_uuid=True), ForeignKey("companies.id"), nullable=False)
    workspace_id = Column(UUID(as_uuid=True), ForeignKey("workspaces.id"), nullable=True)
    owner_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)  # assigned sales rep

    name = Column(String, nullable=False)
    email = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    company_name = Column(String, nullable=True)
    source = Column(String, nullable=True)  # e.g. "website", "referral", "cold_call"

    status = Column(Enum(LeadStatus), default=LeadStatus.new)

    # ---- AI-generated fields ----
    ai_score = Column(Float, nullable=True)          # 0-100, how likely to convert
    ai_summary = Column(Text, nullable=True)          # short AI summary of the lead
    deal_probability = Column(Float, nullable=True)   # 0-1, predicted chance of closing
    next_best_action = Column(Text, nullable=True)    # AI recommendation

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    activities = relationship("Activity", back_populates="lead", cascade="all, delete-orphan")
