"""
智能评估服务 - 规则引擎实现
基于需求信息和数据健康度进行AI项目可行性评估
"""
from typing import Dict, List, Any
import random


class EvaluationService:
    """评估服务类"""
    
    # 行业成熟度权重（基于AI落地案例）
    INDUSTRY_MATURITY = {
        "制造业": 0.9,
        "金融": 0.85,
        "零售": 0.8,
        "医疗": 0.75,
        "政务": 0.7,
        "教育": 0.65,
        "其他": 0.5
    }
    
    # 场景难度系数
    SCENARIO_DIFFICULTY = {
        "图像识别": 0.8,
        "文本分类": 0.9,
        "语音识别": 0.75,
        "推荐系统": 0.85,
        "预测分析": 0.7,
        "目标检测": 0.65,
        "自然语言处理": 0.6,
        "其他": 0.5
    }
    
    def evaluate_demand(self, demand_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        评估需求可行性
        
        Args:
            demand_data: 需求数据字典
            
        Returns:
            评估结果字典
        """
        # 1. 数据健康度评分
        data_health_score = self._evaluate_data_health(demand_data.get("data_summary", {}))
        
        # 2. 技术可行性评分
        technical_feasibility = self._evaluate_technical_feasibility(demand_data)
        
        # 3. 项目就绪度评分
        readiness_score = self._evaluate_readiness(demand_data, data_health_score)
        
        # 4. 风险评估
        risk_level, risk_factors = self._evaluate_risks(demand_data, data_health_score)
        
        # 5. 推荐交付路径
        recommended_path = self._recommend_delivery_path(
            technical_feasibility,
            readiness_score,
            data_health_score
        )
        
        # 6. 综合评分
        overall_score = (technical_feasibility * 0.4 + 
                        readiness_score * 0.35 + 
                        data_health_score * 0.25)
        
        # 7. 生成建议
        notes = self._generate_recommendations(
            demand_data,
            data_health_score,
            technical_feasibility,
            readiness_score,
            risk_factors
        )
        
        # 8. 计算置信度
        confidence = self._calculate_confidence(demand_data, data_health_score)
        
        return {
            "feasibility_score": round(technical_feasibility, 2),
            "readiness_score": round(readiness_score, 2),
            "data_health_score": round(data_health_score, 2),
            "overall_score": round(overall_score, 2),
            "risk_level": risk_level,
            "risk_factors": risk_factors,
            "recommended_path": recommended_path,
            "confidence": round(confidence, 2),
            "notes": notes
        }
    
    def _evaluate_data_health(self, data_summary: Dict[str, Any]) -> float:
        """评估数据健康度"""
        if not data_summary:
            return 30.0  # 无数据信息，低分
        
        score = 50.0  # 基础分
        
        # 数据量评分
        total_count = sum(data_summary.get("counts", {}).values())
        if total_count >= 10000:
            score += 20
        elif total_count >= 5000:
            score += 15
        elif total_count >= 1000:
            score += 10
        elif total_count >= 100:
            score += 5
        
        # 标注率评分
        labeled_ratio = data_summary.get("labeled_ratio", 0)
        if labeled_ratio >= 0.8:
            score += 20
        elif labeled_ratio >= 0.5:
            score += 15
        elif labeled_ratio >= 0.2:
            score += 10
        elif labeled_ratio > 0:
            score += 5
        
        # 数据类型多样性
        data_types = data_summary.get("types", [])
        score += min(len(data_types) * 5, 10)
        
        return min(score, 100.0)
    
    def _evaluate_technical_feasibility(self, demand_data: Dict[str, Any]) -> float:
        """评估技术可行性"""
        score = 60.0  # 基础分
        
        # 行业成熟度加权
        industry_tags = demand_data.get("industry_tags", [])
        if industry_tags:
            industry = industry_tags[0] if industry_tags else "其他"
            maturity = self.INDUSTRY_MATURITY.get(industry, 0.5)
            score += maturity * 20
        
        # 场景难度评估
        scenario_tags = demand_data.get("scenario_tags", [])
        if scenario_tags:
            scenario = scenario_tags[0] if scenario_tags else "其他"
            difficulty = self.SCENARIO_DIFFICULTY.get(scenario, 0.5)
            score += difficulty * 20
        
        return min(score, 100.0)
    
    def _evaluate_readiness(self, demand_data: Dict[str, Any], data_health: float) -> float:
        """评估项目就绪度"""
        score = 40.0  # 基础分
        
        # 需求明确性
        if demand_data.get("description") and len(demand_data["description"]) > 100:
            score += 15
        
        # KPI明确性
        kpis = demand_data.get("kpis", [])
        if kpis and len(kpis) > 0:
            score += 15
        
        # 预算明确性
        if demand_data.get("budget_min") and demand_data.get("budget_max"):
            score += 10
        
        # 时间计划
        if demand_data.get("timeline_start") and demand_data.get("timeline_end"):
            score += 10
        
        # 数据准备度（与数据健康度挂钩）
        score += (data_health / 100) * 10
        
        return min(score, 100.0)
    
    def _evaluate_risks(self, demand_data: Dict[str, Any], data_health: float) -> tuple:
        """评估风险等级"""
        risk_factors = []
        risk_score = 0
        
        # 数据风险
        if data_health < 50:
            risk_factors.append("数据样本量不足或质量较低")
            risk_score += 30
        elif data_health < 70:
            risk_factors.append("数据准备度需要提升")
            risk_score += 15
        
        # 预算风险
        budget_max = demand_data.get("budget_max", 0)
        if budget_max < 100000:
            risk_factors.append("预算可能不足以支撑完整项目交付")
            risk_score += 20
        
        # 时间风险
        if not demand_data.get("timeline_end"):
            risk_factors.append("缺少明确的交付时间要求")
            risk_score += 10
        
        # KPI风险
        kpis = demand_data.get("kpis", [])
        if not kpis:
            risk_factors.append("缺少明确的效果评估指标")
            risk_score += 15
        
        # 保密性风险
        confidentiality = demand_data.get("confidentiality", "internal")
        if confidentiality in ["confidential", "secret"]:
            risk_factors.append("高保密等级可能限制供应商选择")
            risk_score += 10
        
        # 确定风险等级
        if risk_score >= 50:
            risk_level = "high"
        elif risk_score >= 25:
            risk_level = "medium"
        else:
            risk_level = "low"
        
        return risk_level, risk_factors
    
    def _recommend_delivery_path(
        self,
        technical_feasibility: float,
        readiness_score: float,
        data_health: float
    ) -> str:
        """推荐交付路径"""
        avg_score = (technical_feasibility + readiness_score + data_health) / 3
        
        if avg_score >= 80 and data_health >= 70:
            return "direct"  # 直接交付
        elif avg_score >= 60:
            return "pilot"  # 试点项目
        else:
            return "poc"  # 概念验证
    
    def _generate_recommendations(
        self,
        demand_data: Dict[str, Any],
        data_health: float,
        technical_feasibility: float,
        readiness_score: float,
        risk_factors: List[str]
    ) -> List[str]:
        """生成改进建议"""
        recommendations = []
        
        # 数据相关建议
        if data_health < 60:
            recommendations.append("建议增加数据样本数量，目标至少5000条以上")
        
        data_summary = demand_data.get("data_summary", {})
        labeled_ratio = data_summary.get("labeled_ratio", 0)
        if labeled_ratio < 0.5:
            recommendations.append("建议提高数据标注比例至50%以上，以提升模型训练效果")
        
        # 需求明确性建议
        if readiness_score < 70:
            if not demand_data.get("kpis"):
                recommendations.append("建议明确项目KPI指标，如准确率、召回率等具体目标")
            if not demand_data.get("budget_max"):
                recommendations.append("建议确定项目预算范围，便于匹配合适的供应商")
        
        # 技术路线建议
        if technical_feasibility < 70:
            recommendations.append("建议先进行技术预研和PoC验证，降低项目风险")
        
        # 行业特定建议
        industry_tags = demand_data.get("industry_tags", [])
        if "医疗" in industry_tags or "金融" in industry_tags:
            recommendations.append("注意相关行业的合规性要求和数据隐私保护")
        
        # 通用建议
        if len(recommendations) == 0:
            recommendations.append("需求准备充分，可以直接进入供应商匹配流程")
        
        return recommendations
    
    def _calculate_confidence(self, demand_data: Dict[str, Any], data_health: float) -> float:
        """计算评估置信度"""
        confidence = 0.5  # 基础置信度
        
        # 信息完整度提升置信度
        if demand_data.get("description") and len(demand_data["description"]) > 100:
            confidence += 0.1
        
        if demand_data.get("kpis"):
            confidence += 0.1
        
        if demand_data.get("data_summary"):
            confidence += 0.15
        
        if demand_data.get("budget_max"):
            confidence += 0.05
        
        if demand_data.get("industry_tags"):
            confidence += 0.05
        
        if demand_data.get("scenario_tags"):
            confidence += 0.05
        
        return min(confidence, 1.0)


# 创建全局评估服务实例
evaluation_service = EvaluationService()
