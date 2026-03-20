from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..core.auth import AuthContext, get_auth_context
from ..database import get_db
from ..models.user import User
from ..schemas.user import UserCreate, UserResponse, UserUpdate

router = APIRouter(prefix="/api/users", tags=["Users"])


@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(
    payload: UserCreate,
    db: Session = Depends(get_db),
    auth: AuthContext = Depends(get_auth_context),
):
    existing = db.query(User).filter(User.email == payload.email).first()
    if existing:
        raise HTTPException(status_code=409, detail="Email already registered")
    user = User(**payload.model_dump())
    db.add(user)
    db.flush()
    db.refresh(user)
    return user


@router.get("", response_model=list[UserResponse])
def list_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    auth: AuthContext = Depends(get_auth_context),
):
    return db.query(User).offset(skip).limit(limit).all()


@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    auth: AuthContext = Depends(get_auth_context),
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    payload: UserUpdate,
    db: Session = Depends(get_db),
    auth: AuthContext = Depends(get_auth_context),
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(user, field, value)
    db.flush()
    db.refresh(user)
    return user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    auth: AuthContext = Depends(get_auth_context),
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
