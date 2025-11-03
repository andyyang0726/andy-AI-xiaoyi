# GitHub Pages SPA 路由修复说明

## 🐛 问题描述

当直接访问 React Router 的子路由（如 `/supplier-register`、`/login` 等）时，GitHub Pages 会返回 404 错误。

**原因**：
- GitHub Pages 是静态文件托管服务
- 只有一个 `index.html` 文件
- 访问 `/supplier-register` 时，服务器查找 `supplier-register.html` 文件
- 文件不存在，返回 404

## ✅ 解决方案

使用 **spa-github-pages** 方案，通过 `404.html` 和客户端脚本实现 SPA 路由支持。

### 工作原理

```
用户访问 /supplier-register
    ↓
GitHub Pages 返回 404.html
    ↓
404.html 中的脚本将路径转换为查询参数
    ↓
重定向到 /andy-AI-xiaoyi/?/supplier-register
    ↓
index.html 中的脚本解析查询参数
    ↓
恢复为 /andy-AI-xiaoyi/supplier-register
    ↓
React Router 正常处理路由
```

## 📁 实现文件

### 1. frontend/public/404.html

```html
<!DOCTYPE html>
<html lang="zh-CN">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>企业AI需求对接平台</title>
    <script>
      // GitHub Pages SPA redirect hack
      (function() {
        var pathSegmentsToKeep = 1; // For /andy-AI-xiaoyi/
        
        var l = window.location;
        var redirect = l.protocol + '//' + l.hostname + (l.port ? ':' + l.port : '') +
          l.pathname.split('/').slice(0, 1 + pathSegmentsToKeep).join('/') + '/?/' +
          l.pathname.slice(1).split('/').slice(pathSegmentsToKeep).join('/').replace(/&/g, '~and~') +
          (l.search ? '&' + l.search.slice(1).replace(/&/g, '~and~') : '') +
          l.hash;
        
        l.replace(redirect);
      })();
    </script>
  </head>
  <body>
  </body>
</html>
```

**作用**：
- 当访问不存在的路径时，GitHub Pages 自动返回此文件
- 脚本将路径转换为查询参数并重定向

**关键参数**：
- `pathSegmentsToKeep = 1`：保留 `/andy-AI-xiaoyi/` 这一级路径
- `/&/g, '~and~'`：转义 `&` 字符，避免与查询参数冲突

### 2. frontend/index.html

在 `<head>` 中添加：

```html
<!-- GitHub Pages SPA redirect handler -->
<script>
  // Single Page Apps for GitHub Pages
  (function(l) {
    if (l.search[1] === '/' ) {
      var decoded = l.search.slice(1).split('&').map(function(s) { 
        return s.replace(/~and~/g, '&')
      }).join('?');
      window.history.replaceState(null, null,
          l.pathname.slice(0, -1) + decoded + l.hash
      );
    }
  }(window.location))
</script>
```

**作用**：
- 检查URL是否包含特殊的查询参数格式（`?/path`）
- 解析查询参数，恢复原始路径
- 使用 `history.replaceState` 更新浏览器地址栏
- React Router 接管后续路由

## 🚀 部署流程

### 1. 构建前端

```bash
cd frontend
npm run build
```

### 2. 部署到 GitHub Pages

**方法一：使用 git subtree（推荐）**

```bash
cd /home/user/webapp
git subtree push --prefix frontend/dist origin gh-pages
```

**方法二：强制部署（当需要覆盖时）**

```bash
cd /home/user/webapp
git push origin `git subtree split --prefix frontend/dist main`:gh-pages --force
```

### 3. 等待部署完成

GitHub Pages 通常需要 1-3 分钟更新。

## 🧪 测试

部署完成后，测试以下URL是否正常访问：

### 基础路由
✅ https://andyyang0726.github.io/andy-AI-xiaoyi/
✅ https://andyyang0726.github.io/andy-AI-xiaoyi/login

### 供应商注册路由
✅ https://andyyang0726.github.io/andy-AI-xiaoyi/supplier-register

### 其他路由
✅ https://andyyang0726.github.io/andy-AI-xiaoyi/enterprises
✅ https://andyyang0726.github.io/andy-AI-xiaoyi/demands
✅ https://andyyang0726.github.io/andy-AI-xiaoyi/demands/create
✅ https://andyyang0726.github.io/andy-AI-xiaoyi/recommended
✅ https://andyyang0726.github.io/andy-AI-xiaoyi/supplier-home

## 🔍 调试

### 1. 检查 404.html 是否存在

访问：https://andyyang0726.github.io/andy-AI-xiaoyi/404.html

应该能看到空白页面（因为立即重定向）。

### 2. 检查重定向过程

1. 打开浏览器开发者工具（F12）
2. 切换到 Network 标签
3. 访问 `/supplier-register`
4. 观察请求流程：
   - 第一次请求：返回 404.html
   - 立即重定向到：`/?/supplier-register`
   - index.html 加载
   - React Router 接管

### 3. 查看控制台

如果有错误，检查浏览器控制台的错误信息。

## ⚠️ 注意事项

### 1. pathSegmentsToKeep 参数

此参数必须根据 GitHub Pages 的部署路径设置：

- 部署到 `username.github.io`：`pathSegmentsToKeep = 0`
- 部署到 `username.github.io/repo-name/`：`pathSegmentsToKeep = 1`

本项目使用 `/andy-AI-xiaoyi/`，所以设置为 `1`。

### 2. React Router basename

确保 `App.jsx` 中的 basename 与部署路径一致：

```jsx
<Router basename="/andy-AI-xiaoyi">
  ...
</Router>
```

### 3. Vite base 配置

确保 `vite.config.js` 中的 base 正确：

```javascript
export default defineConfig({
  base: '/andy-AI-xiaoyi/',
  ...
})
```

### 4. 部署前必须构建

每次修改代码后，必须重新构建才能部署：

```bash
npm run build
```

### 5. 缓存问题

如果更新后看不到变化：
- 清除浏览器缓存
- 使用无痕模式测试
- 等待几分钟（GitHub Pages 可能有延迟）

## 📚 参考资料

- [spa-github-pages](https://github.com/rafgraph/spa-github-pages)
- [GitHub Pages 文档](https://docs.github.com/en/pages)
- [React Router 部署指南](https://reactrouter.com/en/main/start/concepts#client-side-routing)

## 🎯 总结

使用此方案后，GitHub Pages 上的 React SPA 应用支持：

✅ 直接访问任意路由
✅ 刷新页面保持路由
✅ 浏览器前进/后退正常工作
✅ 分享链接可直接访问
✅ SEO 友好（虽然有轻微影响）

**优点**：
- 简单易用，无需服务器配置
- 纯客户端解决方案
- 兼容所有 React Router 功能

**缺点**：
- 首次加载有轻微重定向
- SEO 不如服务器端渲染
- 依赖客户端 JavaScript

---

**最后更新**：2025-10-28
**状态**：✅ 已部署并测试通过
