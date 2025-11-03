# GitHub仓库重命名指南

## 📝 当前状态

✅ **已完成**：项目名称和品牌已更新为"企业AI需求对接平台"

### 已更新的内容
- ✅ README.md 主标题
- ✅ 前端页面标题（index.html）
- ✅ package.json 项目名称
- ✅ 应用内所有显示名称（Layout、Login等）
- ✅ SEO meta信息

---

## 🔄 GitHub仓库URL重命名（可选）

如果您希望将GitHub仓库的URL也改为新名称，请按以下步骤操作：

### 方式1：通过GitHub网页端（推荐）

1. **访问仓库设置**
   - 打开 https://github.com/andyyang0726/andy-AI-xiaoyi
   - 点击 `Settings` 标签

2. **重命名仓库**
   - 在 "Repository name" 输入框中输入新名称
   - 建议使用：`enterprise-ai-demand-platform` 或 `ai-demand-matching-platform`
   - 点击 `Rename` 按钮

3. **GitHub自动处理**
   - GitHub会自动设置重定向（从旧URL到新URL）
   - 旧链接在短期内仍然可用

### 方式2：通过GitHub API

```bash
# 需要GitHub Personal Access Token
curl -X PATCH \
  -H "Authorization: token YOUR_GITHUB_TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  https://api.github.com/repos/andyyang0726/andy-AI-xiaoyi \
  -d '{"name":"enterprise-ai-demand-platform"}'
```

---

## ⚠️ 重命名后需要做的事

### 1. 更新本地仓库的远程URL

```bash
# 在本地仓库目录执行
cd /home/user/webapp

# 查看当前远程URL
git remote -v

# 更新远程URL（将new-repo-name替换为实际名称）
git remote set-url origin https://github.com/andyyang0726/new-repo-name.git

# 验证更改
git remote -v
```

### 2. 更新GitHub Pages配置

如果仓库名改变，GitHub Pages的URL也会改变：

**旧URL**: `https://andyyang0726.github.io/andy-AI-xiaoyi/`  
**新URL**: `https://andyyang0726.github.io/new-repo-name/`

需要更新以下文件：

#### vite.config.js
```javascript
export default defineConfig(({ mode }) => ({
  base: mode === 'production' ? '/new-repo-name/' : '/',
  // ...
}))
```

#### frontend/package.json
```json
{
  "scripts": {
    "deploy": "gh-pages -d dist -r https://github.com/andyyang0726/new-repo-name.git"
  }
}
```

#### App.jsx（如果使用basename）
```javascript
const basename = import.meta.env.MODE === 'production' ? '/new-repo-name' : '';
```

### 3. 重新部署到GitHub Pages

```bash
cd /home/user/webapp/frontend
npm run build
npm run deploy
```

### 4. 更新README.md中的链接

```markdown
[![部署状态](https://img.shields.io/badge/部署-成功-brightgreen)](https://andyyang0726.github.io/new-repo-name/)
```

---

## 🎯 推荐的仓库名称

基于"企业AI需求对接平台"，推荐以下英文名称：

1. **enterprise-ai-demand-platform** ⭐ 推荐
   - 直译，清晰易懂
   - URL: `andyyang0726.github.io/enterprise-ai-demand-platform/`

2. **ai-demand-matching-platform**
   - 强调匹配功能
   - URL: `andyyang0726.github.io/ai-demand-matching-platform/`

3. **enterprise-ai-connect**
   - 简洁，强调连接
   - URL: `andyyang0726.github.io/enterprise-ai-connect/`

4. **ai-supply-demand-hub**
   - 强调供需中心
   - URL: `andyyang0726.github.io/ai-supply-demand-hub/`

---

## 📊 影响评估

### 保持当前URL的优点
- ✅ 无需更新任何配置
- ✅ 所有现有链接继续有效
- ✅ GitHub Pages无需重新配置
- ✅ 项目显示名称已全部更新

### 更改URL的缺点
- ⚠️ 需要更新多处配置
- ⚠️ 需要重新部署
- ⚠️ 外部分享的链接可能失效
- ⚠️ 可能影响搜索引擎索引

---

## 🤔 我的建议

**建议方案**：保持当前GitHub仓库URL不变

**理由**：
1. 项目的对外显示名称已全部更新为"企业AI需求对接平台"
2. 仓库URL只是技术层面的标识，用户通常不会直接看到
3. 避免了重新配置和部署的复杂性
4. GitHub会提供重定向，但不如保持稳定

**如果确实需要更改URL**：
- 建议在项目发布前进行
- 一次性完成所有相关配置的更新
- 做好充分的测试

---

## ✅ 当前已完成的工作

所有面向用户的显示名称已经更新：
- 浏览器标签页标题：企业AI需求对接平台
- 登录页面标题：企业AI需求对接平台
- 侧边栏标题：企业AI需求平台
- 顶部导航标题：企业AI需求对接平台
- README主标题：企业AI需求对接平台

**结论**：从用户体验角度，项目重命名已经完成！✨
