"""
完整系统功能测试
测试所有业务功能，不仅仅是RBAC权限
"""
import requests
import json
from datetime import datetime
from typing import Dict, List, Tuple

BASE_URL = "http://localhost:8000/api/v1"
TEST_ACCOUNTS = {
    "admin": {"email": "admin@platform.com", "password": "admin123"},
    "demand": {"email": "changan@demo.com", "password": "demo123"},
    "supply": {"email": "xiaoyi@demo.com", "password": "demo123"}
}

class FullSystemTester:
    """完整系统测试器"""
    
    def __init__(self):
        self.results = {
            "total": 0,
            "passed": 0,
            "failed": 0,
            "details": []
        }
        self.tokens = {}
        self.test_data = {}
    
    def login(self, role: str):
        """登录"""
        try:
            response = requests.post(
                f"{BASE_URL}/auth/login",
                json=TEST_ACCOUNTS[role]
            )
            if response.status_code == 200:
                data = response.json()
                self.tokens[role] = data["access_token"]
                return True
            return False
        except Exception as e:
            print(f"登录失败: {e}")
            return False
    
    def get_headers(self, role: str):
        """获取认证头"""
        return {"Authorization": f"Bearer {self.tokens[role]}"}
    
    def add_result(self, test_name: str, passed: bool, message: str = ""):
        """记录测试结果"""
        self.results["total"] += 1
        if passed:
            self.results["passed"] += 1
            status = "✅"
        else:
            self.results["failed"] += 1
            status = "❌"
        
        detail = f"{status} {test_name}: {message}"
        self.results["details"].append(detail)
        print(detail)
    
    def test_enterprise_registration(self):
        """测试企业注册功能"""
        print("\n" + "="*80)
        print("测试模块1: 企业注册与管理")
        print("="*80)
        
        # 测试供应商注册
        new_supplier = {
            "name": "测试供应商科技有限公司",
            "credit_code": f"91500000TEST{datetime.now().strftime('%H%M%S')}",
            "enterprise_type": "supply",
            "industry": "人工智能",
            "location": "重庆市渝北区",
            "contact_person": "张经理",
            "contact_phone": "13900000000",
            "contact_email": "test@supplier.com",
            "description": "测试用供应商企业"
        }
        
        try:
            response = requests.post(
                f"{BASE_URL}/enterprises/register",
                json=new_supplier
            )
            if response.status_code == 201:
                data = response.json()
                self.test_data["new_supplier_id"] = data["id"]
                self.add_result(
                    "供应商企业注册",
                    True,
                    f"成功注册，企业ID: {data['id']}, EID: {data['eid']}"
                )
            else:
                self.add_result("供应商企业注册", False, f"状态码: {response.status_code}")
        except Exception as e:
            self.add_result("供应商企业注册", False, str(e))
        
        # 测试管理员查看企业详情
        if "new_supplier_id" in self.test_data:
            try:
                enterprise_id = self.test_data["new_supplier_id"]
                response = requests.get(
                    f"{BASE_URL}/enterprises/{enterprise_id}",
                    headers=self.get_headers("admin")
                )
                if response.status_code == 200:
                    data = response.json()
                    self.add_result(
                        "查看企业详情",
                        True,
                        f"成功获取企业: {data['name']}, 状态: {data['status']}"
                    )
                else:
                    self.add_result("查看企业详情", False, f"状态码: {response.status_code}")
            except Exception as e:
                self.add_result("查看企业详情", False, str(e))
        
        # 测试管理员审核企业
        if "new_supplier_id" in self.test_data:
            try:
                enterprise_id = self.test_data["new_supplier_id"]
                response = requests.post(
                    f"{BASE_URL}/enterprises/{enterprise_id}/verify",
                    headers=self.get_headers("admin"),
                    params={"approve": True}
                )
                if response.status_code == 200:
                    data = response.json()
                    self.add_result(
                        "企业审核",
                        True,
                        f"审核通过，状态: {data['status']}"
                    )
                else:
                    self.add_result("企业审核", False, f"状态码: {response.status_code}")
            except Exception as e:
                self.add_result("企业审核", False, str(e))
    
    def test_demand_lifecycle(self):
        """测试需求全生命周期"""
        print("\n" + "="*80)
        print("测试模块2: 需求全生命周期")
        print("="*80)
        
        # 获取需求方的企业ID
        try:
            response = requests.get(
                f"{BASE_URL}/enterprises",
                headers=self.get_headers("demand"),
                params={"limit": 1}
            )
            if response.status_code == 200:
                data = response.json()
                if data["total"] > 0:
                    enterprise_id = data["items"][0]["id"]
                    self.test_data["demand_enterprise_id"] = enterprise_id
                else:
                    self.add_result("获取需求方企业", False, "没有关联企业")
                    return
        except Exception as e:
            self.add_result("获取需求方企业", False, str(e))
            return
        
        # 1. 创建需求
        new_demand = {
            "title": "智能客服系统开发需求",
            "description": "需要开发一套基于AI的智能客服系统，支持多轮对话和知识库问答",
            "enterprise_id": self.test_data["demand_enterprise_id"],
            "industry_tags": ["人工智能", "客服系统"],
            "scenario_tags": ["客户服务", "智能问答"],
            "budget_min": 100000,
            "budget_max": 300000,
            "timeline_start": "2025-01-01T00:00:00",
            "timeline_end": "2025-06-30T23:59:59",
            "kpis": [
                {"name": "响应时间", "target": "< 2秒", "metric": "响应时间（秒）"},
                {"name": "准确率", "target": "> 90%", "metric": "回答准确率（%）"}
            ]
        }
        
        try:
            response = requests.post(
                f"{BASE_URL}/demands",
                json=new_demand,
                headers=self.get_headers("demand")
            )
            if response.status_code == 201:
                data = response.json()
                self.test_data["new_demand_id"] = data["id"]
                self.add_result(
                    "创建需求",
                    True,
                    f"成功创建，需求ID: {data['id']}, 标题: {data['title']}"
                )
            else:
                self.add_result("创建需求", False, f"状态码: {response.status_code}, {response.text}")
        except Exception as e:
            self.add_result("创建需求", False, str(e))
        
        # 2. 查看需求详情
        if "new_demand_id" in self.test_data:
            try:
                demand_id = self.test_data["new_demand_id"]
                response = requests.get(
                    f"{BASE_URL}/demands/{demand_id}",
                    headers=self.get_headers("demand")
                )
                if response.status_code == 200:
                    data = response.json()
                    self.add_result(
                        "查看需求详情",
                        True,
                        f"成功获取，状态: {data['status']}"
                    )
                else:
                    self.add_result("查看需求详情", False, f"状态码: {response.status_code}")
            except Exception as e:
                self.add_result("查看需求详情", False, str(e))
        
        # 3. 更新需求
        if "new_demand_id" in self.test_data:
            try:
                demand_id = self.test_data["new_demand_id"]
                update_data = {
                    "description": "更新：需要开发一套基于AI的智能客服系统，支持多轮对话、知识库问答和情感分析"
                }
                response = requests.put(
                    f"{BASE_URL}/demands/{demand_id}",
                    json=update_data,
                    headers=self.get_headers("demand")
                )
                if response.status_code == 200:
                    data = response.json()
                    self.add_result(
                        "更新需求",
                        True,
                        f"成功更新，描述已修改"
                    )
                else:
                    self.add_result("更新需求", False, f"状态码: {response.status_code}")
            except Exception as e:
                self.add_result("更新需求", False, str(e))
        
        # 4. 提交需求
        if "new_demand_id" in self.test_data:
            try:
                demand_id = self.test_data["new_demand_id"]
                response = requests.post(
                    f"{BASE_URL}/demands/{demand_id}/submit",
                    headers=self.get_headers("demand")
                )
                if response.status_code == 200:
                    data = response.json()
                    self.add_result(
                        "提交需求",
                        True,
                        f"成功提交，状态: {data['status']}"
                    )
                else:
                    self.add_result("提交需求", False, f"状态码: {response.status_code}")
            except Exception as e:
                self.add_result("提交需求", False, str(e))
        
        # 5. 评估需求
        if "new_demand_id" in self.test_data:
            try:
                demand_id = self.test_data["new_demand_id"]
                response = requests.post(
                    f"{BASE_URL}/demands/{demand_id}/evaluate",
                    headers=self.get_headers("demand")
                )
                if response.status_code == 200:
                    data = response.json()
                    evaluation = data.get("evaluation", {})
                    self.add_result(
                        "评估需求",
                        True,
                        f"评估完成，复杂度: {evaluation.get('complexity', 'N/A')}"
                    )
                else:
                    self.add_result("评估需求", False, f"状态码: {response.status_code}")
            except Exception as e:
                self.add_result("评估需求", False, str(e))
        
        # 6. 匹配供应商
        if "new_demand_id" in self.test_data:
            try:
                demand_id = self.test_data["new_demand_id"]
                response = requests.post(
                    f"{BASE_URL}/demands/{demand_id}/match",
                    headers=self.get_headers("demand"),
                    params={"top_k": 5}
                )
                if response.status_code == 200:
                    data = response.json()
                    match_results = data.get("match_results", [])
                    self.add_result(
                        "匹配供应商",
                        True,
                        f"匹配完成，找到 {len(match_results)} 个供应商"
                    )
                else:
                    self.add_result("匹配供应商", False, f"状态码: {response.status_code}")
            except Exception as e:
                self.add_result("匹配供应商", False, str(e))
    
    def test_qualification_management(self):
        """测试需求方资质管理"""
        print("\n" + "="*80)
        print("测试模块3: 需求方资质管理")
        print("="*80)
        
        if "demand_enterprise_id" not in self.test_data:
            self.add_result("资质管理", False, "没有需求方企业ID")
            return
        
        # 提交资质信息
        qualification_data = {
            "legal_representative": "李总",
            "registered_capital": "5000万元",
            "business_scope": "汽车制造、研发、销售",
            "contact_person": "王经理",
            "contact_phone": "13800138000",
            "contact_email": "wang@changan.com"
        }
        
        try:
            enterprise_id = self.test_data["demand_enterprise_id"]
            response = requests.put(
                f"{BASE_URL}/enterprises/{enterprise_id}/qualification",
                json=qualification_data,
                headers=self.get_headers("demand")
            )
            if response.status_code == 200:
                data = response.json()
                self.add_result(
                    "提交资质信息",
                    True,
                    f"提交成功，状态: {data.get('qualification_status', 'N/A')}"
                )
            else:
                self.add_result("提交资质信息", False, f"状态码: {response.status_code}")
        except Exception as e:
            self.add_result("提交资质信息", False, str(e))
    
    def test_recommendation_system(self):
        """测试推荐系统"""
        print("\n" + "="*80)
        print("测试模块4: 推荐系统")
        print("="*80)
        
        # 测试需求方查看推荐供应商
        try:
            response = requests.get(
                f"{BASE_URL}/recommendations/my-suppliers",
                headers=self.get_headers("demand"),
                params={"limit": 10}
            )
            if response.status_code == 200:
                data = response.json()
                total = data.get("total", 0)
                items = data.get("items", [])
                self.add_result(
                    "需求方查看推荐供应商",
                    True,
                    f"获取成功，共 {total} 个推荐"
                )
                
                # 检查推荐数据结构
                if items and len(items) > 0:
                    first_item = items[0]
                    has_demand = "demand" in first_item
                    has_suppliers = "matched_suppliers" in first_item
                    self.add_result(
                        "推荐数据结构",
                        has_demand and has_suppliers,
                        f"包含需求信息: {has_demand}, 包含供应商列表: {has_suppliers}"
                    )
            else:
                self.add_result("需求方查看推荐供应商", False, f"状态码: {response.status_code}")
        except Exception as e:
            self.add_result("需求方查看推荐供应商", False, str(e))
        
        # 测试供应方查看匹配客户
        try:
            response = requests.get(
                f"{BASE_URL}/recommendations/my-clients",
                headers=self.get_headers("supply"),
                params={"limit": 10}
            )
            if response.status_code == 200:
                data = response.json()
                total = data.get("total", 0)
                self.add_result(
                    "供应方查看匹配客户",
                    True,
                    f"获取成功，共 {total} 个匹配"
                )
            else:
                self.add_result("供应方查看匹配客户", False, f"状态码: {response.status_code}")
        except Exception as e:
            self.add_result("供应方查看匹配客户", False, str(e))
        
        # 测试管理员查看所有匹配
        try:
            response = requests.get(
                f"{BASE_URL}/recommendations/admin/all-matches",
                headers=self.get_headers("admin"),
                params={"limit": 10}
            )
            if response.status_code == 200:
                data = response.json()
                total = data.get("total", 0)
                self.add_result(
                    "管理员查看所有匹配",
                    True,
                    f"获取成功，共 {total} 个匹配"
                )
            else:
                self.add_result("管理员查看所有匹配", False, f"状态码: {response.status_code}")
        except Exception as e:
            self.add_result("管理员查看所有匹配", False, str(e))
    
    def test_supplier_demand_recommendation(self):
        """测试供应商获取推荐需求"""
        print("\n" + "="*80)
        print("测试模块5: 供应商推荐需求")
        print("="*80)
        
        # 获取供应方的企业ID
        try:
            response = requests.get(
                f"{BASE_URL}/enterprises",
                headers=self.get_headers("supply"),
                params={"limit": 1}
            )
            if response.status_code == 200:
                data = response.json()
                if data["total"] > 0:
                    enterprise_id = data["items"][0]["id"]
                    
                    # 获取推荐需求
                    response = requests.get(
                        f"{BASE_URL}/demands/recommended/{enterprise_id}",
                        headers=self.get_headers("supply"),
                        params={"top_k": 5}
                    )
                    if response.status_code == 200:
                        rec_data = response.json()
                        total = rec_data.get("total", 0)
                        self.add_result(
                            "供应商获取推荐需求",
                            True,
                            f"获取成功，共 {total} 个推荐需求"
                        )
                    else:
                        self.add_result("供应商获取推荐需求", False, f"状态码: {response.status_code}")
                else:
                    self.add_result("供应商获取推荐需求", False, "没有供应商企业")
            else:
                self.add_result("供应商获取推荐需求", False, f"状态码: {response.status_code}")
        except Exception as e:
            self.add_result("供应商获取推荐需求", False, str(e))
    
    def print_summary(self):
        """打印测试总结"""
        print("\n" + "="*80)
        print("完整系统功能测试总结")
        print("="*80)
        print(f"总测试数: {self.results['total']}")
        print(f"通过数量: {self.results['passed']} ✅")
        print(f"失败数量: {self.results['failed']} ❌")
        print(f"通过率: {(self.results['passed']/self.results['total']*100):.1f}%")
        print("="*80)
        
        if self.results['failed'] > 0:
            print("\n失败的测试:")
            for detail in self.results['details']:
                if "❌" in detail:
                    print(detail)
        
        return self.results

def main():
    """主测试流程"""
    print("="*80)
    print("完整系统功能测试")
    print("="*80)
    print(f"测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"API地址: {BASE_URL}")
    print("="*80)
    
    tester = FullSystemTester()
    
    # 登录所有角色
    print("\n登录测试账号...")
    for role in ["admin", "demand", "supply"]:
        if tester.login(role):
            print(f"✅ {role} 登录成功")
        else:
            print(f"❌ {role} 登录失败")
            return False
    
    # 执行测试模块
    tester.test_enterprise_registration()      # 企业注册与管理
    tester.test_demand_lifecycle()             # 需求全生命周期
    tester.test_qualification_management()     # 资质管理
    tester.test_recommendation_system()        # 推荐系统
    tester.test_supplier_demand_recommendation() # 供应商推荐需求
    
    # 打印总结
    results = tester.print_summary()
    
    # 保存报告
    report_file = f"full_system_test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump({
            "test_time": datetime.now().isoformat(),
            "results": results,
            "test_modules": [
                "企业注册与管理",
                "需求全生命周期",
                "资质管理",
                "推荐系统",
                "供应商推荐需求"
            ]
        }, f, ensure_ascii=False, indent=2)
    
    print(f"\n完整测试报告已保存到: {report_file}")
    
    return results['failed'] == 0

if __name__ == "__main__":
    import sys
    success = main()
    sys.exit(0 if success else 1)
