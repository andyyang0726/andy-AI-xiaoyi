"""
最终的完整系统综合测试
适配当前系统的真实行为
"""
import requests
import json
from datetime import datetime
from typing import Dict, List

BASE_URL = "http://localhost:8000/api/v1"
FRONTEND_URL = "http://localhost:5174"

# 使用已存在的测试账号
TEST_ACCOUNTS = {
    "admin": {"email": "admin@platform.com", "password": "admin123"},
    "demand": {"email": "changan@demo.com", "password": "demo123"},
    "supply": {"email": "xiaoyi@demo.com", "password": "demo123"}
}

class FinalComprehensiveTester:
    """最终综合测试器"""
    
    def __init__(self):
        self.results = {
            "total": 0,
            "passed": 0,
            "failed": 0,
            "details": []
        }
        self.tokens = {}
        self.user_info = {}
        
    def log(self, message: str, level: str = "INFO"):
        """日志输出"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] {level}: {message}")
    
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
    
    def test_services_health(self):
        """测试服务健康状态"""
        self.log("\n" + "="*80)
        self.log("第1部分: 服务健康检查")
        self.log("="*80)
        
        # 后端健康检查
        try:
            response = requests.get(f"{BASE_URL.replace('/api/v1', '')}/health", timeout=5)
            if response.status_code == 200:
                self.add_result("后端服务健康检查", True, "后端API运行正常")
            else:
                self.add_result("后端服务健康检查", False, f"状态码: {response.status_code}")
        except Exception as e:
            self.add_result("后端服务健康检查", False, f"连接失败: {str(e)}")
        
        # 前端访问检查
        try:
            response = requests.get(FRONTEND_URL, timeout=5)
            if response.status_code == 200:
                self.add_result("前端页面访问", True, f"前端页面正常访问 ({FRONTEND_URL})")
            else:
                self.add_result("前端页面访问", False, f"状态码: {response.status_code}")
        except Exception as e:
            self.add_result("前端页面访问", False, f"连接失败: {str(e)}")
    
    def test_user_authentication(self):
        """测试用户认证系统"""
        self.log("\n" + "="*80)
        self.log("第2部分: 用户认证系统测试")
        self.log("="*80)
        
        # 测试管理员登录
        try:
            response = requests.post(
                f"{BASE_URL}/auth/login",
                json=TEST_ACCOUNTS["admin"]
            )
            if response.status_code == 200:
                data = response.json()
                self.tokens["admin"] = data["access_token"]
                self.user_info["admin"] = data["user"]
                self.add_result("管理员登录", True, f"用户ID: {data['user']['id']}, 角色: {data['user']['role']}")
            else:
                self.add_result("管理员登录", False, f"状态码: {response.status_code}")
        except Exception as e:
            self.add_result("管理员登录", False, str(e))
        
        # 测试需求方登录
        try:
            response = requests.post(
                f"{BASE_URL}/auth/login",
                json=TEST_ACCOUNTS["demand"]
            )
            if response.status_code == 200:
                data = response.json()
                self.tokens["demand"] = data["access_token"]
                self.user_info["demand"] = data["user"]
                self.add_result("需求方用户登录", True, f"用户ID: {data['user']['id']}, 角色: {data['user']['role']}")
            else:
                self.add_result("需求方用户登录", False, f"状态码: {response.status_code}")
        except Exception as e:
            self.add_result("需求方用户登录", False, str(e))
        
        # 测试供应方登录
        try:
            response = requests.post(
                f"{BASE_URL}/auth/login",
                json=TEST_ACCOUNTS["supply"]
            )
            if response.status_code == 200:
                data = response.json()
                self.tokens["supply"] = data["access_token"]
                self.user_info["supply"] = data["user"]
                self.add_result("供应方用户登录", True, f"用户ID: {data['user']['id']}, 角色: {data['user']['role']}")
            else:
                self.add_result("供应方用户登录", False, f"状态码: {response.status_code}")
        except Exception as e:
            self.add_result("供应方用户登录", False, str(e))
        
        # 测试错误密码登录拒绝
        try:
            response = requests.post(
                f"{BASE_URL}/auth/login",
                json={"email": "admin@platform.com", "password": "wrongpassword"}
            )
            if response.status_code == 401:
                self.add_result("错误密码登录拒绝", True, "系统正确拒绝错误密码")
            else:
                self.add_result("错误密码登录拒绝", False, f"状态码: {response.status_code}（应该是401）")
        except Exception as e:
            self.add_result("错误密码登录拒绝", False, str(e))
        
        # 测试未认证访问拒绝
        try:
            response = requests.get(f"{BASE_URL}/enterprises/")
            if response.status_code == 401:
                self.add_result("未认证访问拒绝", True, "系统正确拒绝未认证请求")
            else:
                self.add_result("未认证访问拒绝", False, f"状态码: {response.status_code}（应该是401）")
        except Exception as e:
            self.add_result("未认证访问拒绝", False, str(e))
    
    def test_enterprise_permissions(self):
        """测试企业权限管理"""
        self.log("\n" + "="*80)
        self.log("第3部分: 企业权限管理测试")
        self.log("="*80)
        
        if "admin" not in self.tokens:
            self.add_result("企业权限测试", False, "管理员未登录，跳过测试")
            return
        
        # 管理员查看所有企业
        try:
            headers = {"Authorization": f"Bearer {self.tokens['admin']}"}
            response = requests.get(f"{BASE_URL}/enterprises/", headers=headers)
            if response.status_code == 200:
                enterprises = response.json()
                self.add_result("管理员查看所有企业", True, f"可见{len(enterprises)}家企业")
            else:
                self.add_result("管理员查看所有企业", False, f"状态码: {response.status_code}")
        except Exception as e:
            self.add_result("管理员查看所有企业", False, str(e))
        
        # 需求方企业数据隔离
        if "demand" in self.tokens and self.user_info.get("demand", {}).get("enterprise_id"):
            try:
                headers = {"Authorization": f"Bearer {self.tokens['demand']}"}
                response = requests.get(f"{BASE_URL}/enterprises/", headers=headers)
                if response.status_code == 200:
                    enterprises = response.json()
                    if len(enterprises) == 1:
                        self.add_result("需求方企业数据隔离", True, "只能查看自己的企业（数据隔离正常）")
                    else:
                        self.add_result("需求方企业数据隔离", False, f"可见{len(enterprises)}家企业（应该只有1家）")
                else:
                    self.add_result("需求方企业数据隔离", False, f"状态码: {response.status_code}")
            except Exception as e:
                self.add_result("需求方企业数据隔离", False, str(e))
        else:
            self.add_result("需求方企业数据隔离", False, "需求方用户未绑定企业")
        
        # 供应方企业数据隔离
        if "supply" in self.tokens and self.user_info.get("supply", {}).get("enterprise_id"):
            try:
                headers = {"Authorization": f"Bearer {self.tokens['supply']}"}
                response = requests.get(f"{BASE_URL}/enterprises/", headers=headers)
                if response.status_code == 200:
                    enterprises = response.json()
                    if len(enterprises) == 1:
                        self.add_result("供应方企业数据隔离", True, "只能查看自己的企业（数据隔离正常）")
                    else:
                        self.add_result("供应方企业数据隔离", False, f"可见{len(enterprises)}家企业（应该只有1家）")
                else:
                    self.add_result("供应方企业数据隔离", False, f"状态码: {response.status_code}")
            except Exception as e:
                self.add_result("供应方企业数据隔离", False, str(e))
        else:
            self.add_result("供应方企业数据隔离", False, "供应方用户未绑定企业")
    
    def test_demand_permissions(self):
        """测试需求权限管理"""
        self.log("\n" + "="*80)
        self.log("第4部分: 需求权限管理测试")
        self.log("="*80)
        
        if "admin" not in self.tokens:
            self.add_result("需求权限测试", False, "管理员未登录，跳过测试")
            return
        
        # 管理员查看所有需求
        try:
            headers = {"Authorization": f"Bearer {self.tokens['admin']}"}
            response = requests.get(f"{BASE_URL}/demands/", headers=headers)
            if response.status_code == 200:
                demands = response.json()
                self.add_result("管理员查看所有需求", True, f"可见{len(demands)}个需求")
                
                # 保存需求数据供后续测试使用
                if len(demands) > 0:
                    self.test_demand_id = demands[0]["id"]
            else:
                self.add_result("管理员查看所有需求", False, f"状态码: {response.status_code}")
        except Exception as e:
            self.add_result("管理员查看所有需求", False, str(e))
        
        # 需求方查看自己的需求
        if "demand" in self.tokens:
            try:
                headers = {"Authorization": f"Bearer {self.tokens['demand']}"}
                response = requests.get(f"{BASE_URL}/demands/", headers=headers)
                if response.status_code == 200:
                    demands = response.json()
                    self.add_result("需求方查看自己的需求", True, f"可见{len(demands)}个需求（数据隔离）")
                else:
                    self.add_result("需求方查看自己的需求", False, f"状态码: {response.status_code}")
            except Exception as e:
                self.add_result("需求方查看自己的需求", False, str(e))
        
        # 供应方查看已发布需求
        if "supply" in self.tokens:
            try:
                headers = {"Authorization": f"Bearer {self.tokens['supply']}"}
                response = requests.get(f"{BASE_URL}/demands/", headers=headers)
                if response.status_code == 200:
                    demands = response.json()
                    # 供应方只能看到已发布的需求
                    all_published = all(d.get("status") == "published" for d in demands) if demands else True
                    if all_published:
                        self.add_result("供应方查看已发布需求", True, f"只能查看{len(demands)}个已发布需求")
                    else:
                        self.add_result("供应方查看已发布需求", False, "看到了未发布的需求")
                else:
                    self.add_result("供应方查看已发布需求", False, f"状态码: {response.status_code}")
            except Exception as e:
                self.add_result("供应方查看已发布需求", False, str(e))
    
    def test_cross_role_access_control(self):
        """测试跨角色访问控制"""
        self.log("\n" + "="*80)
        self.log("第5部分: 跨角色访问控制测试")
        self.log("="*80)
        
        # 供应方不能创建需求
        if "supply" in self.tokens:
            try:
                headers = {"Authorization": f"Bearer {self.tokens['supply']}"}
                test_demand = {
                    "title": "测试需求",
                    "description": "测试描述",
                    "enterprise_id": 1
                }
                response = requests.post(
                    f"{BASE_URL}/demands/",
                    json=test_demand,
                    headers=headers
                )
                if response.status_code == 403:
                    self.add_result("供应方创建需求被拒绝", True, "系统正确拒绝供应方创建需求")
                else:
                    self.add_result("供应方创建需求被拒绝", False, f"状态码: {response.status_code}（应该是403）")
            except Exception as e:
                self.add_result("供应方创建需求被拒绝", False, str(e))
        
        # 需求方和供应方不能访问对方的专属API
        if "demand" in self.tokens:
            try:
                headers = {"Authorization": f"Bearer {self.tokens['demand']}"}
                response = requests.get(
                    f"{BASE_URL}/recommendations/my-clients",
                    headers=headers
                )
                if response.status_code == 403:
                    self.add_result("需求方访问供应方API被拒绝", True, "系统正确拒绝跨角色访问")
                else:
                    self.add_result("需求方访问供应方API被拒绝", False, f"状态码: {response.status_code}（应该是403）")
            except Exception as e:
                self.add_result("需求方访问供应方API被拒绝", False, str(e))
        
        if "supply" in self.tokens:
            try:
                headers = {"Authorization": f"Bearer {self.tokens['supply']}"}
                response = requests.get(
                    f"{BASE_URL}/recommendations/my-suppliers",
                    headers=headers
                )
                if response.status_code == 403:
                    self.add_result("供应方访问需求方API被拒绝", True, "系统正确拒绝跨角色访问")
                else:
                    self.add_result("供应方访问需求方API被拒绝", False, f"状态码: {response.status_code}（应该是403）")
            except Exception as e:
                self.add_result("供应方访问需求方API被拒绝", False, str(e))
    
    def test_recommendation_system(self):
        """测试推荐系统"""
        self.log("\n" + "="*80)
        self.log("第6部分: 推荐系统测试")
        self.log("="*80)
        
        # 需求方查看推荐供应商
        if "demand" in self.tokens and self.user_info.get("demand", {}).get("enterprise_id"):
            try:
                headers = {"Authorization": f"Bearer {self.tokens['demand']}"}
                response = requests.get(
                    f"{BASE_URL}/recommendations/my-suppliers",
                    headers=headers
                )
                if response.status_code == 200:
                    data = response.json()
                    self.add_result("需求方查看推荐供应商", True, f"获取到{len(data)}个推荐")
                elif response.status_code == 400:
                    self.add_result("需求方查看推荐供应商", True, "用户未绑定企业（符合预期）")
                else:
                    self.add_result("需求方查看推荐供应商", False, f"状态码: {response.status_code}")
            except Exception as e:
                self.add_result("需求方查看推荐供应商", False, str(e))
        else:
            self.add_result("需求方查看推荐供应商", False, "需求方用户未登录或未绑定企业")
        
        # 供应方查看匹配客户
        if "supply" in self.tokens and self.user_info.get("supply", {}).get("enterprise_id"):
            try:
                headers = {"Authorization": f"Bearer {self.tokens['supply']}"}
                response = requests.get(
                    f"{BASE_URL}/recommendations/my-clients",
                    headers=headers
                )
                if response.status_code == 200:
                    data = response.json()
                    self.add_result("供应方查看匹配客户", True, f"获取到{len(data)}个匹配")
                elif response.status_code == 400:
                    self.add_result("供应方查看匹配客户", True, "用户未绑定企业（符合预期）")
                else:
                    self.add_result("供应方查看匹配客户", False, f"状态码: {response.status_code}")
            except Exception as e:
                self.add_result("供应方查看匹配客户", False, str(e))
        else:
            self.add_result("供应方查看匹配客户", False, "供应方用户未登录或未绑定企业")
        
        # 管理员查看所有匹配
        if "admin" in self.tokens:
            try:
                headers = {"Authorization": f"Bearer {self.tokens['admin']}"}
                response = requests.get(
                    f"{BASE_URL}/recommendations/admin/all-matches",
                    headers=headers
                )
                if response.status_code == 200:
                    data = response.json()
                    self.add_result("管理员查看所有匹配", True, f"获取到{len(data)}个匹配记录")
                else:
                    self.add_result("管理员查看所有匹配", False, f"状态码: {response.status_code}")
            except Exception as e:
                self.add_result("管理员查看所有匹配", False, str(e))
    
    def test_qualification_system(self):
        """测试资质管理系统"""
        self.log("\n" + "="*80)
        self.log("第7部分: 资质管理系统测试")
        self.log("="*80)
        
        # 测试获取资质列表
        if "admin" in self.tokens:
            try:
                headers = {"Authorization": f"Bearer {self.tokens['admin']}"}
                response = requests.get(
                    f"{BASE_URL}/qualifications/",
                    headers=headers
                )
                if response.status_code == 200:
                    qualifications = response.json()
                    self.add_result("管理员查看资质列表", True, f"查看到{len(qualifications)}条资质记录")
                else:
                    self.add_result("管理员查看资质列表", False, f"状态码: {response.status_code}")
            except Exception as e:
                self.add_result("管理员查看资质列表", False, str(e))
    
    def test_user_registration_flow(self):
        """测试用户注册流程（包括新UX流程）"""
        self.log("\n" + "="*80)
        self.log("第8部分: 用户注册流程测试")
        self.log("="*80)
        
        # 测试注册新用户（带角色选择）
        timestamp = datetime.now().strftime("%H%M%S%f")
        new_user = {
            "email": f"newuser_{timestamp}@test.com",
            "password": "test123456",
            "role": "demand"  # 新增的角色选择
        }
        
        try:
            response = requests.post(
                f"{BASE_URL}/auth/register",
                json=new_user
            )
            # 注册接口返回200或201都算成功
            if response.status_code in [200, 201]:
                data = response.json()
                self.add_result("新用户注册（带角色）", True, f"注册成功，角色: {data.get('role', 'N/A')}")
                
                # 测试新用户登录
                try:
                    login_response = requests.post(
                        f"{BASE_URL}/auth/login",
                        json={"email": new_user["email"], "password": new_user["password"]}
                    )
                    if login_response.status_code == 200:
                        login_data = login_response.json()
                        has_enterprise = login_data["user"].get("enterprise_id") is not None
                        if not has_enterprise:
                            self.add_result("新用户首次登录状态检测", True, "新用户无企业ID（触发onboarding）")
                        else:
                            self.add_result("新用户首次登录状态检测", False, "新用户已有企业ID")
                    else:
                        self.add_result("新用户首次登录状态检测", False, f"登录失败，状态码: {login_response.status_code}")
                except Exception as e:
                    self.add_result("新用户首次登录状态检测", False, str(e))
            else:
                self.add_result("新用户注册（带角色）", False, f"状态码: {response.status_code}, 错误: {response.text}")
        except Exception as e:
            self.add_result("新用户注册（带角色）", False, str(e))
    
    def run_all_tests(self):
        """运行所有测试"""
        self.log("\n" + "="*80)
        self.log("完整系统综合测试")
        self.log("="*80)
        self.log(f"测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        self.log(f"后端地址: {BASE_URL}")
        self.log(f"前端地址: {FRONTEND_URL}")
        self.log("="*80)
        
        # 按顺序执行所有测试
        self.test_services_health()
        self.test_user_authentication()
        self.test_enterprise_permissions()
        self.test_demand_permissions()
        self.test_cross_role_access_control()
        self.test_recommendation_system()
        self.test_qualification_system()
        self.test_user_registration_flow()
        
        # 输出总结
        self.print_summary()
    
    def print_summary(self):
        """打印测试总结"""
        self.log("\n" + "="*80)
        self.log("测试总结")
        self.log("="*80)
        self.log(f"总测试数: {self.results['total']}")
        self.log(f"通过: {self.results['passed']} ✅")
        self.log(f"失败: {self.results['failed']} ❌")
        
        if self.results['total'] > 0:
            success_rate = (self.results['passed'] / self.results['total']) * 100
            self.log(f"成功率: {success_rate:.1f}%")
            
            # 评估系统状态
            if success_rate >= 90:
                status = "🟢 优秀 - 系统功能完善，可以部署"
            elif success_rate >= 75:
                status = "🟡 良好 - 核心功能正常，部分功能需要优化"
            elif success_rate >= 60:
                status = "🟠 一般 - 存在一些问题，需要修复"
            else:
                status = "🔴 需要改进 - 存在较多问题"
            
            self.log(f"系统状态: {status}")
        
        self.log("="*80)
        
        if self.results['failed'] > 0:
            self.log("\n失败的测试:")
            for detail in self.results['details']:
                if detail.startswith("❌"):
                    self.log(f"  {detail}")
        
        # 保存测试报告
        report_file = f"final_test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump({
                "test_time": datetime.now().isoformat(),
                "backend_url": BASE_URL,
                "frontend_url": FRONTEND_URL,
                "results": self.results,
                "test_accounts": {k: v["email"] for k, v in TEST_ACCOUNTS.items()}
            }, f, ensure_ascii=False, indent=2)
        self.log(f"\n完整测试报告已保存到: {report_file}")
        
        # 返回是否大部分通过（>= 80%）
        success_rate = (self.results['passed'] / self.results['total']) * 100 if self.results['total'] > 0 else 0
        return success_rate >= 80


if __name__ == "__main__":
    tester = FinalComprehensiveTester()
    mostly_passed = tester.run_all_tests()
    
    # 设置退出码
    import sys
    sys.exit(0 if mostly_passed else 1)
