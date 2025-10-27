# GitHub Pages 空白页面修复说明

## 问题诊断

GitHub Pages 显示空白页面的原因有以下几个：

### 1. React Router basename 未配置
在子目录部署（如 `/andy-AI-xiaoyi/`）时，React Router 需要知道应用的基础路径。否则路由将无法正确匹配。

### 2. CORS 配置缺失
后端 API 的 CORS 配置只包含 localhost，GitHub Pages 域名的请求会被阻止。

### 3. Vite base 路径
虽然已经配置了 `base: '/andy-AI-xiaoyi/'`，但 Router 也需要相应配置。

## 已实施的修复

### 1. 添加 Router basename ✅
**文件**: `frontend/src/App.jsx`
```jsx
<Router basename="/andy-AI-xiaoyi">
  {/* routes */}
</Router>
```

### 2. 更新后端 CORS 配置 ✅
**文件**: `backend/app/core/config.py`
```python
ALLOWED_ORIGINS: List[str] = [
    "http://localhost:3000", 
    "http://localhost:5173",
    "https://andyyang0726.github.io"  # 新增
]
```

### 3. 重新构建和部署 ✅
- 执行 `npm run build` 生成新的构建文件
- 提交代码到 main 分支
- 部署到 gh-pages 分支

## 访问地址

🌐 **GitHub Pages**: https://andyyang0726.github.io/andy-AI-xiaoyi/

## 验证步骤

1. **等待 1-2 分钟**：GitHub Pages 需要时间更新部署
2. **清除浏览器缓存**：按 Ctrl+Shift+R (Windows) 或 Cmd+Shift+R (Mac)
3. **访问链接**：https://andyyang0726.github.io/andy-AI-xiaoyi/
4. **打开开发者工具**（F12）检查：
   - Console 标签：查看是否有 JavaScript 错误
   - Network 标签：查看资源加载情况
   - 应该看到 `/andy-AI-xiaoyi/assets/` 路径的资源都正常加载

## 后续注意事项

### 如果页面仍然空白

1. **检查 GitHub Pages 是否启用**
   - 进入仓库 Settings → Pages
   - 确认 Source 设置为 `gh-pages` 分支
   - 确认显示绿色的成功部署提示

2. **查看浏览器控制台**
   - 打开开发者工具 (F12)
   - 查看 Console 中的错误信息
   - 查看 Network 中是否有 404 或 CORS 错误

3. **验证资源路径**
   - 检查 HTML 中的资源路径是否正确：
   ```html
   <script src="/andy-AI-xiaoyi/assets/index-xxx.js"></script>
   ```

### 与后端 API 交互

当前前端配置连接到沙箱环境的后端 API：
```
https://8000-ihia78ehq6oi6tkbljqri-02b9cc79.sandbox.novita.ai/api/v1
```

**注意**：
- 沙箱环境的后端可能会定期重启或变更 URL
- 如需长期使用，建议将后端部署到稳定的服务器
- 测试账号：demo_user / demo123456

## 技术架构

```
┌─────────────────────────────────────┐
│   GitHub Pages (静态托管)           │
│   https://andyyang0726.github.io   │
│   /andy-AI-xiaoyi/                 │
└──────────────┬──────────────────────┘
               │ API 请求
               ↓
┌─────────────────────────────────────┐
│   沙箱后端 API (临时)                │
│   FastAPI + SQLite                  │
│   CORS 已配置                       │
└─────────────────────────────────────┘
```

## 构建和部署命令

如需再次部署，执行以下命令：

```bash
# 1. 构建前端
cd /home/user/webapp/frontend
npm run build

# 2. 提交更改
cd /home/user/webapp
git add -A
git commit -m "update: 更新部署内容"
git push origin main

# 3. 部署到 GitHub Pages
git subtree push --prefix frontend/dist origin gh-pages
```

## 配置文件摘要

### Vite 配置
```javascript
// frontend/vite.config.js
export default defineConfig({
  base: '/andy-AI-xiaoyi/',
  // ...
})
```

### React Router 配置
```jsx
// frontend/src/App.jsx
<Router basename="/andy-AI-xiaoyi">
```

### API 配置
```javascript
// frontend/src/services/api.js
const api = axios.create({
  baseURL: 'https://8000-ihia78ehq6oi6tkbljqri-02b9cc79.sandbox.novita.ai/api/v1'
})
```

### 后端 CORS
```python
# backend/app/core/config.py
ALLOWED_ORIGINS: List[str] = [
    "http://localhost:3000", 
    "http://localhost:5173",
    "https://andyyang0726.github.io"
]
```

## 问题排查清单

- [x] Vite base 路径配置
- [x] React Router basename 配置
- [x] 后端 CORS 配置
- [x] 构建文件生成
- [x] 部署到 gh-pages
- [ ] GitHub Pages 设置验证（需要手动检查）
- [ ] 浏览器缓存清除
- [ ] 实际访问测试

---

**部署时间**: 2025-10-27
**部署版本**: c21866f
**状态**: ✅ 已部署，等待 GitHub Pages 生效
