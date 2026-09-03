"""
Entry point. Run this with:
    uvicorn app.main:app --reload
from inside the backend/ folder (with your virtualenv active).

This file just wires the pieces together: CORS so the React app
can call it, and each router file from app/api/routes/.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine
from app import models  # noqa: F401  (importing registers all tables with Base)
from app.api.routes import auth, leads, ai, dashboard

app = FastAPI(title="SalesPilot AI", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite's default dev port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(leads.router)
app.include_router(ai.router)
app.include_router(dashboard.router)


@app.on_event("startup")
def on_startup():
    # For local dev only: creates tables directly from the models.
    # Once you set up Alembic properly, replace this with migrations
    # (`alembic upgrade head`) instead of create_all.
    Base.metadata.create_all(bind=engine)


@app.get("/")
def root():
    return {"status": "SalesPilot AI backend is running"}
