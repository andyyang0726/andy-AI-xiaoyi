"""
匹配推荐服务
基于多维度评分实现需求与供应商的智能匹配
"""
from typing import List, Dict, Any
import random
from sqlalchemy.orm import Session
from ..models import Enterprise, EnterpriseType


class MatchingService:
    """匹配推荐服务类"""
    
    def __init__(self):
        # 权重配置
        self.weights = {
            "industry_match": 0.25,      # 行业匹配度
            "semantic_similarity": 0.30,  # 语义相似度
            "success_rate": 0.20,         # 历史成功率
            "budget_match": 0.10,         # 预算适配度
            "geo_proximity": 0.05,        # 地理位置
            "credit_score": 0.10          # 信用评分
        }
    
    def match_demands_for_vendor(
        self,
        vendor: Enterprise,
        db: Session,
        top_k: int = 10
    ) -> List[Dict[str, Any]]:
        """
        为供应商推荐合适的需求（反向匹配）
        
        Args:
            vendor: 供应商企业对象
            db: 数据库会话
            top_k: 返回top K个结果
            
        Returns:
            推荐需求列表
        """
        from ..models import Demand, DemandStatus
        
        # 获取所有已发布的需求
        demands = db.query(Demand).filter(
            Demand.status.in_([DemandStatus.SUBMITTED, DemandStatus.EVALUATED, DemandStatus.MATCHED])
        ).all()
        
        if not demands:
            return []
        
        # 为每个需求计算匹配分数
        matches = []
        for demand in demands:
            demand_data = {
                "title": demand.title,
                "description": demand.description,
                "industry_tags": demand.industry_tags or [],
                "scenario_tags": demand.scenario_tags or [],
                "budget_max": demand.budget_max or 0,
                "enterprise_location": "重庆"
            }
            
            score_breakdown = self._calculate_match_score(demand_data, vendor)
            
            matches.append({
                "demand_id": demand.id,
                "demand_title": demand.title,
                "demand_description": demand.description[:200] + "..." if len(demand.description) > 200 else demand.description,
                "enterprise_id": demand.enterprise_id,
                "industry_tags": demand.industry_tags,
                "scenario_tags": demand.scenario_tags,
                "budget_range": f"{demand.budget_min}-{demand.budget_max}" if demand.budget_min and demand.budget_max else "面议",
                "score": score_breakdown["total_score"],
                "score_breakdown": score_breakdown,
                "match_reasons": self._generate_match_reasons(score_breakdown),
                "created_at": demand.created_at.isoformat() if demand.created_at else None,
                "status": demand.status.value if demand.status else "submitted"
            })
        
        # 按分数排序
        matches.sort(key=lambda x: x["score"], reverse=True)
        
        return matches[:top_k]
    
    def match_vendors(
        self,
        demand_data: Dict[str, Any],
        db: Session,
        top_k: int = 5
    ) -> List[Dict[str, Any]]:
        """
        为需求匹配合适的供应商（正向匹配）
        
        Args:
            demand_data: 需求数据
            db: 数据库会话
            top_k: 返回top K个结果
            
        Returns:
            匹配结果列表
        """
        # 获取所有供应方企业
        vendors = db.query(Enterprise).filter(
            Enterprise.enterprise_type.in_([EnterpriseType.SUPPLY, EnterpriseType.BOTH]),
            Enterprise.status == "verified"
        ).all()
        
        if not vendors:
            return []
        
        # 为每个供应商计算匹配分数
        matches = []
        for vendor in vendors:
            score_breakdown = self._calculate_match_score(demand_data, vendor)
            
            matches.append({
                "vendor_id": vendor.id,
                "vendor_name": vendor.name,
                "vendor_eid": vendor.eid,
                "score": score_breakdown["total_score"],
                "score_breakdown": score_breakdown,
                "reasons": self._generate_match_reasons(score_breakdown),
                "contact_email": vendor.contact_email,
                "credit_score": vendor.credit_score,
                "ai_capabilities": vendor.ai_capabilities
            })
        
        # 按分数排序
        matches.sort(key=lambda x: x["score"], reverse=True)
        
        return matches[:top_k]
    
    def _calculate_match_score(
        self,
        demand_data: Dict[str, Any],
        vendor: Enterprise
    ) -> Dict[str, Any]:
        """计算单个供应商的匹配分数"""
        
        # 1. 行业匹配度
        industry_score = self._calc_industry_match(
            demand_data.get("industry_tags", []),
            vendor.industry_tags or []
        )
        
        # 2. 语义相似度（模拟）
        semantic_score = self._calc_semantic_similarity(
            demand_data.get("scenario_tags", []),
            vendor.ai_capabilities or []
        )
        
        # 3. 历史成功率（模拟）
        success_score = self._calc_success_rate(vendor)
        
        # 4. 预算匹配度
        budget_score = self._calc_budget_match(
            demand_data.get("budget_max", 0),
            vendor
        )
        
        # 5. 地理位置（重庆本地加分）
        geo_score = self._calc_geo_proximity(
            demand_data.get("enterprise_location", "重庆"),
            vendor.address or ""
        )
        
        # 6. 信用评分
        credit_score = self._normalize_credit_score(vendor.credit_score)
        
        # 计算加权总分
        total_score = (
            industry_score * self.weights["industry_match"] +
            semantic_score * self.weights["semantic_similarity"] +
            success_score * self.weights["success_rate"] +
            budget_score * self.weights["budget_match"] +
            geo_score * self.weights["geo_proximity"] +
            credit_score * self.weights["credit_score"]
        )
        
        return {
            "total_score": round(total_score * 100, 2),
            "industry_match": round(industry_score * 100, 2),
            "semantic_similarity": round(semantic_score * 100, 2),
            "success_rate": round(success_score * 100, 2),
            "budget_match": round(budget_score * 100, 2),
            "geo_proximity": round(geo_score * 100, 2),
            "credit_score": round(credit_score * 100, 2)
        }
    
    def _calc_industry_match(
        self,
        demand_industries: List[str],
        vendor_industries: List[str]
    ) -> float:
        """计算行业匹配度"""
        if not demand_industries or not vendor_industries:
            return 0.5  # 无标签时给中等分
        
        # 计算交集
        common = set(demand_industries) & set(vendor_industries)
        if common:
            return 1.0
        
        # 部分相关行业也给予一定分数
        return 0.3
    
    def _calc_semantic_similarity(
        self,
        demand_scenarios: List[str],
        vendor_capabilities: List[str]
    ) -> float:
        """计算语义相似度（简化版本）"""
        if not demand_scenarios or not vendor_capabilities:
            return 0.5
        
        # 简单的关键词匹配
        demand_keywords = set(s.lower() for s in demand_scenarios)
        capability_keywords = set(c.lower() for c in vendor_capabilities)
        
        common = demand_keywords & capability_keywords
        
        if common:
            # Jaccard相似度
            union = demand_keywords | capability_keywords
            return len(common) / len(union)
        
        # 模糊匹配（包含关系）
        for demand_kw in demand_keywords:
            for cap_kw in capability_keywords:
                if demand_kw in cap_kw or cap_kw in demand_kw:
                    return 0.7
        
        return 0.4
    
    def _calc_success_rate(self, vendor: Enterprise) -> float:
        """计算历史成功率（模拟）"""
        # 在MVP阶段，基于信用分模拟
        # 实际应该从项目表中统计
        credit_score = vendor.credit_score
        
        if credit_score >= 90:
            return 0.95
        elif credit_score >= 80:
            return 0.85
        elif credit_score >= 70:
            return 0.75
        else:
            return 0.65
    
    def _calc_budget_match(self, demand_budget: float, vendor: Enterprise) -> float:
        """计算预算匹配度"""
        if demand_budget == 0:
            return 0.7  # 无预算信息给中等分
        
        # MVP阶段简化处理，所有供应商都能适配
        # 实际应该查询供应商的项目报价范围
        if demand_budget >= 100000:
            return 1.0
        elif demand_budget >= 50000:
            return 0.9
        else:
            return 0.7
    
    def _calc_geo_proximity(self, demand_location: str, vendor_location: str) -> float:
        """计算地理位置加分"""
        if "重庆" in demand_location and "重庆" in vendor_location:
            return 1.0
        elif "重庆" in vendor_location:
            return 0.8
        return 0.5
    
    def _normalize_credit_score(self, credit_score: float) -> float:
        """归一化信用分到0-1"""
        return credit_score / 100.0
    
    def _generate_match_reasons(self, score_breakdown: Dict[str, float]) -> List[str]:
        """生成匹配理由"""
        reasons = []
        
        # 找出得分最高的前3个维度
        scores = [
            ("行业经验丰富", score_breakdown["industry_match"]),
            ("技术能力匹配", score_breakdown["semantic_similarity"]),
            ("历史成功率高", score_breakdown["success_rate"]),
            ("预算范围适配", score_breakdown["budget_match"]),
            ("地理位置便利", score_breakdown["geo_proximity"]),
            ("信用评级优秀", score_breakdown["credit_score"])
        ]
        
        # 按分数排序
        scores.sort(key=lambda x: x[1], reverse=True)
        
        # 取前3个，且分数>70的
        for reason, score in scores[:3]:
            if score >= 70:
                reasons.append(reason)
        
        if not reasons:
            reasons.append("综合能力匹配")
        
        return reasons


# 创建全局匹配服务实例
matching_service = MatchingService()
