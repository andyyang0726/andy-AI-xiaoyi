from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from ..core.database import Base


class UserRole(str, enum.Enum):
    """用户角色"""
    ADMIN = "admin"  # 平台管理员
    ENTERPRISE_ADMIN = "enterprise_admin"  # 企业管理员
    ENTERPRISE_USER = "enterprise_user"  # 企业普通用户
    EXPERT = "expert"  # 行业专家


class User(Base):
    """用户表"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # 基本信息
    email = Column(String(100), unique=True, index=True, nullable=False)
    phone = Column(String(20), unique=True, index=True)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(100))
    
    # 角色与权限
    role = Column(Enum(UserRole), default=UserRole.ENTERPRISE_USER)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    
    # 企业关联
    enterprise_id = Column(Integer, ForeignKey("enterprises.id"), nullable=True)
    
    # 时间戳
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = Column(DateTime, nullable=True)
    
    # 关系
    enterprise = relationship("Enterprise", back_populates="users")
