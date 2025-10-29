from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from datetime import datetime
from ..models.enterprise import EnterpriseStatus, EnterpriseType


class EnterpriseBase(BaseModel):
    """企业基础信息"""
    name: str = Field(..., min_length=2, max_length=200)
    credit_code: Optional[str] = Field(None, max_length=100)
    legal_person: Optional[str] = Field(None, max_length=100)
    enterprise_type: EnterpriseType = EnterpriseType.DEMAND
    industry_tags: List[str] = Field(default_factory=list)
    size: Optional[str] = None
    contact_person: Optional[str] = None
    contact_phone: Optional[str] = None
    contact_email: Optional[EmailStr] = None
    address: Optional[str] = None
    business_scope: Optional[str] = None
    ai_capabilities: List[str] = Field(default_factory=list)
    
    # 供应商详细信息
    capability_details: Optional[List[dict]] = Field(default_factory=list)
    industry_experience: Optional[List[dict]] = Field(default_factory=list)
    success_cases: Optional[List[dict]] = Field(default_factory=list)
    team_size: Optional[int] = 0
    team_structure: Optional[str] = None
    certifications: Optional[List[dict]] = Field(default_factory=list)
    
    # 需求方资质信息
    qualification_status: Optional[str] = "unverified"
    qualification_data: Optional[dict] = Field(default_factory=dict)
    established_year: Optional[str] = None
    main_products: Optional[str] = None
    annual_revenue: Optional[str] = None
    employee_count: Optional[int] = 0


class EnterpriseCreate(EnterpriseBase):
    """创建企业"""
    pass


class EnterpriseUpdate(BaseModel):
    """更新企业"""
    name: Optional[str] = None
    legal_person: Optional[str] = None
    industry_tags: Optional[List[str]] = None
    size: Optional[str] = None
    contact_person: Optional[str] = None
    contact_phone: Optional[str] = None
    contact_email: Optional[EmailStr] = None
    address: Optional[str] = None
    business_scope: Optional[str] = None
    ai_capabilities: Optional[List[str]] = None
    capability_details: Optional[List[dict]] = None
    industry_experience: Optional[List[dict]] = None
    success_cases: Optional[List[dict]] = None
    team_size: Optional[int] = None
    team_structure: Optional[str] = None
    certifications: Optional[List[dict]] = None
    qualification_status: Optional[str] = None
    qualification_data: Optional[dict] = None
    established_year: Optional[str] = None
    main_products: Optional[str] = None
    annual_revenue: Optional[str] = None
    employee_count: Optional[int] = None


class EnterpriseResponse(EnterpriseBase):
    """企业响应"""
    id: int
    eid: str
    status: EnterpriseStatus
    certification_level: str
    credit_score: float
    qualification_status: Optional[str] = None
    qualification_submitted_at: Optional[datetime] = None
    qualification_verified_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class EnterpriseListResponse(BaseModel):
    """企业列表响应"""
    total: int
    items: List[EnterpriseResponse]
