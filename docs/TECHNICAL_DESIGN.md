# 技术设计文档

## 一、系统架构

### 1.1 总体架构

```
┌─────────────────────────────────────────────────────┐
│                   用户层                              │
│  Web浏览器 / 移动端 / 小程序                           │
└─────────────────────────────────────────────────────┘
                        ▼
┌─────────────────────────────────────────────────────┐
│                  前端层 (React)                       │
│  - 用户界面组件                                        │
│  - 路由管理                                           │
│  - 状态管理                                           │
│  - API调用封装                                        │
└─────────────────────────────────────────────────────┘
                        ▼
┌─────────────────────────────────────────────────────┐
│               API网关层 (FastAPI)                     │
│  - 请求路由                                           │
│  - 认证鉴权                                           │
│  - 参数验证                                           │
│  - 响应序列化                                         │
└─────────────────────────────────────────────────────┘
                        ▼
┌─────────────────────────────────────────────────────┐
│                 业务逻辑层                            │
│  ┌──────────────┐  ┌──────────────┐                │
│  │ 评估服务      │  │ 匹配服务      │                │
│  │ - 可行性评估  │  │ - 多维匹配    │                │
│  │ - 风险分析    │  │ - 排序推荐    │                │
│  └──────────────┘  └──────────────┘                │
└─────────────────────────────────────────────────────┘
                        ▼
┌─────────────────────────────────────────────────────┐
│              数据访问层 (SQLAlchemy)                  │
│  - ORM模型                                            │
│  - 查询构建                                           │
│  - 事务管理                                           │
└─────────────────────────────────────────────────────┘
                        ▼
┌─────────────────────────────────────────────────────┐
│                 数据存储层                            │
│  - SQLite (MVP)                                      │
│  - 未来: PostgreSQL / MySQL                          │
└─────────────────────────────────────────────────────┘
```

## 二、核心模块设计

### 2.1 智能评估服务

**设计思路：**
基于规则引擎实现AI项目的可行性评估，考虑数据、技术、资源等多个维度。

**评分模型：**

1. **数据健康度评分 (0-100)**
   ```python
   score = 50  # 基础分
   
   # 数据量评分（最高20分）
   if total_count >= 10000: score += 20
   elif total_count >= 5000: score += 15
   elif total_count >= 1000: score += 10
   
   # 标注率评分（最高20分）
   if labeled_ratio >= 0.8: score += 20
   elif labeled_ratio >= 0.5: score += 15
   elif labeled_ratio >= 0.2: score += 10
   
   # 数据类型多样性（最高10分）
   score += min(len(data_types) * 5, 10)
   ```

2. **技术可行性评分 (0-100)**
   ```python
   score = 60  # 基础分
   
   # 行业成熟度加权（最高20分）
   maturity = INDUSTRY_MATURITY[industry]
   score += maturity * 20
   
   # 场景难度评估（最高20分）
   difficulty = SCENARIO_DIFFICULTY[scenario]
   score += difficulty * 20
   ```

3. **项目就绪度评分 (0-100)**
   ```python
   score = 40  # 基础分
   
   # 需求明确性（15分）
   if description_length > 100: score += 15
   
   # KPI明确性（15分）
   if has_kpis: score += 15
   
   # 预算明确性（10分）
   if has_budget: score += 10
   
   # 时间计划（10分）
   if has_timeline: score += 10
   
   # 数据准备度（10分）
   score += (data_health / 100) * 10
   ```

4. **风险评估**
   - 数据风险：数据量不足、质量低
   - 预算风险：预算不足
   - 时间风险：缺少时间计划
   - KPI风险：缺少评估指标
   - 保密风险：高保密等级限制

5. **交付路径推荐**
   ```python
   avg_score = (technical + readiness + data_health) / 3
   
   if avg_score >= 80 and data_health >= 70:
       return "direct"  # 直接交付
   elif avg_score >= 60:
       return "pilot"   # 试点项目
   else:
       return "poc"     # PoC验证
   ```

### 2.2 匹配推荐服务

**设计思路：**
基于多维度加权评分，实现需求与供应商的智能匹配。

**匹配算法：**

```python
MatchScore = 
    α * IndustryMatch      # 0.25 - 行业匹配度
  + β * SemanticSimilarity # 0.30 - 语义相似度
  + γ * SuccessRate        # 0.20 - 历史成功率
  + δ * BudgetMatch        # 0.10 - 预算适配度
  + ε * GeoProximity       # 0.05 - 地理位置
  + ζ * CreditScore        # 0.10 - 信用评分
```

**各维度计算：**

1. **行业匹配度**
   ```python
   def calc_industry_match(demand_industries, vendor_industries):
       common = set(demand_industries) & set(vendor_industries)
       if common: return 1.0  # 完全匹配
       return 0.3  # 部分相关
   ```

2. **语义相似度**（MVP版本使用关键词匹配）
   ```python
   def calc_semantic_similarity(demand_tags, vendor_capabilities):
       # Jaccard相似度
       common = demand_tags & vendor_capabilities
       union = demand_tags | vendor_capabilities
       return len(common) / len(union) if union else 0.5
   ```

3. **历史成功率**（MVP使用信用分模拟）
   ```python
   def calc_success_rate(vendor):
       credit_score = vendor.credit_score
       if credit_score >= 90: return 0.95
       elif credit_score >= 80: return 0.85
       elif credit_score >= 70: return 0.75
       else: return 0.65
   ```

4. **预算匹配度**
   ```python
   def calc_budget_match(demand_budget):
       if demand_budget >= 100000: return 1.0
       elif demand_budget >= 50000: return 0.9
       else: return 0.7
   ```

5. **地理位置**
   ```python
   def calc_geo_proximity(demand_loc, vendor_loc):
       if "重庆" in both: return 1.0  # 同城
       elif "重庆" in vendor: return 0.8  # 本地供应商
       return 0.5  # 其他
   ```

6. **信用评分**
   ```python
   def normalize_credit_score(credit_score):
       return credit_score / 100.0  # 归一化到0-1
   ```

**匹配理由生成：**
从6个维度中选择得分最高的前3个作为匹配理由展示。

## 三、数据模型设计

### 3.1 企业表 (enterprises)

| 字段 | 类型 | 说明 |
|------|------|------|
| id | Integer | 主键 |
| eid | String(50) | 企业唯一识别码 |
| name | String(200) | 企业名称 |
| credit_code | String(100) | 统一社会信用代码 |
| enterprise_type | Enum | demand/supply/both |
| industry_tags | JSON | 行业标签数组 |
| ai_capabilities | JSON | AI能力标签数组 |
| status | Enum | pending/verified/rejected |
| credit_score | Float | 信用分（0-100） |

### 3.2 用户表 (users)

| 字段 | 类型 | 说明 |
|------|------|------|
| id | Integer | 主键 |
| email | String(100) | 邮箱（唯一） |
| hashed_password | String(255) | 密码哈希 |
| role | Enum | admin/enterprise_admin/enterprise_user |
| enterprise_id | Integer | 关联企业ID |

### 3.3 需求表 (demands)

| 字段 | 类型 | 说明 |
|------|------|------|
| id | Integer | 主键 |
| enterprise_id | Integer | 企业ID |
| title | String(200) | 需求标题 |
| description | Text | 需求描述 |
| industry_tags | JSON | 行业标签 |
| scenario_tags | JSON | 场景标签 |
| kpis | JSON | KPI数组 |
| budget_min/max | Float | 预算范围 |
| data_summary | JSON | 数据摘要 |
| evaluation_result | JSON | 评估结果 |
| match_results | JSON | 匹配结果数组 |
| status | Enum | draft/submitted/evaluated/matched等 |

## 四、API设计

### 4.1 认证接口

**POST /api/v1/auth/register**
```json
Request:
{
  "email": "user@example.com",
  "password": "password123",
  "full_name": "张三",
  "phone": "13800138000"
}

Response:
{
  "id": 1,
  "email": "user@example.com",
  "full_name": "张三",
  "role": "enterprise_user",
  "is_active": true
}
```

**POST /api/v1/auth/login**
```json
Request:
{
  "email": "user@example.com",
  "password": "password123"
}

Response:
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer",
  "user": { ... }
}
```

### 4.2 需求评估接口

**POST /api/v1/demands/{id}/evaluate**

```json
Response:
{
  "demand_id": 1,
  "evaluation": {
    "feasibility_score": 85.5,
    "readiness_score": 72.0,
    "data_health_score": 88.0,
    "overall_score": 82.5,
    "risk_level": "medium",
    "risk_factors": [
      "预算可能不足以支撑完整项目交付"
    ],
    "recommended_path": "pilot",
    "confidence": 0.85,
    "notes": [
      "需求准备充分，可以直接进入供应商匹配流程"
    ]
  },
  "message": "需求评估完成"
}
```

### 4.3 匹配推荐接口

**POST /api/v1/demands/{id}/match?top_k=5**

```json
Response:
{
  "id": 1,
  "match_results": [
    {
      "vendor_id": 4,
      "vendor_name": "重庆小易智联科技有限公司",
      "vendor_eid": "EID-1234-ABCDEF",
      "score": 87.5,
      "score_breakdown": {
        "total_score": 87.5,
        "industry_match": 100.0,
        "semantic_similarity": 85.0,
        "success_rate": 95.0,
        "budget_match": 100.0,
        "geo_proximity": 100.0,
        "credit_score": 96.0
      },
      "reasons": [
        "行业经验丰富",
        "技术能力匹配",
        "历史成功率高"
      ],
      "contact_email": "chen@xiaoyi.ai",
      "credit_score": 96.0,
      "ai_capabilities": [
        "计算机视觉",
        "自然语言处理",
        "端侧部署"
      ]
    }
  ]
}
```

## 五、安全设计

### 5.1 认证机制

- **JWT Token认证**
  - 令牌有效期：30分钟
  - 算法：HS256
  - 载荷：user_id, email

- **密码安全**
  - bcrypt哈希算法
  - 密码最小长度：6位

### 5.2 权限控制

**角色定义：**
- `admin` - 平台管理员
- `enterprise_admin` - 企业管理员
- `enterprise_user` - 企业普通用户
- `expert` - 行业专家

### 5.3 数据安全

- SQL注入防护：使用ORM参数化查询
- XSS防护：前端输入验证和转义
- CSRF防护：CORS配置

## 六、性能优化

### 6.1 数据库优化

- 为常用查询字段添加索引
- 使用分页查询避免全表扫描
- 数据库连接池管理

### 6.2 API优化

- 响应数据序列化
- 合理的HTTP缓存策略
- 异步处理耗时操作

## 七、未来扩展

### 7.1 向量语义检索

- 集成Milvus向量数据库
- 使用Sentence-BERT生成文本向量
- 实现真正的语义相似度匹配

### 7.2 智脑OS集成

- 调用小易智联智脑OS API
- 增强评估能力
- 自然语言理解

### 7.3 实时推荐

- WebSocket实时通知
- 在线学习优化推荐算法
- A/B测试框架

### 7.4 微服务化

- 服务拆分：认证、评估、匹配、项目管理
- 服务网格：Istio
- 服务注册与发现：Consul/Etcd

## 八、部署架构

### 8.1 MVP部署

```
┌─────────────────┐
│  Nginx (反向代理) │
└─────────────────┘
         │
    ┌────┴────┐
    │         │
┌───▼───┐ ┌──▼──┐
│Frontend│ │FastAPI│
│ (静态) │ │ (API) │
└────────┘ └──┬───┘
              │
         ┌────▼────┐
         │ SQLite  │
         └─────────┘
```

### 8.2 生产部署（未来）

```
            ┌──────────┐
            │   CDN    │
            └──────────┘
                 │
         ┌───────▼────────┐
         │  Load Balancer  │
         └───────┬─────────┘
                 │
      ┌──────────┴──────────┐
      │                     │
┌─────▼─────┐       ┌──────▼──────┐
│  Frontend  │       │  API Cluster │
│  (Nginx)   │       │  (Uvicorn)  │
└────────────┘       └──────┬───────┘
                            │
                    ┌───────┴────────┐
                    │                │
              ┌─────▼─────┐   ┌─────▼──────┐
              │ PostgreSQL │   │   Milvus   │
              │  (Master)  │   │  (Vector)  │
              └────────────┘   └────────────┘
```

## 九、监控与运维

### 9.1 日志管理

- 应用日志：uvicorn日志
- 访问日志：nginx access.log
- 错误日志：应用异常追踪

### 9.2 性能监控

- API响应时间
- 数据库查询性能
- 系统资源使用率

### 9.3 告警机制

- 服务健康检查
- 错误率阈值告警
- 资源使用告警

## 十、测试策略

### 10.1 单元测试

- 业务逻辑测试
- 数据模型测试
- 工具函数测试

### 10.2 集成测试

- API接口测试
- 数据库操作测试
- 认证流程测试

### 10.3 端到端测试

- 用户操作流程测试
- 完整业务场景测试

---

**文档版本**: v1.0  
**最后更新**: 2024-10  
**维护**: 小易智联技术团队
