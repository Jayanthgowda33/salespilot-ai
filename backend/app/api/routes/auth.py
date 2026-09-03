"""
Signup and login. Signup creates a brand new Company plus its
first admin User in one step (this is how a new customer of your
SaaS gets started). Login just checks the password and hands back
a JWT.

Google OAuth is stubbed with a clear TODO — wiring it up fully
needs a registered app in Google Cloud Console, which only you can
create, so the code here is ready to plug your client ID into.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.company import Company, Workspace
from app.models.user import User, UserRole
from app.schemas.auth import SignupRequest, TokenResponse, UserOut
from app.core.security import hash_password, verify_password, create_access_token

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/signup", response_model=TokenResponse)
def signup(payload: SignupRequest, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == payload.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    company = Company(name=payload.company_name)
    db.add(company)
    db.flush()  # gets company.id before commit

    workspace = Workspace(company_id=company.id, name="Default Workspace")
    db.add(workspace)
    db.flush()

    user = User(
        company_id=company.id,
        workspace_id=workspace.id,
        full_name=payload.full_name,
        email=payload.email,
        hashed_password=hash_password(payload.password),
        role=UserRole.admin,
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    token = create_access_token({"sub": str(user.id), "company_id": str(company.id)})
    return TokenResponse(access_token=token)


@router.post("/login", response_model=TokenResponse)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # OAuth2PasswordRequestForm sends "username" for the email field
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not user.hashed_password or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")

    token = create_access_token({"sub": str(user.id), "company_id": str(user.company_id)})
    return TokenResponse(access_token=token)


# TODO: Google OAuth flow.
# 1. Register your app at https://console.cloud.google.com and get a client ID/secret.
# 2. Frontend redirects to Google's consent screen and gets a code back.
# 3. This backend exchanges the code for the user's email via Google's token endpoint.
# 4. Find-or-create a User with that email (same as signup, but hashed_password stays null).
# 5. Issue the same JWT as above.
# Use the `authlib` package (already in requirements.txt) to keep this short.
