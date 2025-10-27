from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from ..core import get_db
from ..models import Demand, DemandStatus, Enterprise
from ..schemas import (
    DemandCreate,
    DemandUpdate,
    DemandResponse,
    DemandListResponse,
    DemandEvaluateRequest,
    DemandEvaluateResponse
)
from ..services import evaluation_service, matching_service

router = APIRouter(prefix="/demands", tags=["需求管理"])


@router.post("", response_model=DemandResponse, status_code=status.HTTP_201_CREATED)
def create_demand(
    demand_data: DemandCreate,
    db: Session = Depends(get_db)
):
    """创建需求"""
    # 验证企业是否存在
    enterprise = db.query(Enterprise).filter(
        Enterprise.id == demand_data.enterprise_id
    ).first()
    
    if not enterprise:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="企业不存在"
        )
    
    # 创建需求
    new_demand = Demand(**demand_data.model_dump())
    
    db.add(new_demand)
    db.commit()
    db.refresh(new_demand)
    
    return new_demand


@router.get("", response_model=DemandListResponse)
def list_demands(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    status_filter: Optional[str] = Query(None),
    enterprise_id: Optional[int] = Query(None),
    db: Session = Depends(get_db)
):
    """获取需求列表"""
    query = db.query(Demand)
    
    # 应用过滤器
    if status_filter:
        query = query.filter(Demand.status == status_filter)
    
    if enterprise_id:
        query = query.filter(Demand.enterprise_id == enterprise_id)
    
    # 按创建时间倒序
    query = query.order_by(Demand.created_at.desc())
    
    total = query.count()
    demands = query.offset(skip).limit(limit).all()
    
    return {
        "total": total,
        "items": demands
    }


@router.get("/{demand_id}", response_model=DemandResponse)
def get_demand(demand_id: int, db: Session = Depends(get_db)):
    """获取需求详情"""
    demand = db.query(Demand).filter(Demand.id == demand_id).first()
    
    if not demand:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="需求不存在"
        )
    
    return demand


@router.put("/{demand_id}", response_model=DemandResponse)
def update_demand(
    demand_id: int,
    demand_data: DemandUpdate,
    db: Session = Depends(get_db)
):
    """更新需求"""
    demand = db.query(Demand).filter(Demand.id == demand_id).first()
    
    if not demand:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="需求不存在"
        )
    
    # 更新字段
    update_data = demand_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(demand, field, value)
    
    db.commit()
    db.refresh(demand)
    
    return demand


@router.post("/{demand_id}/submit", response_model=DemandResponse)
def submit_demand(demand_id: int, db: Session = Depends(get_db)):
    """提交需求"""
    demand = db.query(Demand).filter(Demand.id == demand_id).first()
    
    if not demand:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="需求不存在"
        )
    
    demand.status = DemandStatus.SUBMITTED
    demand.submitted_at = datetime.utcnow()
    
    db.commit()
    db.refresh(demand)
    
    return demand


@router.post("/{demand_id}/evaluate", response_model=DemandEvaluateResponse)
def evaluate_demand(demand_id: int, db: Session = Depends(get_db)):
    """评估需求"""
    demand = db.query(Demand).filter(Demand.id == demand_id).first()
    
    if not demand:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="需求不存在"
        )
    
    # 准备评估数据
    demand_dict = {
        "title": demand.title,
        "description": demand.description,
        "industry_tags": demand.industry_tags or [],
        "scenario_tags": demand.scenario_tags or [],
        "kpis": demand.kpis or [],
        "budget_min": demand.budget_min,
        "budget_max": demand.budget_max,
        "timeline_start": demand.timeline_start,
        "timeline_end": demand.timeline_end,
        "data_summary": demand.data_summary or {},
        "confidentiality": demand.confidentiality.value if demand.confidentiality else "internal"
    }
    
    # 执行评估
    evaluation_result = evaluation_service.evaluate_demand(demand_dict)
    
    # 更新需求状态和评估结果
    demand.status = DemandStatus.EVALUATED
    demand.evaluation_result = evaluation_result
    
    db.commit()
    db.refresh(demand)
    
    return {
        "demand_id": demand.id,
        "evaluation": evaluation_result,
        "message": "需求评估完成"
    }


@router.post("/{demand_id}/match", response_model=DemandResponse)
def match_demand(
    demand_id: int,
    top_k: int = Query(5, ge=1, le=20),
    db: Session = Depends(get_db)
):
    """匹配供应商"""
    demand = db.query(Demand).filter(Demand.id == demand_id).first()
    
    if not demand:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="需求不存在"
        )
    
    # 准备匹配数据
    demand_dict = {
        "title": demand.title,
        "description": demand.description,
        "industry_tags": demand.industry_tags or [],
        "scenario_tags": demand.scenario_tags or [],
        "budget_max": demand.budget_max or 0,
        "enterprise_location": "重庆"  # MVP阶段默认重庆
    }
    
    # 执行匹配
    match_results = matching_service.match_vendors(demand_dict, db, top_k)
    
    # 更新需求的匹配结果
    demand.match_results = match_results
    demand.status = DemandStatus.MATCHED
    
    db.commit()
    db.refresh(demand)
    
    return demand


@router.get("/recommended/{enterprise_id}")
def get_recommended_demands(
    enterprise_id: int,
    top_k: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db)
):
    """
    为供应商企业推荐匹配的需求
    
    Args:
        enterprise_id: 供应商企业ID
        top_k: 返回top K个推荐结果
        db: 数据库会话
        
    Returns:
        推荐需求列表
    """
    # 验证企业是否存在且为供应方
    enterprise = db.query(Enterprise).filter(
        Enterprise.id == enterprise_id
    ).first()
    
    if not enterprise:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="企业不存在"
        )
    
    from ..models import EnterpriseType
    if enterprise.enterprise_type not in [EnterpriseType.SUPPLY, EnterpriseType.BOTH]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="只有供应方企业可以获取需求推荐"
        )
    
    # 获取推荐需求
    recommended_demands = matching_service.match_demands_for_vendor(
        vendor=enterprise,
        db=db,
        top_k=top_k
    )
    
    return {
        "enterprise_id": enterprise_id,
        "enterprise_name": enterprise.name,
        "total": len(recommended_demands),
        "recommendations": recommended_demands
    }


@router.delete("/{demand_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_demand(demand_id: int, db: Session = Depends(get_db)):
    """删除需求"""
    demand = db.query(Demand).filter(Demand.id == demand_id).first()
    
    if not demand:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="需求不存在"
        )
    
    db.delete(demand)
    db.commit()
    
    return None
