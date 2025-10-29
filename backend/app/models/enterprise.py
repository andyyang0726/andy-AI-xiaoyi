from sqlalchemy import Column, Integer, String, Enum, DateTime, JSON, Float
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from ..core.database import Base


class EnterpriseStatus(str, enum.Enum):
    """企业状态"""
    PENDING = "pending"  # 待审核
    VERIFIED = "verified"  # 已认证
    REJECTED = "rejected"  # 已拒绝
    SUSPENDED = "suspended"  # 已暂停


class EnterpriseType(str, enum.Enum):
    """企业类型"""
    DEMAND = "demand"  # 需求方
    SUPPLY = "supply"  # 供应方
    BOTH = "both"  # 双重角色


class Enterprise(Base):
    """企业信息表"""
    __tablename__ = "enterprises"
    
    id = Column(Integer, primary_key=True, index=True)
    eid = Column(String(50), unique=True, index=True, nullable=False)  # 企业唯一识别码
    
    # 基本信息
    name = Column(String(200), nullable=False, index=True)
    credit_code = Column(String(100), unique=True, index=True)  # 统一社会信用代码
    legal_person = Column(String(100))  # 法人代表
    
    # 分类信息
    enterprise_type = Column(Enum(EnterpriseType), default=EnterpriseType.DEMAND)
    industry_tags = Column(JSON, default=list)  # 行业标签列表
    size = Column(String(50))  # 企业规模：小型/中型/大型
    
    # 联系信息
    contact_person = Column(String(100))
    contact_phone = Column(String(20))
    contact_email = Column(String(100))
    address = Column(String(500))
    
    # 业务信息
    business_scope = Column(String(2000))  # 主营业务
    ai_capabilities = Column(JSON, default=list)  # AI相关能力标签
    
    # 供应商详细信息（供应方企业专用）
    capability_details = Column(JSON, default=list)  # AI能力详情列表
    industry_experience = Column(JSON, default=list)  # 行业经验列表
    success_cases = Column(JSON, default=list)  # 成功案例列表
    team_size = Column(Integer, default=0)  # 团队规模
    team_structure = Column(String(500))  # 团队构成
    certifications = Column(JSON, default=list)  # 认证资质
    
    # 需求方资质信息（需求方企业专用）
    qualification_status = Column(String(50), default="unverified")  # 资质状态：unverified/pending/verified/rejected
    qualification_data = Column(JSON, default=dict)  # 资质详细数据
    qualification_submitted_at = Column(DateTime)  # 资质提交时间
    qualification_verified_at = Column(DateTime)  # 资质审核通过时间
    established_year = Column(String(10))  # 成立年份
    main_products = Column(String(500))  # 主要产品/服务
    annual_revenue = Column(String(50))  # 年营业额
    employee_count = Column(Integer, default=0)  # 员工人数
    
    # 认证信息
    status = Column(Enum(EnterpriseStatus), default=EnterpriseStatus.PENDING)
    certification_level = Column(String(50), default="普通会员")  # 普通会员/认证企业/优选企业
    
    # 信用信息
    credit_score = Column(Float, default=80.0)  # 信用分，默认80分
    
    # 时间戳
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关系
    users = relationship("User", back_populates="enterprise")
    demands = relationship("Demand", back_populates="enterprise")
