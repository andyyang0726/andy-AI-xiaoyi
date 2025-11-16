# 企业AI需求对接平台

[![部署状态](https://img.shields.io/badge/部署-成功-brightgreen)](https://andyyang0726.github.io/andy-AI-xiaoyi/)
[![技术栈](https://img.shields.io/badge/React-18-blue)](https://react.dev/)
[![后端](https://img.shields.io/badge/FastAPI-最新-green)](https://fastapi.tiangolo.com/)
[![许可证](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

企业AI需求对接平台是一个智能化的AI供需匹配系统，通过智能评估引擎和匹配推荐算法，帮助需求方企业找到最合适的AI供应商，提升对接效率和成功率。

## 🌟 核心特性

### 1. 供应商企业注册入驻 ⭐ NEW
- **4步渐进式注册流程**：基本信息 → AI能力 → 行业经验 → 成功案例
- **AI能力详细展示**：12种技术方向，支持多个能力详情（技术栈、专业水平、成功案例）
- **实时完成度评分**：0-100分动态评分，激励用户完善信息
- **成功案例结构化**：项目背景、解决方案、项目成果三段式展示
- **企业信息预览**：实时预览最终展示效果
- **智能表单验证**：必填项、格式、长度、唯一性全面验证
- 📚 [查看详细文档](SUPPLIER_REGISTRATION_GUIDE.md)
- 🚀 [快速开始指南](SUPPLIER_REGISTRATION_QUICKSTART.md)
- 🎬 [演示说明](DEMO_SUPPLIER_REGISTRATION.md)

### 2. 智能需求评估引擎
- **多维度评估**：数据健康度、技术可行性、项目准备度
- **规则引擎**：基于行业最佳实践的智能评估规则
- **详细报告**：生成专业的需求评估报告和改进建议

### 3. 智能匹配推荐系统
- **双向匹配**：需求→供应商（正向）+ 供应商→需求（反向）
- **6维度算法**：
  - 行业匹配度 (25%)
  - 语义相似度 (30%)
  - 历史成功率 (20%)
  - 预算匹配度 (10%)
  - 地理位置 (5%)
  - 企业信用 (10%)
- **排序优化**：综合加权评分，推荐最优供应商
- **可解释性**：展示各维度得分，增强推荐透明度

### 4. 企业认证体系
- **信用评分**：基于多维度的企业信用评分系统
- **认证等级**：优选企业、认证企业、普通企业
- **能力标签**：AI技术能力标签展示
- **详细档案**：能力详情、行业经验、成功案例完整展示

### 5. 需求全生命周期管理
- **需求提交**：结构化的需求提交表单
- **状态跟踪**：待审核、已发布、匹配中、已完成
- **协作功能**：需求方与供应方在线沟通

### 6. 供应方功能
- **供应方主页**：企业信息卡片、统计数据、TOP5推荐需求
- **推荐需求列表**：智能匹配的需求，显示匹配分数和详细评分
- **需求浏览**：查看所有公开发布的需求（公开平台模式）

## 🚀 快速访问

### 🌐 在线体验

#### 生产环境 (推荐)
- **前端应用**: https://andyyang0726.github.io/andy-AI-xiaoyi/
- **部署方式**: GitHub Pages
- **状态**: ✅ 24/7在线稳定运行

#### 开发环境 (完整功能体验)
- **前端应用**: https://5174-ihia78ehq6oi6tkbljqri-02b9cc79.sandbox.novita.ai
- **后端API**: https://8000-ihia78ehq6oi6tkbljqri-02b9cc79.sandbox.novita.ai
- **API文档**: https://8000-ihia78ehq6oi6tkbljqri-02b9cc79.sandbox.novita.ai/docs
- **状态**: ✅ 开发调试环境

> 💡 **使用建议**: 生产环境访问速度更快；开发环境可体验完整后端功能

### 测试账号
```
供应方（小易智联）- 推荐使用 ⭐:
邮箱: xiaoyi@xiaoyi.ai
密码: xiaoyi123
特点: 96分信用，优选企业，2个AI能力详情，2个成功案例

需求方（长安汽车）:
邮箱: changan@demo.com
密码: demo123

管理员:
邮箱: admin@platform.com
密码: admin123
```

### 供应商企业入驻
新供应商企业可以通过以下方式注册：
1. 访问：https://andyyang0726.github.io/andy-AI-xiaoyi/login
2. 点击"供应商企业入驻"按钮
3. 按照4步流程填写详细信息
4. 提交后等待审核（3个工作日内）

💡 建议资料完成度达到80分以上，可获得更多精准推荐！

## 📁 项目结构

```
andy-AI-xiaoyi/
├── frontend/                 # 前端应用
│   ├── src/
│   │   ├── components/      # React组件
│   │   ├── pages/           # 页面组件
│   │   ├── services/        # API服务
│   │   └── App.jsx          # 主应用组件
│   ├── dist/                # 构建输出（部署到GitHub Pages）
│   └── vite.config.js       # Vite配置
│
├── backend/                  # 后端应用
│   ├── app/
│   │   ├── api/             # API路由
│   │   ├── models/          # 数据模型
│   │   ├── services/        # 业务逻辑
│   │   │   ├── evaluation_service.py    # 评估引擎
│   │   │   └── matching_service.py      # 匹配算法
│   │   ├── core/            # 核心配置
│   │   └── main.py          # FastAPI应用入口
│   ├── init_db.py           # 数据库初始化
│   └── requirements.txt     # Python依赖
│
├── USER_GUIDE.md            # 详细使用指南
├── DEPLOYMENT_FIX.md        # 部署问题修复说明
└── README.md                # 项目说明（本文件）
```

## 🛠️ 技术栈

### 前端
- **React 18** - 现代化的UI框架
- **Ant Design 5** - 企业级UI组件库
- **Vite** - 快速的构建工具
- **React Router v6** - 客户端路由
- **Axios** - HTTP客户端

### 后端
- **FastAPI** - 高性能Python Web框架
- **SQLAlchemy** - Python ORM
- **SQLite** - 轻量级数据库
- **JWT** - 身份认证
- **bcrypt** - 密码加密
- **Pydantic** - 数据验证

### 部署
- **GitHub Pages** - 前端静态托管
- **沙箱环境** - 后端API托管（临时）

## 📦 本地开发

### 前端开发

```bash
# 安装依赖
cd frontend
npm install

# 启动开发服务器
npm run dev

# 访问 http://localhost:5173
```

### 后端开发

```bash
# 创建虚拟环境
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 初始化数据库
python init_db.py

# 启动开发服务器
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 访问 http://localhost:8000/api/docs
```

## 🔧 构建和部署

### 前端构建
```bash
cd frontend
npm run build
```

### 部署到GitHub Pages
```bash
# 提交代码
git add -A
git commit -m "update: 更新内容"
git push origin main

# 部署到gh-pages分支
git subtree push --prefix frontend/dist origin gh-pages
```

## 📊 数据库设计

### 核心表结构

#### enterprises (企业表)
- `id`: 主键
- `eid`: 企业唯一识别码
- `name`: 企业名称
- `enterprise_type`: 企业类型（需求方/供应方）
- `industry_tags`: 行业标签
- `ai_capabilities`: AI能力标签
- `credit_score`: 信用评分
- `certification_level`: 认证等级
- `capability_details`: AI能力详情列表（JSON）⭐ NEW
- `industry_experience`: 行业经验列表（JSON）⭐ NEW
- `success_cases`: 成功案例列表（JSON）⭐ NEW
- `team_size`: 团队规模 ⭐ NEW
- `team_structure`: 团队构成 ⭐ NEW
- `certifications`: 认证资质（JSON）⭐ NEW

#### users (用户表)
- `id`: 主键
- `email`: 邮箱
- `hashed_password`: 加密密码
- `role`: 用户角色
- `enterprise_id`: 关联企业

#### demands (需求表)
- `id`: 主键
- `enterprise_id`: 发布企业
- `title`: 需求标题
- `description`: 需求描述
- `industry_tags`: 行业标签
- `scenario_tags`: 场景标签
- `kpis`: KPI指标
- `budget_min/max`: 预算范围
- `data_summary`: 数据摘要
- `status`: 需求状态

## 🤖 智能算法

### 需求评估引擎

基于规则引擎的多维度评估系统：

1. **数据健康度评估** (0-100分)
   - 数据量充足性 (40%)
   - 数据标注率 (40%)
   - 数据质量评分 (20%)

2. **技术可行性评估** (0-100分)
   - 技术成熟度分析
   - 实现难度评估
   - 技术栈匹配度

3. **项目准备度评估** (0-100分)
   - 需求明确度
   - 资源准备情况
   - 团队能力评估

### 匹配推荐算法

基于加权评分的多维度匹配系统：

```python
综合得分 = 行业匹配(25%) + 语义相似(30%) + 成功率(20%) 
         + 预算匹配(10%) + 地理位置(5%) + 信用评分(10%)
```

**关键技术**：
- TF-IDF文本相似度计算
- Jaccard相似度（标签匹配）
- 地理位置距离计算
- 归一化评分算法

## 📈 功能路线图

### MVP版本 (v1.0) - 已完成 ✅
- [x] 用户认证系统
- [x] 企业管理功能
- [x] 需求发布与管理
- [x] 智能评估引擎
- [x] 双向智能匹配推荐
- [x] 数据看板
- [x] 供应商企业注册入驻 ⭐ NEW
- [x] 供应方主页和推荐需求 ⭐ NEW
- [x] 公开平台模式（供应商可查看所有需求）⭐ NEW

### 下一版本 (v1.1) - 规划中
- [ ] 在线沟通功能
- [ ] 合同管理系统
- [ ] 项目进度跟踪
- [ ] 支付集成
- [ ] 消息通知系统
- [ ] 移动端适配

### 未来版本 (v2.0)
- [ ] 深度学习推荐算法
- [ ] 知识图谱构建
- [ ] 智能客服机器人
- [ ] 数据分析报告
- [ ] 第三方服务集成

## 🔍 核心代码示例

### 智能评估引擎
```python
# backend/app/services/evaluation_service.py
class EvaluationService:
    def evaluate_demand(self, demand: Demand) -> EvaluationResult:
        """
        多维度需求评估
        """
        # 数据健康度评估
        data_health_score = self._evaluate_data_health(demand)
        
        # 技术可行性评估
        tech_feasibility_score = self._evaluate_tech_feasibility(demand)
        
        # 项目准备度评估
        project_readiness_score = self._evaluate_project_readiness(demand)
        
        # 综合评分
        overall_score = (data_health_score + tech_feasibility_score + 
                        project_readiness_score) / 3
        
        return EvaluationResult(...)
```

### 智能匹配算法
```python
# backend/app/services/matching_service.py
class MatchingService:
    def find_matching_enterprises(self, demand: Demand) -> List[MatchResult]:
        """
        6维度智能匹配
        """
        suppliers = self._get_supply_enterprises()
        
        matches = []
        for supplier in suppliers:
            # 行业匹配度 (25%)
            industry_score = self._calculate_industry_match(demand, supplier)
            
            # 语义相似度 (30%)
            semantic_score = self._calculate_semantic_similarity(demand, supplier)
            
            # 历史成功率 (20%)
            success_rate_score = self._get_success_rate(supplier)
            
            # 预算匹配度 (10%)
            budget_score = self._calculate_budget_match(demand, supplier)
            
            # 地理位置 (5%)
            location_score = self._calculate_location_score(demand, supplier)
            
            # 企业信用 (10%)
            credit_score = supplier.credit_score / 100
            
            # 综合评分
            total_score = (industry_score * 0.25 + semantic_score * 0.30 +
                          success_rate_score * 0.20 + budget_score * 0.10 +
                          location_score * 0.05 + credit_score * 0.10)
            
            matches.append(MatchResult(...))
        
        return sorted(matches, key=lambda x: x.total_score, reverse=True)
```

## 🐛 已知问题

1. ~~GitHub Pages空白页~~ ✅ 已修复
   - 已添加Router basename配置
   - 已更新CORS设置

2. 沙箱环境限制
   - 后端URL可能会变化
   - 建议生产环境部署到稳定服务器

## 🤝 贡献指南

欢迎提交Issue和Pull Request！

1. Fork本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

## 📞 联系方式

- **项目维护者**: Andy Yang
- **GitHub**: [@andyyang0726](https://github.com/andyyang0726)
- **仓库地址**: https://github.com/andyyang0726/andy-AI-xiaoyi

## 🙏 致谢

感谢以下开源项目：
- [React](https://react.dev/)
- [Ant Design](https://ant.design/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [Vite](https://vitejs.dev/)

---

**最后更新**: 2025-10-27  
**版本**: v1.0.0  
**状态**: ✅ 生产就绪

---

📚 **更多文档**:
- [详细使用指南](USER_GUIDE.md)
- [部署修复说明](DEPLOYMENT_FIX.md)
- [供应商注册功能说明](SUPPLIER_REGISTRATION_GUIDE.md) ⭐ NEW
- [供应商注册快速指南](SUPPLIER_REGISTRATION_QUICKSTART.md) ⭐ NEW
- [供应商注册演示说明](DEMO_SUPPLIER_REGISTRATION.md) ⭐ NEW
- [供应商注册开发总结](SUPPLIER_REGISTRATION_SUMMARY.md) ⭐ NEW
- [API文档](https://8000-ihia78ehq6oi6tkbljqri-02b9cc79.sandbox.novita.ai/api/docs)
