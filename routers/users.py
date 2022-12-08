import sys
sys.path.append("..")

from fastapi import FastAPI, Depends, HTTPException, status, APIRouter
from pydantic import BaseModel, Field
from typing import Optional
import models
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from database import engine, SessionLocal
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from datetime import datetime, timedelta
from jose import jwt, JWTError
from .auth import get_user_exception, get_current_user, verify_password, get_password_hash


router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "User not found"}}
)

models.Base.metadata.create_all(bind=engine)

# Open and close db after use
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


class UserVerification(BaseModel):
    username: str
    password: str
    new_password: str



# Get all users
@router.get("/")
async def get_all_users(db: Session = Depends(get_db)):
    all_users = db.query(models.Users).all()
    return all_users


# Get user by a path parameter
@router.get("/{user_id}")
async def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.Users).filter(models.Users.id == user_id).first()
    if not user:
        return HTTPException(status_code=404, detail="User not found")
    return user

# Get user by a query parameter
@router.get("/get_user/")
async def query_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.Users).filter(models.Users.id == user_id).first()
    if not user:
        return HTTPException(status_code=404, detail="User not found")
    return user



@router.put("/update_password")
async def update_password(user_verification: UserVerification, user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    if user is None:
        return get_user_exception()

    model_user = db.query(models.Users).filter(models.Users.id == user.get("id")).first()

    if model_user is not None:
        if user_verification.username == model_user.username and verify_password(user_verification.password, model_user.hashed_password):
            model_user.hashed_password = get_password_hash(user_verification.new_password)
            db.add(model_user)
            db.commit()
        return "Sucess"
    return "invalid user or request"


@router.delete("/user")
async def delete_user(user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    if user is None:
        raise get_user_exception()

    user_model = db.query(models.Users).filter(models.Users.id == user.get("id")).first()

    if user_model is None:
        return "Invalid user or request"
    
    db.query(models.Users).filter(models.Users.id == user.get("id")).delete()
    db.commit()

    return "User deleted"
