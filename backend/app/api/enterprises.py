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


@router.post("", response_model=EnterpriseResponse, status_code=status.HTTP_201_CREATED)
def create_enterprise(
    enterprise_data: EnterpriseCreate,
    db: Session = Depends(get_db)
):
    """创建企业"""
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
