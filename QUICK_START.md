# 🚀 快速启动指南

## 项目概览

**企业AI需求对接平台**

这是一个完整的企业级AI供需对接平台，包含智能评估和匹配推荐功能。

### 📊 项目统计
- **代码文件**: 33个
- **总文件**: 64个
- **代码行数**: 约3200行
- **开发时间**: MVP阶段
- **技术栈**: FastAPI + React + SQLite

## 🎯 核心功能

1. ✅ **企业管理** - 注册、认证、信用评分
2. ✅ **需求采集** - 结构化表单、标签分类
3. ✅ **智能评估** - 多维度自动评估
4. ✅ **智能匹配** - 6维度加权推荐算法

## ⚡ 一键启动（推荐）

```bash
# 使用启动脚本（自动处理所有步骤）
./start.sh
```

启动后访问：
- 🌐 **前端界面**: http://localhost:3000
- 📡 **API文档**: http://localhost:8000/api/docs
- ❤️ **健康检查**: http://localhost:8000/health

## 📝 手动启动步骤

### 步骤 1: 启动后端

```bash
cd backend

# 创建虚拟环境（首次运行）
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt

# 初始化数据库（首次运行）
python init_db.py

# 启动后端服务
python -m app.main
```

后端服务: http://localhost:8000

### 步骤 2: 启动前端（新终端）

```bash
cd frontend

# 安装依赖（首次运行）
npm install

# 启动前端开发服务器
npm run dev
```

前端服务: http://localhost:3000

## 🔑 测试账号

| 角色 | 邮箱 | 密码 | 说明 |
|-----|------|------|------|
| 管理员 | admin@platform.com | admin123 | 平台管理员 |
| 长安汽车 | changan@demo.com | demo123 | 需求方企业 |
| 小易智联 | xiaoyi@demo.com | demo123 | 供应方企业 |

## 📖 演示流程

### 1. 登录系统
使用管理员账号登录，查看工作台统计数据。

### 2. 浏览企业
进入"企业管理"，查看预置的7家企业（3家需求方 + 4家供应方）。

### 3. 创建需求
1. 点击"创建需求"
2. 填写需求信息
3. 选择行业和场景标签
4. 设置预算和时间
5. 提交需求

### 4. 智能评估 ⭐
1. 进入需求详情
2. 点击"评估需求"
3. 查看评估报告：
   - 技术可行性评分
   - 项目就绪度评分
   - 数据健康度评分
   - 风险等级
   - 推荐路径
   - 改进建议

### 5. 智能匹配 ⭐⭐
1. 对已评估的需求点击"匹配供应商"
2. 查看匹配结果：
   - Top-5 供应商
   - 匹配度评分
   - 6个维度的详细得分
   - 匹配理由
   - 供应商联系方式

## 🔧 API测试

### 健康检查
```bash
curl http://localhost:8000/health
```

### 登录获取Token
```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@platform.com","password":"admin123"}'
```

### 获取企业列表
```bash
TOKEN="your-token-here"
curl -H "Authorization: Bearer $TOKEN" \
  "http://localhost:8000/api/v1/enterprises"
```

### 获取需求列表
```bash
TOKEN="your-token-here"
curl -H "Authorization: Bearer $TOKEN" \
  "http://localhost:8000/api/v1/demands"
```

### 评估需求
```bash
TOKEN="your-token-here"
curl -X POST -H "Authorization: Bearer $TOKEN" \
  "http://localhost:8000/api/v1/demands/1/evaluate"
```

### 匹配供应商
```bash
TOKEN="your-token-here"
curl -X POST -H "Authorization: Bearer $TOKEN" \
  "http://localhost:8000/api/v1/demands/1/match"
```

## 📁 项目结构

```
webapp/
├── backend/              # 后端服务
│   ├── app/
│   │   ├── api/         # API路由
│   │   ├── core/        # 核心配置
│   │   ├── models/      # 数据模型
│   │   ├── schemas/     # 数据模式
│   │   ├── services/    # 业务逻辑
│   │   └── main.py      # 应用入口
│   ├── init_db.py       # 数据库初始化
│   └── requirements.txt # Python依赖
├── frontend/            # 前端应用
│   ├── src/
│   │   ├── components/  # 公共组件
│   │   ├── pages/       # 页面组件
│   │   ├── services/    # API服务
│   │   └── App.jsx      # 应用入口
│   └── package.json     # Node依赖
├── docs/                # 文档目录
│   ├── TECHNICAL_DESIGN.md  # 技术设计
│   └── DEMO_GUIDE.md        # 演示指南
└── README.md            # 项目说明
```

## 🎨 核心特性展示

### 智能评估引擎

**评分维度：**
- 📊 数据健康度 (0-100)
- 🔬 技术可行性 (0-100)
- ✅ 项目就绪度 (0-100)
- ⚠️ 风险评估 (低/中/高)
- 🛤️ 推荐路径 (直接交付/试点/PoC)

**算法公式：**
```
综合评分 = 技术可行性 × 0.4 + 项目就绪度 × 0.35 + 数据健康度 × 0.25
```

### 智能匹配引擎

**匹配维度：**
- 🏭 行业匹配度 (25%)
- 🧠 语义相似度 (30%)
- ⭐ 历史成功率 (20%)
- 💰 预算匹配度 (10%)
- 📍 地理位置 (5%)
- 🏆 信用评分 (10%)

**匹配公式：**
```
MatchScore = Σ(维度得分 × 权重)
```

## 🐛 常见问题

### Q1: 后端启动失败？
**A**: 检查Python版本 >= 3.9，确保依赖安装完整
```bash
python --version
pip list
```

### Q2: 前端启动失败？
**A**: 检查Node.js版本 >= 18，删除node_modules重新安装
```bash
node --version
rm -rf node_modules
npm install
```

### Q3: 数据库初始化失败？
**A**: 删除旧数据库文件重新初始化
```bash
cd backend
rm -f ai_platform.db
python init_db.py
```

### Q4: API请求401错误？
**A**: Token过期，重新登录获取新Token

### Q5: CORS错误？
**A**: 检查前端和后端是否在正确的端口运行

## 📚 相关文档

- 📖 [README.md](README.md) - 完整项目说明
- 🏗️ [技术设计文档](docs/TECHNICAL_DESIGN.md)
- 🎬 [演示指南](docs/DEMO_GUIDE.md)

## 🔄 更新日志

### v1.0.0-MVP (2024-10)
- ✅ 完成核心功能开发
- ✅ 实现智能评估引擎
- ✅ 实现智能匹配推荐
- ✅ 预置测试数据
- ✅ 完善文档

## 🤝 技术支持

- 💬 遇到问题？查看文档或联系技术团队
- 📧 Email: tech@xiaoyi.ai
- 🌐 官网: https://xiaoyi.ai

## 📜 许可证

Copyright © 2024 企业AI需求对接平台开发团队

---

**开发团队**: 小易智联  
**版本**: v1.0.0-MVP  
**最后更新**: 2024-10-27
