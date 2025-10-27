# 🚀 如何启用GitHub Pages访问

## ✅ 当前状态

- ✅ 代码已推送到GitHub
- ✅ 前端已构建并部署到 `gh-pages` 分支
- ✅ 资源路径已修复（base: '/andy-AI-xiaoyi/'）

## 📝 启用步骤（必须手动完成）

### 第1步：访问仓库设置

点击链接打开设置页面：
```
https://github.com/andyyang0726/andy-AI-xiaoyi/settings/pages
```

或者：
1. 打开仓库：https://github.com/andyyang0726/andy-AI-xiaoyi
2. 点击顶部的 **Settings** 标签
3. 在左侧菜单找到 **Pages**

### 第2步：配置GitHub Pages

在 **Build and deployment** 部分：

1. **Source（来源）**：
   - 选择 `Deploy from a branch`

2. **Branch（分支）**：
   - 第一个下拉菜单选择：`gh-pages`
   - 第二个下拉菜单选择：`/ (root)`

3. 点击 **Save** 按钮

### 第3步：等待部署

- GitHub会自动开始部署
- 通常需要 **1-3分钟**
- 页面会显示绿色的部署状态

### 第4步：访问你的应用

部署完成后，访问：
```
https://andyyang0726.github.io/andy-AI-xiaoyi/
```

---

## 🔍 如何确认部署成功

### 方法1：查看Settings页面
在 https://github.com/andyyang0726/andy-AI-xiaoyi/settings/pages 会显示：
```
✅ Your site is live at https://andyyang0726.github.io/andy-AI-xiaoyi/
```

### 方法2：查看Deployments
访问：https://github.com/andyyang0726/andy-AI-xiaoyi/deployments

会看到 `github-pages` 的部署记录，状态应该是 **Active**

### 方法3：查看Actions
访问：https://github.com/andyyang0726/andy-AI-xiaoyi/actions

会看到 `pages build and deployment` 工作流，状态应该是 ✅ 成功

---

## 🎯 访问后的使用

### 测试账号

| 角色 | 邮箱 | 密码 |
|-----|------|------|
| 管理员 | admin@platform.com | admin123 |
| 长安汽车 | changan@demo.com | demo123 |
| 小易智联 | xiaoyi@demo.com | demo123 |

### 功能演示流程

1. **登录** - 使用测试账号登录
2. **工作台** - 查看统计数据
3. **企业管理** - 浏览7家企业
4. **需求列表** - 查看3个示例需求
5. **创建需求** - 体验智能表单
6. **智能评估** - 点击"评估"按钮，查看详细报告
7. **智能匹配** - 点击"匹配"按钮，查看推荐供应商

---

## ⚠️ 常见问题

### Q1: 点击Save后没有反应
**A**: 刷新页面，确认配置已保存

### Q2: 显示404错误
**A**: 
- 确认已选择 `gh-pages` 分支
- 等待几分钟，GitHub需要时间部署
- 检查 Actions 页面是否有部署错误

### Q3: 页面空白或样式丢失
**A**: 这个问题已经通过配置 `base: '/andy-AI-xiaoyi/'` 解决了

### Q4: 无法连接后端API
**A**: 
- 检查后端服务是否运行
- 当前后端是临时sandbox环境
- 生产环境需要部署稳定的后端服务器

### Q5: 如何更新部署
**A**: 
```bash
# 修改代码后
cd frontend
npm run build
cd ..
git add frontend/dist
git commit -m "update: 更新前端"
git push origin main
git subtree push --prefix frontend/dist origin gh-pages
```

---

## 📞 技术支持

如果遇到问题：
1. 查看 https://github.com/andyyang0726/andy-AI-xiaoyi/issues
2. 查看 GitHub Pages 文档：https://docs.github.com/en/pages
3. 检查浏览器控制台的错误信息

---

## 📚 相关链接

- 🏠 GitHub仓库：https://github.com/andyyang0726/andy-AI-xiaoyi
- ⚙️ Pages设置：https://github.com/andyyang0726/andy-AI-xiaoyi/settings/pages
- 🚀 部署记录：https://github.com/andyyang0726/andy-AI-xiaoyi/deployments
- 📖 完整文档：查看仓库中的 README.md

---

**预期访问地址**: https://andyyang0726.github.io/andy-AI-xiaoyi/  
**更新时间**: 2024-10-27  
**状态**: 等待启用GitHub Pages设置
