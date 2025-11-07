/**
 * 权限管理Hook
 * 根据用户角色提供权限检查功能
 */
import { useMemo } from 'react';

export const UserRole = {
  ADMIN: 'admin',
  DEMAND: 'demand',
  SUPPLY: 'supply'
};

export const usePermissions = () => {
  const user = useMemo(() => {
    try {
      return JSON.parse(localStorage.getItem('user') || '{}');
    } catch {
      return {};
    }
  }, []);

  const role = user.role || UserRole.DEMAND;

  return {
    // 角色判断
    isAdmin: role === UserRole.ADMIN,
    isDemand: role === UserRole.DEMAND,
    isSupply: role === UserRole.SUPPLY,
    role,
    user,

    // 企业管理权限
    canViewAllEnterprises: role === UserRole.ADMIN,
    canViewOwnEnterprise: true,
    canModifyEnterprise: (enterpriseId) => {
      if (role === UserRole.ADMIN) return true;
      return user.enterprise_id === enterpriseId;
    },

    // 需求管理权限
    canViewAllDemands: role === UserRole.ADMIN,
    canViewPublishedDemands: role === UserRole.SUPPLY || role === UserRole.ADMIN,
    canViewOwnDemands: role === UserRole.DEMAND || role === UserRole.ADMIN,
    canCreateDemand: role === UserRole.ADMIN || role === UserRole.DEMAND,
    canModifyDemand: (demandEnterpriseId) => {
      if (role === UserRole.ADMIN) return true;
      if (role === UserRole.DEMAND) {
        return user.enterprise_id === demandEnterpriseId;
      }
      return false;
    },

    // 匹配推荐权限
    canViewAllRecommendations: role === UserRole.ADMIN,
    canViewOwnRecommendations: role === UserRole.DEMAND || role === UserRole.SUPPLY,
    canViewMatchedEnterprises: true,

    // 审核权限
    canApproveQualification: role === UserRole.ADMIN,
    canApproveDemand: role === UserRole.ADMIN,

    // 统计权限
    canViewPlatformStats: role === UserRole.ADMIN,
    canViewOwnStats: true,

    // 菜单权限
    getMenuItems: () => {
      const baseItems = [
        { key: '/profile', label: '个人信息', visible: true }
      ];

      if (role === UserRole.ADMIN) {
        return [
          { key: '/', label: '工作台', visible: true },
          { key: '/enterprises', label: '企业管理', visible: true },
          { key: '/demands', label: '需求管理', visible: true },
          { key: '/recommended', label: '匹配管理', visible: true },
          ...baseItems
        ];
      }

      if (role === UserRole.DEMAND) {
        return [
          { key: '/', label: '我的工作台', visible: true },
          { key: '/demands', label: '我的需求', visible: true },
          { key: '/matched-suppliers', label: '推荐供应商', visible: true },
          ...baseItems
        ];
      }

      if (role === UserRole.SUPPLY) {
        return [
          { key: '/', label: '我的工作台', visible: true },
          { key: '/supplier-home', label: '企业主页', visible: true },
          { key: '/matched-clients', label: '匹配客户', visible: true },
          ...baseItems
        ];
      }

      return baseItems;
    }
  };
};

export default usePermissions;
