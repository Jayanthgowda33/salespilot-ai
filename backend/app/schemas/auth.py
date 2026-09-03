"""
Pydantic schemas = the shape of data going in and out of the API.
These are what FastAPI uses to validate request bodies and to
control exactly what gets sent back in a response (so we never
accidentally leak a password hash, for example).
"""

from pydantic import BaseModel, EmailStr
import uuid


class SignupRequest(BaseModel):
    company_name: str
    full_name: str
    email: EmailStr
    password: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserOut(BaseModel):
    id: uuid.UUID
    full_name: str
    email: EmailStr
    role: str

    class Config:
        from_attributes = True
