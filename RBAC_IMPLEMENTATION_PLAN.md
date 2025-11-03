# RBAC权限系统实施计划

## ✅ 第一阶段：后端基础（已完成）

### 完成内容
1. ✅ 更新User模型角色枚举
2. ✅ 创建权限控制模块
3. ✅ 实现权限装饰器
4. ✅ 创建角色迁移脚本
5. ✅ 编写RBAC设计文档

### 文件变更
- `backend/app/models/user.py` - 更新角色枚举
- `backend/app/core/permissions.py` - 新建权限模块
- `backend/migrate_user_roles.py` - 新建迁移脚本
- `RBAC_DESIGN.md` - 新建设计文档

---

## 🔄 第二阶段：后端API更新（进行中）

### 需要完成的内容

#### 1. 更新企业API (`backend/app/api/enterprises.py`)
```python
# 需要添加权限控制的端点：
- GET /enterprises - 根据角色过滤可见企业
- GET /enterprises/{id} - 检查是否有权查看该企业
- POST /enterprises - 允许需求方和供应方创建
- PUT /enterprises/{id} - 只能修改自己的企业
```

#### 2. 更新需求API (`backend/app/api/demands.py`)
```python
# 需要添加权限控制的端点：
- GET /demands - 根据角色过滤可见需求
- GET /demands/{id} - 检查是否有权查看该需求
- POST /demands - 只有需求方可以创建
- PUT /demands/{id} - 只能修改自己的需求
- DELETE /demands/{id} - 只能删除自己的需求
```

#### 3. 更新推荐API (`backend/app/api/recommendations.py`)
```python
# 需要添加权限控制的端点：
- GET /recommendations - 根据角色返回不同数据
- GET /demands/{demand_id}/recommendations - 需求方查看匹配供应商
- GET /enterprises/{enterprise_id}/recommendations - 供应方查看推荐需求
```

#### 4. 更新认证API (`backend/app/api/auth.py`)
```python
# 需要更新的内容：
- 注册时根据企业类型设置用户角色
- 登录响应中包含用户角色信息
- /me端点返回完整的角色信息
```

---

## 🎨 第三阶段：前端权限控制

### 1. 创建权限管理Hook
**文件**: `frontend/src/hooks/usePermissions.js`
```javascript
export const usePermissions = () => {
  const user = JSON.parse(localStorage.getItem('user') || '{}');
  
  return {
    isAdmin: user.role === 'admin',
    isDemand: user.role === 'demand',
    isSupply: user.role === 'supply',
    canViewAllEnterprises: user.role === 'admin',
    canViewAllDemands: user.role === 'admin',
    canCreateDemand: ['admin', 'demand'].includes(user.role),
    // ... 更多权限检查
  };
};
```

### 2. 更新Layout组件
**文件**: `frontend/src/components/Layout.jsx`
- 根据角色动态渲染菜单
- 管理员：显示所有菜单
- 需求方：显示需求相关菜单
- 供应方：显示供应相关菜单

### 3. 更新各页面组件
- **企业管理页**: 根据角色过滤显示的企业
- **需求管理页**: 根据角色过滤显示的需求
- **推荐页面**: 分离为两个不同的页面
  - 需求方：查看匹配的供应商
  - 供应方：查看推荐的需求

### 4. 创建新页面
- `frontend/src/pages/MatchedSuppliers.jsx` - 需求方查看匹配供应商
- `frontend/src/pages/RecommendedDemands.jsx` - 供应方查看推荐需求
- `frontend/src/pages/MatchedClients.jsx` - 供应方查看匹配客户

---

## 🧪 第四阶段：测试与验证

### 测试场景

#### 1. 管理员测试
- [ ] 可以查看所有企业
- [ ] 可以查看所有需求
- [ ] 可以查看所有匹配记录
- [ ] 可以审核企业资质
- [ ] 可以审核需求

#### 2. 需求方测试
- [ ] 只能看到自己企业的需求
- [ ] 可以创建新需求
- [ ] 可以修改自己的需求
- [ ] 可以查看匹配的供应商
- [ ] 看不到其他需求方信息
- [ ] 看不到未匹配的供应商

#### 3. 供应方测试
- [ ] 可以看到所有已发布的需求
- [ ] 看不到需求方企业详细信息（未匹配前）
- [ ] 可以查看推荐给自己的需求
- [ ] 匹配后可以看到需求方企业信息
- [ ] 看不到其他供应方信息
- [ ] 不能创建需求

#### 4. 权限隔离测试
- [ ] 尝试访问无权限的API（应返回403）
- [ ] 尝试修改其他人的数据（应被拒绝）
- [ ] 尝试查看无权查看的数据（应被过滤）

---

## 📝 第五阶段：文档更新

### 需要更新的文档
1. `USER_GUIDE.md` - 更新使用指南，说明不同角色的功能
2. `README.md` - 添加权限系统说明
3. `API文档` - 标注每个端点的权限要求
4. `RBAC_DESIGN.md` - 完善设计文档

---

## 🚀 实施步骤建议

### 立即执行（必需）
1. **运行角色迁移脚本**
   ```bash
   cd backend
   python migrate_user_roles.py
   ```

2. **更新企业API** - 添加权限过滤

3. **更新需求API** - 添加权限控制

4. **更新前端Layout** - 动态菜单

### 后续执行（推荐）
5. **创建新的推荐页面** - 分离需求方和供应方视图

6. **更新Dashboard** - 根据角色显示不同数据

7. **完整测试** - 验证所有权限场景

8. **更新文档** - 确保文档准确

---

## ⚠️ 注意事项

### 数据兼容性
- 现有数据库的用户需要运行迁移脚本
- 确保所有用户都有有效的role值
- 测试数据需要更新角色

### API兼容性
- 前端请求需要处理403权限错误
- 需要优雅降级，显示友好的错误信息
- 考虑添加权限相关的错误提示

### 性能考虑
- 权限检查应该高效
- 考虑缓存常用的权限判断
- 避免在循环中进行复杂的权限检查

---

## 📊 进度追踪

- [x] 第一阶段：后端基础
- [ ] 第二阶段：后端API更新
- [ ] 第三阶段：前端权限控制
- [ ] 第四阶段：测试与验证
- [ ] 第五阶段：文档更新

**当前进度**: 20% 完成

---

**文档版本**: v1.0  
**最后更新**: 2025-11-03  
**负责人**: AI Assistant
