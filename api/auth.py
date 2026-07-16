# auth.py
# This file handles everything related to authentication
# 1. Register a new farmer
# 2. Login an existing farmer
# 3. Hash passwords (never store plain text passwords)
# 4. Create JWT tokens (so farmer stays logged in)
# 5. Verify JWT tokens (to protect private routes)
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional

from api.database import get_db
from api.models import Farmer
from api.schemas import FarmerRegister, FarmerLogin, FarmerResponse, Token, TokenData

# -------------------------------------------------------
# SECURITY SETTINGS
# Change SECRET_KEY to any long random string you want
# This key is used to sign JWT tokens - keep it secret!
# -------------------------------------------------------
SECRET_KEY = "grootify_secret_key_potato_2026" 
GOOGLE_CLIENT_ID = "82309149742-nrrrmnu18fhi4tqvtgd486ule2rca90h.apps.googleusercontent.com"  # paste your client ID here # change this to something random
ALGORITHM = "HS256"                              # the algorithm to encode JWT
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24           # token expires after 24 hours


# -------------------------------------------------------
# PASSWORD HASHING
# bcrypt = a secure way to hash passwords
# When farmer registers: plain password → hashed password saved in DB
# When farmer logs in: plain password compared with hashed password
# -------------------------------------------------------
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    # converts plain password to hashed version
    # example: "mypassword123" → "$2b$12$abc...xyz" (unreadable)
    return pwd_context.hash(password[:72])

def verify_password(plain_password: str, hashed_password: str) -> bool:
    # checks if plain password matches the hashed one in database
    # returns True if match, False if wrong password
    return pwd_context.verify(plain_password, hashed_password)


# -------------------------------------------------------
# JWT TOKEN FUNCTIONS
# JWT = JSON Web Token
# It's like a digital ID card for the farmer
# After login, farmer gets this token
# They send this token with every request to prove who they are
# -------------------------------------------------------
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()

    # set expiry time for token
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})   # add expiry to token data

    # create the actual JWT token string
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str) -> Optional[str]:
    # decode the JWT token and get the farmer email from it
    # if token is invalid or expired, return None
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")   # "sub" = subject = farmer email
        if email is None:
            return None
        return email
    except JWTError:
        return None


# -------------------------------------------------------
# API ROUTER
# Instead of putting routes in main.py, we use a router
# This keeps code clean and organized
# In main.py we will just include this router
# -------------------------------------------------------
router = APIRouter(
    prefix="/auth",     # all routes here start with /auth
    tags=["auth"]       # groups them in API docs
)


# -------------------------------------------------------
# ROUTE 1: REGISTER
# POST /auth/register
# Farmer sends: name, email, password
# We check: email not already used, password min 6 chars
# We save: farmer to database with hashed password
# We return: farmer info + JWT token
# -------------------------------------------------------
@router.post("/register", response_model=Token)
def register(farmer_data: FarmerRegister, db: Session = Depends(get_db)):

    # check if email already exists in database
    existing_farmer = db.query(Farmer).filter(Farmer.email == farmer_data.email).first()
    if existing_farmer:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered. Please login instead."
        )

    # check password length (minimum 6 characters)
    if len(farmer_data.password) < 6:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must be at least 6 characters long."
        )

    # hash the password before saving
    hashed_pw = hash_password(farmer_data.password)

    # create new farmer object
    new_farmer = Farmer(
        name     = farmer_data.name,
        email    = farmer_data.email,
        password = hashed_pw          # save hashed password, never plain text!
    )

    # save farmer to database
    db.add(new_farmer)
    db.commit()
    db.refresh(new_farmer)   # refresh to get the auto-generated ID

    # create JWT token for this farmer
    access_token = create_access_token(data={"sub": new_farmer.email})

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


# -------------------------------------------------------
# ROUTE 2: LOGIN
# POST /auth/login
# Farmer sends: email, password
# We check: email exists, password is correct
# We return: JWT token
# -------------------------------------------------------
@router.post("/login", response_model=Token)
def login(farmer_data: FarmerLogin, db: Session = Depends(get_db)):

    # find farmer by email
    farmer = db.query(Farmer).filter(Farmer.email == farmer_data.email).first()

    # if farmer not found OR password wrong, return error
    # we give same error for both cases for security
    # (don't tell hackers which one is wrong)
    if not farmer or not verify_password(farmer_data.password, farmer.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
            headers={"WWW-Authenticate": "Bearer"}
        )

    # create JWT token for this farmer
    access_token = create_access_token(data={"sub": farmer.email})

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


# -------------------------------------------------------
# ROUTE 3: GET CURRENT FARMER (who is logged in?)
# GET /auth/me
# Farmer sends their JWT token in header
# We decode token and return their info
# -------------------------------------------------------
from fastapi.security import OAuth2PasswordBearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_farmer(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    # this function is used to PROTECT routes
    # any route that needs login will use this as dependency

    email = verify_token(token)

    if email is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token. Please login again.",
            headers={"WWW-Authenticate": "Bearer"}
        )

    # get farmer from database using email from token
    farmer = db.query(Farmer).filter(Farmer.email == email).first()

    if farmer is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Farmer not found."
        )

    return farmer


@router.get("/me", response_model=FarmerResponse)
def get_me(current_farmer: Farmer = Depends(get_current_farmer)):
    # returns the currently logged in farmer's info
    return current_farmer
@router.post("/google")
def google_login(token_data: dict, db: Session = Depends(get_db)):
    try:
        # verify google token
        idinfo = id_token.verify_oauth2_token(
            token_data["token"],
            google_requests.Request(),
            GOOGLE_CLIENT_ID
        )

        email = idinfo["email"]
        name  = idinfo["name"]

        # check if farmer already exists
        farmer = db.query(Farmer).filter(Farmer.email == email).first()

        # if not exists, create new farmer automatically
        if not farmer:
            farmer = Farmer(
                name     = name,
                email    = email,
                password = hash_password("google_oauth_user")
            )
            db.add(farmer)
            db.commit()
            db.refresh(farmer)

        # create JWT token
        access_token = create_access_token(data={"sub": farmer.email})

        return {
            "access_token": access_token,
            "token_type"  : "bearer",
            "farmer_name" : farmer.name
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Google token"
        )