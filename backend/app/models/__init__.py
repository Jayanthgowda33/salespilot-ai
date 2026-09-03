# Importing every model here so that Base.metadata knows about all
# of them when Alembic (or create_all) builds the database tables.
from app.models.company import Company, Workspace
from app.models.user import User, UserRole
from app.models.lead import Lead, LeadStatus
from app.models.activity import Activity, ActivityType
from app.models.deal import Deal, DealStage
