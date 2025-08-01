from pydantic import BaseModel, EmailStr, constr
from enum import Enum
from typing import Optional, List

class SubscriptionTierEnum(str, Enum):
    FREE = "FREE"
    STANDARD = "STANDARD"
    PREMIUM = "PREMIUM"

class TenantBase(BaseModel):
    name: constr(strip_whitespace=True, min_length=1)

class TenantCreate(TenantBase):
    pass

class TenantUpdate(BaseModel):
    name: Optional[constr(strip_whitespace=True, min_length=1)] = None

class TenantRead(TenantBase):
    id: int
    class Config:
        orm_mode = True

class UserBase(BaseModel):
    email: EmailStr
    full_name: constr(strip_whitespace=True, min_length=1)
    subscription_tier: SubscriptionTierEnum

class UserCreate(UserBase):
    tenant_id: int

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[constr(strip_whitespace=True, min_length=1)] = None
    subscription_tier: Optional[SubscriptionTierEnum] = None

class UserRead(UserBase):
    id: int
    tenant_id: int
    class Config:
        orm_mode = True
