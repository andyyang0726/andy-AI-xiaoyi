from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime
from ..models.user import UserRole


class UserBase(BaseModel):
    """用户基础信息"""
    email: EmailStr
    phone: Optional[str] = None
    full_name: Optional[str] = None
    role: UserRole = UserRole.ENTERPRISE_USER


class UserCreate(UserBase):
    """创建用户"""
    password: str = Field(..., min_length=6)
    enterprise_id: Optional[int] = None


class UserLogin(BaseModel):
    """用户登录"""
    email: EmailStr
    password: str


class UserResponse(UserBase):
    """用户响应"""
    id: int
    is_active: bool
    is_superuser: bool
    enterprise_id: Optional[int] = None
    created_at: datetime
    last_login: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class Token(BaseModel):
    """Token响应"""
    access_token: str
    token_type: str = "bearer"
    user: UserResponse


class TokenData(BaseModel):
    """Token数据"""
    user_id: Optional[int] = None
    email: Optional[str] = None
