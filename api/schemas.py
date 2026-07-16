# schemas.py
# This file validates data coming FROM the frontend
# Before saving anything to database, we check it here first
# Pydantic library does this validation automatically
# Example: is email in correct format? is password long enough?

from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


# -------------------------------------------------------
# FARMER SCHEMAS
# -------------------------------------------------------

# Used when farmer REGISTERS (data we receive from register form)
class FarmerRegister(BaseModel):
    name     : str          # must be a string
    email    : EmailStr     # must be valid email format like abc@gmail.com
    password : str          # must be a string, min length we check in auth.py


# Used when farmer LOGS IN (data we receive from login form)
class FarmerLogin(BaseModel):
    email    : EmailStr     # valid email
    password : str          # plain password (we will compare with hashed one in DB)


# Used when we SEND farmer data back to frontend
# We never send password back - so no password field here!
class FarmerResponse(BaseModel):
    id         : int
    name       : str
    email      : EmailStr
    created_at : datetime

    class Config:
        from_attributes = True  # allows reading data from SQLAlchemy models directly


# -------------------------------------------------------
# TOKEN SCHEMAS (JWT)
# -------------------------------------------------------

# When farmer logs in successfully, we send back a JWT token
class Token(BaseModel):
    access_token : str      # the actual JWT token string
    token_type   : str      # always "bearer"


# This is the data INSIDE the token (called payload)
class TokenData(BaseModel):
    email : Optional[str] = None   # we store farmer email inside the token


# -------------------------------------------------------
# SCAN HISTORY SCHEMAS
# -------------------------------------------------------

# Used when we SEND scan history back to frontend
class ScanHistoryResponse(BaseModel):
    id         : int
    image_path : str
    result     : str        # Early Blight / Late Blight / Healthy
    confidence : float      # 0.956 means 95.6%
    scanned_at : datetime

    class Config:
        from_attributes = True  # allows reading data from SQLAlchemy models directly
