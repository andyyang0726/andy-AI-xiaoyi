"""
推荐管理API
提供需求-供应商匹配推荐功能
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from ..core import get_db, get_current_user_dependency
from ..core.permissions import PermissionChecker, get_permission_checker
from ..models import Demand, Enterprise, User, UserRole, EnterpriseType
from ..schemas import DemandResponse, EnterpriseResponse

router = APIRouter(prefix="/recommendations", tags=["推荐管理"])


@router.get("/my-suppliers")
def get_my_matched_suppliers(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_dependency),
    permissions: PermissionChecker = Depends(get_permission_checker)
):
    """
    获取匹配给我的供应商列表（需求方用户使用）
    
    返回：
    - 我的需求列表
    - 每个需求匹配的供应商信息
    """
    # 只有需求方和管理员可以访问
    if not (permissions.is_demand() or permissions.is_admin()):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="只有需求方企业用户可以查看匹配的供应商"
        )
    
    # 检查用户是否关联企业
    if not current_user.enterprise_id and not permissions.is_admin():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="用户未关联企业"
        )
    
    # 获取用户企业的需求
    query = db.query(Demand)
    
    if permissions.is_demand():
        query = query.filter(Demand.enterprise_id == current_user.enterprise_id)
    
    # 只获取已匹配的需求
    query = query.filter(Demand.match_results.isnot(None))
    query = query.order_by(Demand.created_at.desc())
    
    total = query.count()
    demands = query.offset(skip).limit(limit).all()
    
    # 构建返回数据：需求 + 匹配的供应商
    results = []
    for demand in demands:
        match_results = demand.match_results or []
        
        # 获取匹配的供应商企业信息
        matched_suppliers = []
        for match in match_results[:5]:  # 只取前5个推荐
            supplier_id = match.get('vendor_id')
            if supplier_id:
                supplier = db.query(Enterprise).filter(Enterprise.id == supplier_id).first()
                if supplier:
                    matched_suppliers.append({
                        "enterprise": supplier,
                        "score": match.get('score', 0),
                        "reason": match.get('reason', '')
                    })
        
        results.append({
            "demand": demand,
            "matched_suppliers": matched_suppliers,
            "match_count": len(matched_suppliers)
        })
    
    return {
        "total": total,
        "items": results
    }


@router.get("/my-clients")
def get_my_matched_clients(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_dependency),
    permissions: PermissionChecker = Depends(get_permission_checker)
):
    """
    获取匹配给我的需求客户列表（供应方用户使用）
    
    返回：
    - 推荐给我的需求列表
    - 每个需求的企业信息
    """
    # 只有供应方和管理员可以访问
    if not (permissions.is_supply() or permissions.is_admin()):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="只有供应方企业用户可以查看匹配的需求"
        )
    
    # 检查用户是否关联企业
    if not current_user.enterprise_id and not permissions.is_admin():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="用户未关联企业"
        )
    
    # 验证企业是供应方
    if not permissions.is_admin():
        enterprise = db.query(Enterprise).filter(Enterprise.id == current_user.enterprise_id).first()
        if not enterprise or enterprise.enterprise_type not in [EnterpriseType.SUPPLY, EnterpriseType.BOTH]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="企业类型不是供应方"
            )
    
    # 获取所有已匹配的需求
    query = db.query(Demand).filter(Demand.match_results.isnot(None))
    query = query.order_by(Demand.created_at.desc())
    
    all_demands = query.all()
    
    # 过滤出匹配到当前供应商的需求
    matched_demands = []
    for demand in all_demands:
        match_results = demand.match_results or []
        
        # 检查当前供应商是否在推荐列表中
        for match in match_results:
            if match.get('vendor_id') == current_user.enterprise_id:
                # 获取需求企业信息
                demand_enterprise = db.query(Enterprise).filter(
                    Enterprise.id == demand.enterprise_id
                ).first()
                
                matched_demands.append({
                    "demand": demand,
                    "client_enterprise": demand_enterprise,
                    "match_score": match.get('score', 0),
                    "match_reason": match.get('reason', '')
                })
                break
    
    # 分页
    total = len(matched_demands)
    start = skip
    end = skip + limit
    paginated_results = matched_demands[start:end]
    
    return {
        "total": total,
        "items": paginated_results
    }


@router.get("/admin/all-matches")
def get_all_matches(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    permissions: PermissionChecker = Depends(get_permission_checker)
):
    """
    获取所有匹配情况（管理员专用）
    
    返回所有需求及其匹配的供应商信息
    """
    # 只有管理员可以访问
    if not permissions.is_admin():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="只有管理员可以查看所有匹配情况"
        )
    
    # 获取所有已匹配的需求
    query = db.query(Demand).filter(Demand.match_results.isnot(None))
    query = query.order_by(Demand.created_at.desc())
    
    total = query.count()
    demands = query.offset(skip).limit(limit).all()
    
    # 构建完整的匹配数据
    results = []
    for demand in demands:
        # 获取需求企业信息
        demand_enterprise = db.query(Enterprise).filter(
            Enterprise.id == demand.enterprise_id
        ).first()
        
        match_results = demand.match_results or []
        
        # 获取所有匹配的供应商信息
        matched_suppliers = []
        for match in match_results:
            supplier_id = match.get('vendor_id')
            if supplier_id:
                supplier = db.query(Enterprise).filter(Enterprise.id == supplier_id).first()
                if supplier:
                    matched_suppliers.append({
                        "enterprise": supplier,
                        "score": match.get('score', 0),
                        "reason": match.get('reason', '')
                    })
        
        results.append({
            "demand": demand,
            "demand_enterprise": demand_enterprise,
            "matched_suppliers": matched_suppliers,
            "match_count": len(matched_suppliers)
        })
    
    return {
        "total": total,
        "items": results
    }
