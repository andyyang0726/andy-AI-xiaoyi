"""
权限控制模块
提供基于角色的访问控制(RBAC)功能
"""
from functools import wraps
from fastapi import HTTPException, status, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
from .database import get_db
from ..models.user import User, UserRole
from .security import get_current_user_dependency as get_current_user


def require_roles(allowed_roles: List[UserRole]):
    """
    装饰器：要求用户具有指定角色之一
    
    Args:
        allowed_roles: 允许访问的角色列表
    
    Usage:
        @require_roles([UserRole.ADMIN, UserRole.DEMAND])
        def some_endpoint(current_user: User = Depends(get_current_user)):
            pass
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, current_user: User = Depends(get_current_user), **kwargs):
            if current_user.role not in allowed_roles:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"需要以下角色之一: {[role.value for role in allowed_roles]}"
                )
            return await func(*args, current_user=current_user, **kwargs)
        return wrapper
    return decorator


def require_admin(func):
    """装饰器：要求管理员角色"""
    return require_roles([UserRole.ADMIN])(func)


def require_demand(func):
    """装饰器：要求需求方角色"""
    return require_roles([UserRole.DEMAND])(func)


def require_supply(func):
    """装饰器：要求供应方角色"""
    return require_roles([UserRole.SUPPLY])(func)


class PermissionChecker:
    """权限检查器类"""
    
    def __init__(self, user: User):
        self.user = user
    
    def is_admin(self) -> bool:
        """是否为管理员"""
        return self.user.role == UserRole.ADMIN
    
    def is_demand(self) -> bool:
        """是否为需求方"""
        return self.user.role == UserRole.DEMAND
    
    def is_supply(self) -> bool:
        """是否为供应方"""
        return self.user.role == UserRole.SUPPLY
    
    def can_view_enterprise(self, enterprise_id: int, matched_enterprise_ids: List[int] = None) -> bool:
        """
        检查是否可以查看指定企业信息
        
        Args:
            enterprise_id: 要查看的企业ID
            matched_enterprise_ids: 已匹配的企业ID列表（可选）
        
        Returns:
            bool: 是否有权限查看
        """
        # 管理员可以查看所有企业
        if self.is_admin():
            return True
        
        # 可以查看自己的企业
        if self.user.enterprise_id == enterprise_id:
            return True
        
        # 如果有匹配关系，可以查看对方企业
        if matched_enterprise_ids and enterprise_id in matched_enterprise_ids:
            return True
        
        return False
    
    def can_view_demand(self, demand: 'Demand') -> bool:
        """
        检查是否可以查看指定需求
        
        Args:
            demand: 需求对象
        
        Returns:
            bool: 是否有权限查看
        """
        # 管理员可以查看所有需求
        if self.is_admin():
            return True
        
        # 需求方只能查看自己企业的需求
        if self.is_demand():
            return demand.enterprise_id == self.user.enterprise_id
        
        # 供应方可以查看所有已发布的需求
        if self.is_supply():
            return demand.status == 'published'
        
        return False
    
    def can_modify_demand(self, demand: 'Demand') -> bool:
        """
        检查是否可以修改指定需求
        
        Args:
            demand: 需求对象
        
        Returns:
            bool: 是否有权限修改
        """
        # 管理员可以修改所有需求
        if self.is_admin():
            return True
        
        # 需求方只能修改自己企业的需求
        if self.is_demand():
            return demand.enterprise_id == self.user.enterprise_id
        
        # 供应方不能修改需求
        return False
    
    def can_create_demand(self) -> bool:
        """检查是否可以创建需求"""
        return self.is_admin() or self.is_demand()
    
    def can_view_all_enterprises(self) -> bool:
        """检查是否可以查看所有企业"""
        return self.is_admin()
    
    def can_view_all_demands(self) -> bool:
        """检查是否可以查看所有需求"""
        return self.is_admin()
    
    def can_approve_qualification(self) -> bool:
        """检查是否可以审核资质"""
        return self.is_admin()


def get_permission_checker(current_user: User = Depends(get_current_user)) -> PermissionChecker:
    """获取权限检查器"""
    return PermissionChecker(current_user)


def filter_enterprises_by_permission(
    query,
    user: User,
    matched_enterprise_ids: List[int] = None
):
    """
    根据用户权限过滤企业查询
    
    Args:
        query: SQLAlchemy查询对象
        user: 当前用户
        matched_enterprise_ids: 已匹配的企业ID列表
    
    Returns:
        过滤后的查询对象
    """
    from ..models.enterprise import Enterprise
    from sqlalchemy import or_
    
    # 管理员可以看到所有企业
    if user.role == UserRole.ADMIN:
        return query
    
    # 构建过滤条件
    conditions = []
    
    # 可以看到自己的企业
    if user.enterprise_id:
        conditions.append(Enterprise.id == user.enterprise_id)
    
    # 可以看到匹配的企业
    if matched_enterprise_ids:
        conditions.append(Enterprise.id.in_(matched_enterprise_ids))
    
    if conditions:
        return query.filter(or_(*conditions))
    
    # 如果没有任何条件，返回空结果
    return query.filter(False)


def filter_demands_by_permission(query, user: User):
    """
    根据用户权限过滤需求查询
    
    Args:
        query: SQLAlchemy查询对象
        user: 当前用户
    
    Returns:
        过滤后的查询对象
    """
    from ..models.demand import Demand
    
    # 管理员可以看到所有需求
    if user.role == UserRole.ADMIN:
        return query
    
    # 需求方只能看到自己企业的需求
    if user.role == UserRole.DEMAND:
        if user.enterprise_id:
            return query.filter(Demand.enterprise_id == user.enterprise_id)
        else:
            return query.filter(False)  # 没有企业则看不到任何需求
    
    # 供应方可以看到所有已发布的需求
    if user.role == UserRole.SUPPLY:
        return query.filter(Demand.status == 'published')
    
    return query.filter(False)
