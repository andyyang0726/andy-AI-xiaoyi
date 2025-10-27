# 重庆人工智能供需对接平台

[![部署状态](https://img.shields.io/badge/部署-成功-brightgreen)](https://andyyang0726.github.io/andy-AI-xiaoyi/)
[![技术栈](https://img.shields.io/badge/React-18-blue)](https://react.dev/)
[![后端](https://img.shields.io/badge/FastAPI-最新-green)](https://fastapi.tiangolo.com/)
[![许可证](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

重庆人工智能供需对接平台是一个智能化的AI供需匹配系统，通过智能评估引擎和匹配推荐算法，帮助需求方企业找到最合适的AI供应商，提升对接效率和成功率。

## 🌟 核心特性

### 1. 智能需求评估引擎
- **多维度评估**：数据健康度、技术可行性、项目准备度
- **规则引擎**：基于行业最佳实践的智能评估规则
- **详细报告**：生成专业的需求评估报告和改进建议

### 2. 智能匹配推荐系统
- **6维度算法**：
  - 行业匹配度 (25%)
  - 语义相似度 (30%)
  - 历史成功率 (20%)
  - 预算匹配度 (10%)
  - 地理位置 (5%)
  - 企业信用 (10%)
- **排序优化**：综合加权评分，推荐最优供应商
- **可解释性**：展示各维度得分，增强推荐透明度

### 3. 企业认证体系
- **信用评分**：基于多维度的企业信用评分系统
- **认证等级**：优选企业、认证企业、普通企业
- **能力标签**：AI技术能力标签展示

### 4. 需求全生命周期管理
- **需求提交**：结构化的需求提交表单
- **状态跟踪**：待审核、已发布、匹配中、已完成
- **协作功能**：需求方与供应方在线沟通

## 🚀 快速访问

### 在线体验
- **前端应用**: https://andyyang0726.github.io/andy-AI-xiaoyi/
- **API文档**: https://8000-ihia78ehq6oi6tkbljqri-02b9cc79.sandbox.novita.ai/api/docs

### 测试账号
```
需求方（长安汽车）:
邮箱: changan@demo.com
密码: demo123

供应方（小易智联）:
邮箱: xiaoyi@demo.com
密码: demo123

管理员:
邮箱: admin@platform.com
密码: demo123
```

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
- [x] 智能匹配推荐
- [x] 数据看板

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
- [API文档](https://8000-ihia78ehq6oi6tkbljqri-02b9cc79.sandbox.novita.ai/api/docs)
