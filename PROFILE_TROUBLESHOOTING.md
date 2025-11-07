# Profile 页面问题排查指南

## 问题描述
用户反馈：在个人信息页面想补充企业信息时，页面显示为空白。

## 已实施的修复

### 1. 增强错误处理和调试日志

在 `frontend/src/pages/Profile.jsx` 中添加了：

```javascript
// 增强的用户数据加载
const fetchUserProfile = async () => {
  try {
    setLoading(true);
    const userDataStr = localStorage.getItem('user');
    console.log('Raw user data from localStorage:', userDataStr);
    
    if (!userDataStr) {
      console.error('No user data in localStorage');
      message.error('未找到用户信息，请重新登录');
      navigate('/login');
      return;
    }
    
    const userData = JSON.parse(userDataStr);
    console.log('Parsed user data:', userData);
    setUser(userData);
    
    // ... 企业信息加载
  } catch (error) {
    console.error('Error fetching profile:', error);
    message.error('获取用户信息失败: ' + (error.message || '未知错误'));
  } finally {
    setLoading(false);
  }
};
```

### 2. 添加空数据保护

```javascript
// 如果没有用户数据，显示提示
if (!user && !loading) {
  return (
    <Card>
      <Alert
        message="无法加载用户信息"
        description="请尝试重新登录"
        type="error"
        showIcon
        action={
          <Button onClick={() => navigate('/login')}>
            前往登录
          </Button>
        }
      />
    </Card>
  );
}
```

### 3. 改进企业信息显示逻辑

根据用户角色显示不同的企业注册入口：

```javascript
// 供应方用户
if (user?.role === 'supply') {
  <Button onClick={() => navigate('/supplier-register')}>
    供应商企业入驻
  </Button>
}

// 需求方用户
if (user?.role === 'demand') {
  <Button onClick={() => navigate('/qualification')}>
    完善企业资质
  </Button>
}
```

## 排查步骤

### 步骤1：检查浏览器控制台

1. 打开浏览器开发者工具（F12）
2. 切换到 Console 标签
3. 刷新个人信息页面
4. 查看以下日志：
   - `Raw user data from localStorage:`
   - `Parsed user data:`
   - `Rendering user info, user:`
   - `Rendering enterprise info, user:`

### 步骤2：检查用户数据

在浏览器控制台执行：
```javascript
// 查看localStorage中的用户数据
console.log('Token:', localStorage.getItem('token'));
console.log('User:', localStorage.getItem('user'));

// 解析用户数据
const user = JSON.parse(localStorage.getItem('user'));
console.log('Parsed user:', user);
console.log('User role:', user?.role);
console.log('Enterprise ID:', user?.enterprise_id);
```

### 步骤3：检查API响应

如果用户有 `enterprise_id`，检查企业数据API：

在浏览器控制台或命令行：
```bash
# 获取token
TOKEN=$(grep token ~/.../localStorage)

# 测试企业API
curl -H "Authorization: Bearer $TOKEN" \
  http://localhost:8000/api/v1/enterprises/1
```

### 步骤4：检查路由配置

确认Profile页面路由正确：
```javascript
// 在 App.jsx 中
<Route path="profile" element={<Profile />} />
```

访问URL应该是：`http://localhost:5173/#/profile`

## 常见问题和解决方案

### 问题1：页面完全空白

**可能原因**：
- localStorage中没有用户数据
- React组件渲染错误
- 路由配置问题

**解决方案**：
1. 检查是否已登录（localStorage中是否有token和user）
2. 尝试重新登录
3. 检查浏览器控制台的错误信息

### 问题2：显示"未关联企业"但看不到按钮

**可能原因**：
- 用户角色未正确设置
- EnterpriseRoleSelection组件加载失败

**解决方案**：
1. 检查用户数据中的 `role` 字段
2. 确认 `role` 是 'supply' 或 'demand'
3. 如果role不正确，需要更新用户数据

### 问题3：点击"选择角色并注册企业"后没有反应

**可能原因**：
- EnterpriseRoleSelection组件未正确导入
- 导航函数失败

**解决方案**：
1. 检查组件路径：`src/components/EnterpriseRoleSelection.jsx`
2. 确认路由配置包含 `/supplier-register` 和 `/qualification`

## 测试用例

### 测试1：有企业的用户

```javascript
// 用户数据
{
  "id": 2,
  "email": "changan@demo.com",
  "role": "demand",
  "enterprise_id": 1,
  "full_name": "张三",
  "phone": "13800138000"
}

// 期望结果
- 个人信息标签页：显示用户基本信息
- 企业信息标签页：显示企业详细信息
- 显示"管理企业"按钮
```

### 测试2：无企业的需求方用户

```javascript
// 用户数据
{
  "id": 5,
  "email": "newuser@test.com",
  "role": "demand",
  "enterprise_id": null
}

// 期望结果
- 个人信息标签页：显示用户基本信息
- 企业信息标签页：显示"未关联企业"提示
- 显示"完善企业资质"按钮（导航到 /qualification）
```

### 测试3：无企业的供应方用户

```javascript
// 用户数据
{
  "id": 6,
  "email": "newsupplier@test.com",
  "role": "supply",
  "enterprise_id": null
}

// 期望结果
- 个人信息标签页：显示用户基本信息
- 企业信息标签页：显示"未关联企业"提示
- 显示"供应商企业入驻"按钮（导航到 /supplier-register）
```

## 快速验证命令

```bash
# 1. 检查前端服务
curl http://localhost:5173/ | grep -o "<title>.*</title>"

# 2. 检查后端服务
curl http://localhost:8000/health

# 3. 测试登录
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "changan@demo.com", "password": "demo123"}'

# 4. 检查Profile页面组件
grep -r "const Profile" frontend/src/pages/
```

## 前端访问地址

- **开发服务器**: http://localhost:5173
- **Profile页面**: http://localhost:5173/#/profile

## 后续建议

1. **如果页面仍然空白**：
   - 清除浏览器缓存
   - 清除localStorage（重新登录）
   - 检查浏览器控制台的React错误

2. **如果显示但功能不正常**：
   - 检查用户的role字段
   - 确认enterprise_id的值
   - 验证API端点是否正常响应

3. **优化建议**：
   - 添加加载骨架屏
   - 添加更友好的错误提示
   - 实现自动重试机制

---

**修改文件**：
- `frontend/src/pages/Profile.jsx`

**测试账号**：
- 需求方：changan@demo.com / demo123
- 供应方：xiaoyi@demo.com / demo123

**前端运行状态**：✅ 运行在 http://localhost:5173
