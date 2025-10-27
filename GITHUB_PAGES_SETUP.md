# 🌐 GitHub Pages 部署指南

## ✅ 部署状态

代码已成功推送到GitHub，前端构建文件已部署到 `gh-pages` 分支。

## 📍 GitHub仓库地址

```
https://github.com/andyyang0726/andy-AI-xiaoyi
```

## 🔧 启用GitHub Pages的步骤

### 1. 进入仓库设置

访问：https://github.com/andyyang0726/andy-AI-xiaoyi/settings/pages

### 2. 配置GitHub Pages

在 **Settings** → **Pages** 页面：

1. **Source（来源）**：
   - 选择 `Deploy from a branch`

2. **Branch（分支）**：
   - 选择 `gh-pages`
   - 目录选择 `/ (root)`

3. 点击 **Save（保存）**

### 3. 等待部署完成

- GitHub会自动部署，通常需要1-2分钟
- 部署完成后会显示访问链接

### 4. 访问地址

部署成功后，你的前端应用将可以通过以下地址访问：

```
https://andyyang0726.github.io/andy-AI-xiaoyi/
```

---

## 🎯 完整访问地址

部署完成后：

### 前端界面（GitHub Pages）
```
https://andyyang0726.github.io/andy-AI-xiaoyi/
```

### 后端API服务（Sandbox - 临时）
```
https://8000-ihia78ehq6oi6tkbljqri-02b9cc79.sandbox.novita.ai
```

### API文档（Swagger）
```
https://8000-ihia78ehq6oi6tkbljqri-02b9cc79.sandbox.novita.ai/api/docs
```

---

## ⚙️ 前端配置说明

前端已配置为直接连接到在线后端API：

**文件**：`frontend/src/services/api.js`

```javascript
const api = axios.create({
  baseURL: 'https://8000-ihia78ehq6oi6tkbljqri-02b9cc79.sandbox.novita.ai/api/v1',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
});
```

### ⚠️ 注意事项

1. **后端服务是临时的**
   - Sandbox环境的后端服务可能会在一段时间后停止
   - 生产环境需要部署到稳定的服务器

2. **CORS配置**
   - 如果前端访问后端时出现CORS错误
   - 需要在后端的 `ALLOWED_ORIGINS` 中添加 GitHub Pages 域名
   - 修改文件：`backend/app/core/config.py`

3. **生产环境部署建议**
   - 后端：部署到云服务器（阿里云、腾讯云、AWS等）
   - 前端：可继续使用GitHub Pages或部署到CDN
   - 数据库：迁移到PostgreSQL
   - 域名：配置自定义域名

---

## 🔄 更新部署

当你修改了前端代码后，重新部署：

```bash
# 1. 构建前端
cd frontend
npm run build

# 2. 提交更改
cd ..
git add frontend/dist
git commit -m "build: 更新前端构建"

# 3. 推送到gh-pages分支
git subtree push --prefix frontend/dist origin gh-pages
```

GitHub Pages会自动更新（可能需要几分钟）。

---

## 🎨 自定义域名（可选）

如果你有自己的域名：

1. 在域名DNS设置中添加CNAME记录：
   ```
   CNAME  www  andyyang0726.github.io
   ```

2. 在GitHub仓库设置中：
   - **Settings** → **Pages**
   - **Custom domain** 输入你的域名
   - 保存

3. 创建 `frontend/dist/CNAME` 文件：
   ```
   your-domain.com
   ```

---

## 📱 测试账号

部署完成后，使用以下账号登录：

| 角色 | 邮箱 | 密码 |
|-----|------|------|
| 管理员 | admin@platform.com | admin123 |
| 长安汽车 | changan@demo.com | demo123 |
| 小易智联 | xiaoyi@demo.com | demo123 |

---

## 🐛 常见问题

### Q1: GitHub Pages显示404
**A**: 确保已正确配置Pages设置，选择了gh-pages分支

### Q2: 页面显示但无法登录
**A**: 检查浏览器控制台，可能是CORS问题或后端服务已停止

### Q3: 如何查看部署状态
**A**: 
- 访问：https://github.com/andyyang0726/andy-AI-xiaoyi/deployments
- 查看最新的部署状态

### Q4: 需要更新后端地址
**A**: 修改 `frontend/src/services/api.js` 中的 `baseURL`，重新构建并部署

---

## 📚 相关文档

- [GitHub Pages 文档](https://docs.github.com/en/pages)
- [项目 README](README.md)
- [快速启动指南](QUICK_START.md)
- [技术设计文档](docs/TECHNICAL_DESIGN.md)

---

**仓库地址**: https://github.com/andyyang0726/andy-AI-xiaoyi  
**预计访问地址**: https://andyyang0726.github.io/andy-AI-xiaoyi/  
**更新时间**: 2024-10-27
