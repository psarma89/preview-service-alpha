from datetime import datetime

from pydantic import BaseModel


class UserBase(BaseModel):
    email: str
    name: str
    bio: str | None = None


class UserCreate(UserBase):
    pass


class UserUpdate(BaseModel):
    email: str | None = None
    name: str | None = None
    bio: str | None = None


class UserResponse(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
