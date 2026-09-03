"""
Company = the top-level tenant. Every account that signs up gets
one Company. Everything else (workspaces, users, leads, deals)
hangs off a company_id, which is how we keep Company A's data
completely separate from Company B's data (multi-tenancy).
"""

import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.database import Base


class Company(Base):
    __tablename__ = "companies"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    users = relationship("User", back_populates="company", cascade="all, delete-orphan")
    workspaces = relationship("Workspace", back_populates="company", cascade="all, delete-orphan")


class Workspace(Base):
    """
    A company can have multiple workspaces (e.g. 'North Sales Team',
    'EMEA Sales Team'). Reps and leads belong to a workspace.
    For a simple MVP you can just create one default workspace per
    company at signup and ignore the rest of this complexity.
    """
    __tablename__ = "workspaces"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    company_id = Column(UUID(as_uuid=True), ForeignKey("companies.id"), nullable=False)
    name = Column(String, nullable=False, default="Default Workspace")
    created_at = Column(DateTime, default=datetime.utcnow)

    company = relationship("Company", back_populates="workspaces")
