"""
An Activity is anything that happens with a lead: an email, a call,
a meeting, or a note. This is the raw material the AI reads in
order to score leads, summarize meetings, and detect sentiment.
"""

import uuid
import enum
from datetime import datetime
from sqlalchemy import Column, String, DateTime, ForeignKey, Enum, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.database import Base


class ActivityType(str, enum.Enum):
    email = "email"
    call = "call"
    meeting = "meeting"
    note = "note"


class Activity(Base):
    __tablename__ = "activities"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    lead_id = Column(UUID(as_uuid=True), ForeignKey("leads.id"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)  # who logged it

    type = Column(Enum(ActivityType), nullable=False)
    content = Column(Text, nullable=False)  # raw text: email body, call transcript, note, etc.

    # ---- AI-generated fields, filled in after analysis ----
    ai_sentiment = Column(String, nullable=True)   # "positive" / "neutral" / "negative"
    ai_summary = Column(Text, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)

    lead = relationship("Lead", back_populates="activities")
