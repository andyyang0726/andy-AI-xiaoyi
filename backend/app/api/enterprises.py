from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List
import random
import string
from ..core import get_db
from ..models import Enterprise, EnterpriseStatus
from ..schemas import (
    EnterpriseCreate,
    EnterpriseUpdate,
    EnterpriseResponse,
    EnterpriseListResponse
)

router = APIRouter(prefix="/enterprises", tags=["企业管理"])


def generate_eid() -> str:
    """生成企业唯一识别码"""
    timestamp = str(int(random.random() * 10000))
    random_str = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    return f"EID-{timestamp}-{random_str}"


@router.post("/register", response_model=EnterpriseResponse, status_code=status.HTTP_201_CREATED)
def register_enterprise(
    enterprise_data: EnterpriseCreate,
    db: Session = Depends(get_db)
):
    """供应商企业注册入驻"""
    # 检查统一社会信用代码是否已存在
    if enterprise_data.credit_code:
        existing = db.query(Enterprise).filter(
            Enterprise.credit_code == enterprise_data.credit_code
        ).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="该企业信用代码已注册，请直接登录"
            )
    
    # 检查企业名称是否已存在
    existing_name = db.query(Enterprise).filter(
        Enterprise.name == enterprise_data.name
    ).first()
    if existing_name:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="该企业名称已注册"
        )
    
    # 创建企业（待审核状态）
    enterprise_dict = enterprise_data.model_dump()
    enterprise_dict['status'] = EnterpriseStatus.PENDING
    enterprise_dict['credit_score'] = 80.0  # 初始信用分
    
    new_enterprise = Enterprise(
        eid=generate_eid(),
        **enterprise_dict
    )
    
    db.add(new_enterprise)
    db.commit()
    db.refresh(new_enterprise)
    
    return new_enterprise


@router.post("", response_model=EnterpriseResponse, status_code=status.HTTP_201_CREATED)
def create_enterprise(
    enterprise_data: EnterpriseCreate,
    db: Session = Depends(get_db)
):
    """创建企业（管理员使用）"""
    # 检查统一社会信用代码是否已存在
    if enterprise_data.credit_code:
        existing = db.query(Enterprise).filter(
            Enterprise.credit_code == enterprise_data.credit_code
        ).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="该企业信用代码已存在"
            )
    
    # 创建企业
    new_enterprise = Enterprise(
        eid=generate_eid(),
        **enterprise_data.model_dump()
    )
    
    db.add(new_enterprise)
    db.commit()
    db.refresh(new_enterprise)
    
    return new_enterprise


@router.get("", response_model=EnterpriseListResponse)
def list_enterprises(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    status_filter: str = Query(None),
    enterprise_type: str = Query(None),
    db: Session = Depends(get_db)
):
    """获取企业列表"""
    query = db.query(Enterprise)
    
    # 应用过滤器
    if status_filter:
        query = query.filter(Enterprise.status == status_filter)
    
    if enterprise_type:
        query = query.filter(Enterprise.enterprise_type == enterprise_type)
    
    total = query.count()
    enterprises = query.offset(skip).limit(limit).all()
    
    return {
        "total": total,
        "items": enterprises
    }


@router.get("/{enterprise_id}", response_model=EnterpriseResponse)
def get_enterprise(enterprise_id: int, db: Session = Depends(get_db)):
    """获取企业详情"""
    enterprise = db.query(Enterprise).filter(Enterprise.id == enterprise_id).first()
    
    if not enterprise:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="企业不存在"
        )
    
    return enterprise


@router.put("/{enterprise_id}", response_model=EnterpriseResponse)
def update_enterprise(
    enterprise_id: int,
    enterprise_data: EnterpriseUpdate,
    db: Session = Depends(get_db)
):
    """更新企业信息"""
    enterprise = db.query(Enterprise).filter(Enterprise.id == enterprise_id).first()
    
    if not enterprise:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="企业不存在"
        )
    
    # 更新字段
    update_data = enterprise_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(enterprise, field, value)
    
    db.commit()
    db.refresh(enterprise)
    
    return enterprise


@router.post("/{enterprise_id}/verify", response_model=EnterpriseResponse)
def verify_enterprise(
    enterprise_id: int,
    approve: bool = Query(..., description="是否通过审核"),
    db: Session = Depends(get_db)
):
    """审核企业"""
    enterprise = db.query(Enterprise).filter(Enterprise.id == enterprise_id).first()
    
    if not enterprise:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="企业不存在"
        )
    
    if approve:
        enterprise.status = EnterpriseStatus.VERIFIED
        enterprise.certification_level = "认证企业"
    else:
        enterprise.status = EnterpriseStatus.REJECTED
    
    db.commit()
    db.refresh(enterprise)
    
    return enterprise


@router.put("/{enterprise_id}/qualification", response_model=EnterpriseResponse)
def submit_qualification(
    enterprise_id: int,
    qualification_data: EnterpriseUpdate,
    db: Session = Depends(get_db)
):
    """提交需求方企业资质信息"""
    from datetime import datetime
    
    enterprise = db.query(Enterprise).filter(Enterprise.id == enterprise_id).first()
    
    if not enterprise:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="企业不存在"
        )
    
    # 检查企业类型
    if enterprise.enterprise_type not in [EnterpriseType.DEMAND, EnterpriseType.BOTH]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="只有需求方企业需要提交资质信息"
        )
    
    # 更新资质信息
    update_data = qualification_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(enterprise, field, value)
    
    # 设置资质状态和提交时间
    enterprise.qualification_status = "pending"
    enterprise.qualification_submitted_at = datetime.utcnow()
    
    db.commit()
    db.refresh(enterprise)
    
    return enterprise


@router.post("/{enterprise_id}/qualification/verify", response_model=EnterpriseResponse)
def verify_qualification(
    enterprise_id: int,
    approve: bool = Query(..., description="是否通过资质审核"),
    db: Session = Depends(get_db)
):
    """审核需求方企业资质（管理员使用）"""
    from datetime import datetime
    
    enterprise = db.query(Enterprise).filter(Enterprise.id == enterprise_id).first()
    
    if not enterprise:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="企业不存在"
        )
    
    if enterprise.qualification_status != "pending":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="资质状态不是待审核"
        )
    
    if approve:
        enterprise.qualification_status = "verified"
        enterprise.qualification_verified_at = datetime.utcnow()
        enterprise.status = EnterpriseStatus.VERIFIED
        enterprise.certification_level = "认证企业"
    else:
        enterprise.qualification_status = "rejected"
    
    db.commit()
    db.refresh(enterprise)
    
    return enterprise


@router.get("/{enterprise_id}/can-create-demand")
def check_can_create_demand(
    enterprise_id: int,
    db: Session = Depends(get_db)
):
    """检查企业是否可以创建需求"""
    enterprise = db.query(Enterprise).filter(Enterprise.id == enterprise_id).first()
    
    if not enterprise:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="企业不存在"
        )
    
    # 检查企业类型
    if enterprise.enterprise_type not in [EnterpriseType.DEMAND, EnterpriseType.BOTH]:
        return {
            "can_create": False,
            "reason": "企业类型不是需求方",
            "qualification_status": None
        }
    
    # 检查资质状态
    qualification_status = enterprise.qualification_status or "unverified"
    
    can_create = qualification_status == "verified"
    
    reason = ""
    if qualification_status == "unverified":
        reason = "企业资质未提交，请先完善企业资质信息"
    elif qualification_status == "pending":
        reason = "企业资质审核中，请等待审核结果"
    elif qualification_status == "rejected":
        reason = "企业资质审核未通过，请重新提交"
    
    return {
        "can_create": can_create,
        "reason": reason,
        "qualification_status": qualification_status,
        "enterprise_name": enterprise.name
    }
