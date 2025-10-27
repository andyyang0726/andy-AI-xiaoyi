from sqlalchemy import Column, Integer, String, Enum, DateTime, JSON, Float, Text, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from ..core.database import Base


class DemandStatus(str, enum.Enum):
    """需求状态"""
    DRAFT = "draft"  # 草稿
    SUBMITTED = "submitted"  # 已提交
    EVALUATING = "evaluating"  # 评估中
    EVALUATED = "evaluated"  # 已评估
    MATCHING = "matching"  # 匹配中
    MATCHED = "matched"  # 已匹配
    IN_PROGRESS = "in_progress"  # 进行中
    COMPLETED = "completed"  # 已完成
    CLOSED = "closed"  # 已关闭


class ConfidentialityLevel(str, enum.Enum):
    """保密等级"""
    PUBLIC = "public"  # 公开
    INTERNAL = "internal"  # 内部
    CONFIDENTIAL = "confidential"  # 机密
    SECRET = "secret"  # 绝密


class Demand(Base):
    """需求表"""
    __tablename__ = "demands"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # 关联信息
    enterprise_id = Column(Integer, ForeignKey("enterprises.id"), nullable=False)
    
    # 基本信息
    title = Column(String(200), nullable=False, index=True)
    description = Column(Text, nullable=False)
    
    # 场景与标签
    industry_tags = Column(JSON, default=list)  # 行业标签
    scenario_tags = Column(JSON, default=list)  # 应用场景标签
    
    # 目标与KPI
    kpis = Column(JSON, default=list)  # [{"name": "准确率", "target": "95%", "metric": "accuracy"}]
    
    # 预算与时间
    budget_min = Column(Float, nullable=True)
    budget_max = Column(Float, nullable=True)
    timeline_start = Column(DateTime, nullable=True)
    timeline_end = Column(DateTime, nullable=True)
    
    # 数据资产
    data_summary = Column(JSON, default=dict)  # 数据健康摘要
    # {
    #   "types": ["image", "csv"],
    #   "counts": {"image": 12000, "csv": 50},
    #   "labeled_ratio": 0.2,
    #   "size_bytes": 1024000000,
    #   "health_score": 75
    # }
    
    # 保密与状态
    confidentiality = Column(Enum(ConfidentialityLevel), default=ConfidentialityLevel.INTERNAL)
    status = Column(Enum(DemandStatus), default=DemandStatus.DRAFT)
    priority = Column(Integer, default=5)  # 1-10，10最高
    
    # 评估结果
    evaluation_result = Column(JSON, nullable=True)
    # {
    #   "feasibility_score": 85,
    #   "readiness_score": 70,
    #   "risk_level": "medium",
    #   "recommended_path": "poc",
    #   "confidence": 0.8,
    #   "notes": ["需要更多样本数据", "建议先进行PoC验证"]
    # }
    
    # 推荐结果
    match_results = Column(JSON, default=list)
    # [
    #   {
    #     "vendor_id": 123,
    #     "score": 0.87,
    #     "reasons": ["行业经验丰富", "语义相似度高", "成功率高"]
    #   }
    # ]
    
    # 时间戳
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    submitted_at = Column(DateTime, nullable=True)
    
    # 关系
    enterprise = relationship("Enterprise", back_populates="demands")
