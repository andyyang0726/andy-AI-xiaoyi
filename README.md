# 重庆人工智能供需对接平台 - MVP版本

## 📋 项目简介

重庆人工智能供需对接平台是一个企业AI需求收集、智能评估、算法撮合、项目孵化的闭环系统。本MVP版本实现了核心功能模块，用于客户展示和开发预研。

### 核心功能

- ✅ **企业注册与认证** - 企业信息管理、资质审核
- ✅ **AI需求采集** - 智能表单、结构化需求收集
- ✅ **智能评估引擎** - 基于规则的AI项目可行性评估
- ✅ **匹配推荐系统** - 多维度供应商智能匹配
- ✅ **用户认证系统** - JWT令牌认证、角色权限管理

### 技术栈

**后端：**
- FastAPI - 高性能Python Web框架
- SQLAlchemy - ORM数据库操作
- SQLite - 轻量级数据库（MVP阶段）
- Pydantic - 数据验证和序列化

**前端：**
- React 18 - UI框架
- Ant Design 5 - 企业级UI组件库
- Vite - 快速构建工具
- React Router - 路由管理
- Axios - HTTP客户端

## 🚀 快速开始

### 环境要求

- Python 3.9+
- Node.js 18+
- npm 或 yarn

### 1. 后端设置

```bash
# 进入后端目录
cd backend

# 创建虚拟环境（推荐）
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt

# 初始化数据库（创建示例数据）
python init_db.py

# 启动后端服务
python -m app.main
```

后端服务将在 http://localhost:8000 启动

API文档：http://localhost:8000/api/docs

### 2. 前端设置

```bash
# 进入前端目录
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

前端服务将在 http://localhost:3000 启动

### 3. 测试账号

初始化数据库后，可使用以下测试账号登录：

- **系统管理员**: `admin@platform.com` / `admin123`
- **长安汽车**: `changan@demo.com` / `demo123`
- **小易智联**: `xiaoyi@demo.com` / `demo123`

## 📁 项目结构

```
webapp/
├── backend/                 # 后端服务
│   ├── app/
│   │   ├── api/            # API路由
│   │   │   ├── auth.py     # 认证接口
│   │   │   ├── enterprises.py  # 企业管理
│   │   │   └── demands.py  # 需求管理
│   │   ├── core/           # 核心配置
│   │   │   ├── config.py   # 应用配置
│   │   │   ├── database.py # 数据库配置
│   │   │   └── security.py # 安全工具
│   │   ├── models/         # 数据模型
│   │   │   ├── enterprise.py  # 企业模型
│   │   │   ├── user.py     # 用户模型
│   │   │   └── demand.py   # 需求模型
│   │   ├── schemas/        # Pydantic模式
│   │   ├── services/       # 业务逻辑
│   │   │   ├── evaluation_service.py  # 评估服务
│   │   │   └── matching_service.py    # 匹配服务
│   │   └── main.py         # 应用入口
│   ├── init_db.py          # 数据库初始化
│   └── requirements.txt    # Python依赖
├── frontend/               # 前端应用
│   ├── src/
│   │   ├── components/     # 公共组件
│   │   │   └── Layout.jsx  # 布局组件
│   │   ├── pages/          # 页面组件
│   │   │   ├── Login.jsx   # 登录页
│   │   │   ├── Dashboard.jsx  # 工作台
│   │   │   ├── EnterpriseList.jsx  # 企业列表
│   │   │   ├── DemandList.jsx      # 需求列表
│   │   │   ├── DemandCreate.jsx    # 创建需求
│   │   │   └── DemandDetail.jsx    # 需求详情
│   │   ├── services/       # API服务
│   │   │   └── api.js      # API封装
│   │   ├── App.jsx         # 应用根组件
│   │   └── main.jsx        # 入口文件
│   ├── package.json
│   └── vite.config.js
└── docs/                   # 文档目录
```

## 🔑 核心功能说明

### 1. 企业注册与管理

- 企业基本信息录入
- 统一社会信用代码验证
- 企业类型：需求方/供应方/双重角色
- 行业标签和AI能力标签
- 认证等级：普通会员/认证企业/优选企业
- 信用评分系统

### 2. 需求采集模块

- 结构化需求表单
- 行业和场景标签分类
- KPI目标设定
- 预算和时间计划
- 保密等级设置
- 优先级标记

### 3. 智能评估引擎

**评估维度：**
- **数据健康度** (0-100分)
  - 数据量评分
  - 标注率评分
  - 数据类型多样性

- **技术可行性** (0-100分)
  - 行业成熟度加权
  - 场景难度评估

- **项目就绪度** (0-100分)
  - 需求明确性
  - KPI明确性
  - 预算和时间计划

- **风险评估** (低/中/高)
  - 数据风险
  - 预算风险
  - 时间风险
  - KPI风险

**推荐路径：**
- **直接交付** - 需求明确，数据充足，可直接实施
- **试点项目** - 条件较好，建议小范围试点
- **PoC验证** - 需先进行概念验证

### 4. 匹配推荐引擎

**匹配算法：**

```
综合评分 = 
  行业匹配度 × 0.25 +
  语义相似度 × 0.30 +
  历史成功率 × 0.20 +
  预算匹配度 × 0.10 +
  地理位置 × 0.05 +
  信用评分 × 0.10
```

**匹配维度：**
- 行业标签匹配
- 技术能力语义相似度
- 供应商历史成功率
- 预算范围适配
- 地理位置便利性（重庆本地优先）
- 企业信用评分

**输出结果：**
- Top-N 供应商排序
- 匹配度百分比
- 可解释的匹配理由
- 供应商联系方式

## 📊 数据库设计

### 核心表结构

**enterprises** - 企业表
- id, eid (企业唯一识别码)
- 基本信息：name, credit_code, legal_person
- 分类：enterprise_type, industry_tags, size
- 联系方式：contact_*, address
- 认证：status, certification_level, credit_score

**users** - 用户表
- id, email, phone, hashed_password
- role (admin/enterprise_admin/enterprise_user/expert)
- enterprise_id (关联企业)

**demands** - 需求表
- id, enterprise_id
- 基本信息：title, description
- 标签：industry_tags, scenario_tags
- 目标：kpis, budget, timeline
- 数据：data_summary
- 评估结果：evaluation_result
- 匹配结果：match_results

## 🔧 API接口

### 认证接口
- POST `/api/v1/auth/register` - 用户注册
- POST `/api/v1/auth/login` - 用户登录

### 企业管理
- GET `/api/v1/enterprises` - 企业列表
- POST `/api/v1/enterprises` - 创建企业
- GET `/api/v1/enterprises/{id}` - 企业详情
- PUT `/api/v1/enterprises/{id}` - 更新企业
- POST `/api/v1/enterprises/{id}/verify` - 审核企业

### 需求管理
- GET `/api/v1/demands` - 需求列表
- POST `/api/v1/demands` - 创建需求
- GET `/api/v1/demands/{id}` - 需求详情
- PUT `/api/v1/demands/{id}` - 更新需求
- POST `/api/v1/demands/{id}/submit` - 提交需求
- POST `/api/v1/demands/{id}/evaluate` - 评估需求
- POST `/api/v1/demands/{id}/match` - 匹配供应商
- DELETE `/api/v1/demands/{id}` - 删除需求

## 🎯 MVP功能展示流程

### 演示流程建议：

1. **用户登录** - 展示认证系统
2. **查看工作台** - 统计数据概览
3. **浏览企业列表** - 需求方和供应方企业
4. **创建AI需求**
   - 填写结构化表单
   - 选择行业和场景标签
   - 设置预算和KPI
5. **智能评估**
   - 一键触发评估
   - 查看评估报告（可行性、就绪度、风险）
   - 获得改进建议
6. **匹配推荐**
   - 一键触发匹配
   - 查看Top-N供应商
   - 匹配度和理由展示
7. **查看需求详情** - 完整信息展示

## 🔮 后续扩展方向

### 已规划功能（未实现）

1. **向量语义检索**
   - 集成Milvus向量数据库
   - 使用Embedding模型进行语义匹配

2. **智脑OS集成**
   - 接入小易智联智脑OS
   - 增强评估和推荐能力

3. **项目孵化模块**
   - 投标管理
   - 在线协作（IM）
   - 项目进度追踪
   - 验收评价

4. **信用体系**
   - 双向评分
   - 投诉仲裁
   - 信用等级

5. **文件管理**
   - 样本数据上传
   - 证照管理
   - 项目交付物管理

6. **数据统计**
   - 可视化报表
   - 行业趋势分析
   - 平台运营数据

## 🐛 已知问题

- [ ] 数据健康度检测功能为模拟实现
- [ ] 语义相似度采用简单关键词匹配
- [ ] 历史成功率基于信用分模拟
- [ ] 文件上传功能未实现
- [ ] 邮件通知功能未实现

## 📝 开发注意事项

1. **数据库** - MVP使用SQLite，生产环境建议切换到PostgreSQL
2. **安全** - SECRET_KEY需在生产环境更换
3. **CORS** - 根据实际部署调整允许的域名
4. **认证** - JWT有效期为30分钟，可根据需求调整
5. **权限** - 当前权限控制较简单，生产环境需加强

## 🤝 贡献指南

本项目为MVP演示版本，如需扩展功能，请参考以下步骤：

1. 创建功能分支
2. 实现新功能
3. 编写测试用例
4. 提交Pull Request

## 📄 许可证

Copyright © 2024 重庆民营企业协会人工智能专委会 / 小易智联

---

**开发团队**: 小易智联  
**版本**: v1.0.0-MVP  
**最后更新**: 2024-10
