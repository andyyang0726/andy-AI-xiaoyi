from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from ..models.demand import DemandStatus, ConfidentialityLevel


class KPIItem(BaseModel):
    """KPI项"""
    name: str
    target: str
    metric: str


class DemandBase(BaseModel):
    """需求基础信息"""
    title: str = Field(..., min_length=5, max_length=200)
    description: str = Field(..., min_length=10)
    industry_tags: List[str] = Field(default_factory=list)
    scenario_tags: List[str] = Field(default_factory=list)
    kpis: List[KPIItem] = Field(default_factory=list)
    budget_min: Optional[float] = None
    budget_max: Optional[float] = None
    timeline_start: Optional[datetime] = None
    timeline_end: Optional[datetime] = None
    confidentiality: ConfidentialityLevel = ConfidentialityLevel.INTERNAL
    priority: int = Field(default=5, ge=1, le=10)


class DemandCreate(DemandBase):
    """创建需求"""
    enterprise_id: int


class DemandUpdate(BaseModel):
    """更新需求"""
    title: Optional[str] = None
    description: Optional[str] = None
    industry_tags: Optional[List[str]] = None
    scenario_tags: Optional[List[str]] = None
    kpis: Optional[List[KPIItem]] = None
    budget_min: Optional[float] = None
    budget_max: Optional[float] = None
    timeline_start: Optional[datetime] = None
    timeline_end: Optional[datetime] = None
    confidentiality: Optional[ConfidentialityLevel] = None
    priority: Optional[int] = None
    status: Optional[DemandStatus] = None


class DataSummary(BaseModel):
    """数据摘要"""
    types: List[str] = Field(default_factory=list)
    counts: Dict[str, int] = Field(default_factory=dict)
    labeled_ratio: float = 0.0
    size_bytes: int = 0
    health_score: float = 0.0


class EvaluationResult(BaseModel):
    """评估结果"""
    feasibility_score: float = Field(..., ge=0, le=100)
    readiness_score: float = Field(..., ge=0, le=100)
    risk_level: str  # low, medium, high
    recommended_path: str  # direct, poc, pilot
    confidence: float = Field(..., ge=0, le=1)
    notes: List[str] = Field(default_factory=list)


class MatchResult(BaseModel):
    """匹配结果"""
    vendor_id: int
    vendor_name: str
    score: float
    reasons: List[str]


class DemandResponse(DemandBase):
    """需求响应"""
    id: int
    enterprise_id: int
    status: DemandStatus
    data_summary: Optional[Dict[str, Any]] = None
    evaluation_result: Optional[Dict[str, Any]] = None
    match_results: List[Dict[str, Any]] = Field(default_factory=list)
    created_at: datetime
    updated_at: datetime
    submitted_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class DemandListResponse(BaseModel):
    """需求列表响应"""
    total: int
    items: List[DemandResponse]


class DemandEvaluateRequest(BaseModel):
    """评估请求"""
    demand_id: int


class DemandEvaluateResponse(BaseModel):
    """评估响应"""
    demand_id: int
    evaluation: EvaluationResult
    message: str
