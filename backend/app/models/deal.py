"""
A Deal is what a Lead turns into once it's a real sales
opportunity with a dollar (or rupee) value attached. The dashboard
revenue and pipeline numbers are calculated from this table.
"""

import uuid
import enum
from datetime import datetime
from sqlalchemy import Column, String, DateTime, ForeignKey, Enum, Numeric
from sqlalchemy.dialects.postgresql import UUID

from app.database import Base


class DealStage(str, enum.Enum):
    open = "open"
    won = "won"
    lost = "lost"


class Deal(Base):
    __tablename__ = "deals"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    company_id = Column(UUID(as_uuid=True), ForeignKey("companies.id"), nullable=False)
    lead_id = Column(UUID(as_uuid=True), ForeignKey("leads.id"), nullable=False)
    owner_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)

    title = Column(String, nullable=False)
    value = Column(Numeric(12, 2), default=0)
    stage = Column(Enum(DealStage), default=DealStage.open)

    created_at = Column(DateTime, default=datetime.utcnow)
    closed_at = Column(DateTime, nullable=True)
