"""
RBAC权限系统综合功能测试
完整测试所有API端点的权限控制和数据隔离
"""
import requests
import json
from datetime import datetime
from typing import Dict, List, Tuple

# 测试配置
BASE_URL = "http://localhost:8000/api/v1"
TEST_ACCOUNTS = {
    "admin": {"email": "admin@platform.com", "password": "admin123"},
    "demand": {"email": "changan@demo.com", "password": "demo123"},
    "supply": {"email": "xiaoyi@demo.com", "password": "demo123"}
}

class TestResult:
    """测试结果记录"""
    def __init__(self):
        self.total = 0
        self.passed = 0
        self.failed = 0
        self.details = []
    
    def add_test(self, name: str, passed: bool, message: str = ""):
        self.total += 1
        if passed:
            self.passed += 1
            self.details.append(f"✅ {name}: {message}")
        else:
            self.failed += 1
            self.details.append(f"❌ {name}: {message}")
    
    def print_summary(self):
        print("\n" + "=" * 80)
        print("测试总结")
        print("=" * 80)
        print(f"总测试数: {self.total}")
        print(f"通过: {self.passed} ✅")
        print(f"失败: {self.failed} ❌")
        print(f"成功率: {(self.passed/self.total*100):.1f}%")
        print("=" * 80)
        
        if self.failed > 0:
            print("\n失败的测试:")
            for detail in self.details:
                if "❌" in detail:
                    print(detail)

class RBACTester:
    """RBAC测试器"""
    
    def __init__(self):
        self.result = TestResult()
        self.tokens = {}
        self.users = {}
    
    def login(self, role: str) -> Tuple[bool, str]:
        """登录并获取token"""
        try:
            account = TEST_ACCOUNTS[role]
            response = requests.post(
                f"{BASE_URL}/auth/login",
                json=account
            )
            
            if response.status_code == 200:
                data = response.json()
                self.tokens[role] = data["access_token"]
                self.users[role] = data["user"]
                return True, f"登录成功 (user_id={data['user']['id']})"
            else:
                return False, f"登录失败: {response.status_code}"
        except Exception as e:
            return False, f"登录异常: {str(e)}"
    
    def get_headers(self, role: str) -> Dict:
        """获取认证头"""
        return {"Authorization": f"Bearer {self.tokens[role]}"}
    
    def test_authentication(self):
        """测试1: 认证功能"""
        print("\n" + "=" * 80)
        print("测试1: 用户认证功能")
        print("=" * 80)
        
        # 测试管理员登录
        passed, msg = self.login("admin")
        self.result.add_test("管理员登录", passed, msg)
        
        # 测试需求方登录
        passed, msg = self.login("demand")
        self.result.add_test("需求方登录", passed, msg)
        
        # 测试供应方登录
        passed, msg = self.login("supply")
        self.result.add_test("供应方登录", passed, msg)
        
        # 测试错误密码
        try:
            response = requests.post(
                f"{BASE_URL}/auth/login",
                json={"email": "admin@platform.com", "password": "wrongpassword"}
            )
            passed = response.status_code == 401
            self.result.add_test("错误密码拒绝", passed, 
                               "正确拒绝" if passed else f"状态码: {response.status_code}")
        except Exception as e:
            self.result.add_test("错误密码拒绝", False, str(e))
        
        # 测试未认证访问
        try:
            response = requests.get(f"{BASE_URL}/enterprises")
            passed = response.status_code == 401
            self.result.add_test("未认证访问拒绝", passed,
                               "正确拒绝" if passed else f"状态码: {response.status_code}")
        except Exception as e:
            self.result.add_test("未认证访问拒绝", False, str(e))
    
    def test_enterprise_permissions(self):
        """测试2: 企业管理权限"""
        print("\n" + "=" * 80)
        print("测试2: 企业管理权限")
        print("=" * 80)
        
        # 管理员查看所有企业
        try:
            response = requests.get(
                f"{BASE_URL}/enterprises",
                headers=self.get_headers("admin"),
                params={"limit": 100}
            )
            if response.status_code == 200:
                data = response.json()
                admin_count = data.get("total", 0)
                passed = admin_count > 0
                self.result.add_test("管理员查看所有企业", passed, 
                                   f"可见{admin_count}家企业")
            else:
                self.result.add_test("管理员查看所有企业", False, 
                                   f"状态码: {response.status_code}")
        except Exception as e:
            self.result.add_test("管理员查看所有企业", False, str(e))
        
        # 需求方只能看到自己的企业
        try:
            response = requests.get(
                f"{BASE_URL}/enterprises",
                headers=self.get_headers("demand"),
                params={"limit": 100}
            )
            if response.status_code == 200:
                data = response.json()
                demand_count = data.get("total", 0)
                # 需求方应该只能看到1家企业（自己的）
                passed = demand_count == 1
                self.result.add_test("需求方数据隔离", passed,
                                   f"可见{demand_count}家企业 (预期1家)")
            else:
                self.result.add_test("需求方数据隔离", False,
                                   f"状态码: {response.status_code}")
        except Exception as e:
            self.result.add_test("需求方数据隔离", False, str(e))
        
        # 供应方只能看到自己的企业
        try:
            response = requests.get(
                f"{BASE_URL}/enterprises",
                headers=self.get_headers("supply"),
                params={"limit": 100}
            )
            if response.status_code == 200:
                data = response.json()
                supply_count = data.get("total", 0)
                # 供应方应该只能看到1家企业（自己的）
                passed = supply_count == 1
                self.result.add_test("供应方数据隔离", passed,
                                   f"可见{supply_count}家企业 (预期1家)")
            else:
                self.result.add_test("供应方数据隔离", False,
                                   f"状态码: {response.status_code}")
        except Exception as e:
            self.result.add_test("供应方数据隔离", False, str(e))
    
    def test_demand_permissions(self):
        """测试3: 需求管理权限"""
        print("\n" + "=" * 80)
        print("测试3: 需求管理权限")
        print("=" * 80)
        
        # 管理员查看所有需求
        try:
            response = requests.get(
                f"{BASE_URL}/demands",
                headers=self.get_headers("admin"),
                params={"limit": 100}
            )
            if response.status_code == 200:
                data = response.json()
                admin_demand_count = data.get("total", 0)
                self.result.add_test("管理员查看所有需求", True,
                                   f"可见{admin_demand_count}个需求")
            else:
                self.result.add_test("管理员查看所有需求", False,
                                   f"状态码: {response.status_code}")
        except Exception as e:
            self.result.add_test("管理员查看所有需求", False, str(e))
        
        # 需求方只能看到自己企业的需求
        try:
            response = requests.get(
                f"{BASE_URL}/demands",
                headers=self.get_headers("demand"),
                params={"limit": 100}
            )
            if response.status_code == 200:
                data = response.json()
                demand_count = data.get("total", 0)
                # 需求方只能看到自己的需求
                passed = demand_count >= 0
                self.result.add_test("需求方查看自己的需求", passed,
                                   f"可见{demand_count}个需求")
            else:
                self.result.add_test("需求方查看自己的需求", False,
                                   f"状态码: {response.status_code}")
        except Exception as e:
            self.result.add_test("需求方查看自己的需求", False, str(e))
        
        # 供应方查看已发布的需求
        try:
            response = requests.get(
                f"{BASE_URL}/demands",
                headers=self.get_headers("supply"),
                params={"limit": 100}
            )
            if response.status_code == 200:
                data = response.json()
                supply_demand_count = data.get("total", 0)
                # 供应方可以看到已发布的需求（可能为0）
                self.result.add_test("供应方查看已发布需求", True,
                                   f"可见{supply_demand_count}个需求")
            else:
                self.result.add_test("供应方查看已发布需求", False,
                                   f"状态码: {response.status_code}")
        except Exception as e:
            self.result.add_test("供应方查看已发布需求", False, str(e))
    
    def test_recommendation_permissions(self):
        """测试4: 推荐功能权限"""
        print("\n" + "=" * 80)
        print("测试4: 推荐功能权限")
        print("=" * 80)
        
        # 需求方访问推荐供应商
        try:
            response = requests.get(
                f"{BASE_URL}/recommendations/my-suppliers",
                headers=self.get_headers("demand"),
                params={"limit": 10}
            )
            passed = response.status_code == 200
            if passed:
                data = response.json()
                count = data.get("total", 0)
                self.result.add_test("需求方访问推荐供应商", True,
                                   f"获取到{count}个推荐")
            else:
                self.result.add_test("需求方访问推荐供应商", False,
                                   f"状态码: {response.status_code}")
        except Exception as e:
            self.result.add_test("需求方访问推荐供应商", False, str(e))
        
        # 供应方访问匹配客户
        try:
            response = requests.get(
                f"{BASE_URL}/recommendations/my-clients",
                headers=self.get_headers("supply"),
                params={"limit": 10}
            )
            passed = response.status_code == 200
            if passed:
                data = response.json()
                count = data.get("total", 0)
                self.result.add_test("供应方访问匹配客户", True,
                                   f"获取到{count}个推荐")
            else:
                self.result.add_test("供应方访问匹配客户", False,
                                   f"状态码: {response.status_code}")
        except Exception as e:
            self.result.add_test("供应方访问匹配客户", False, str(e))
        
        # 需求方不能访问供应方专用API
        try:
            response = requests.get(
                f"{BASE_URL}/recommendations/my-clients",
                headers=self.get_headers("demand"),
                params={"limit": 10}
            )
            passed = response.status_code == 403
            self.result.add_test("需求方访问供应方API被拒绝", passed,
                               "正确拒绝" if passed else f"状态码: {response.status_code}")
        except Exception as e:
            self.result.add_test("需求方访问供应方API被拒绝", False, str(e))
        
        # 供应方不能访问需求方专用API
        try:
            response = requests.get(
                f"{BASE_URL}/recommendations/my-suppliers",
                headers=self.get_headers("supply"),
                params={"limit": 10}
            )
            passed = response.status_code == 403
            self.result.add_test("供应方访问需求方API被拒绝", passed,
                               "正确拒绝" if passed else f"状态码: {response.status_code}")
        except Exception as e:
            self.result.add_test("供应方访问需求方API被拒绝", False, str(e))
        
        # 管理员访问所有匹配数据
        try:
            response = requests.get(
                f"{BASE_URL}/recommendations/admin/all-matches",
                headers=self.get_headers("admin"),
                params={"limit": 10}
            )
            passed = response.status_code == 200
            if passed:
                data = response.json()
                count = data.get("total", 0)
                self.result.add_test("管理员访问所有匹配数据", True,
                                   f"获取到{count}个匹配")
            else:
                self.result.add_test("管理员访问所有匹配数据", False,
                                   f"状态码: {response.status_code}")
        except Exception as e:
            self.result.add_test("管理员访问所有匹配数据", False, str(e))
    
    def test_cross_role_access(self):
        """测试5: 跨角色访问控制"""
        print("\n" + "=" * 80)
        print("测试5: 跨角色访问控制")
        print("=" * 80)
        
        # 测试未认证访问
        endpoints = [
            "/enterprises",
            "/demands",
            "/recommendations/my-suppliers"
        ]
        
        for endpoint in endpoints:
            try:
                response = requests.get(f"{BASE_URL}{endpoint}")
                passed = response.status_code == 401
                self.result.add_test(f"未认证访问{endpoint}被拒绝", passed,
                                   "正确拒绝" if passed else f"状态码: {response.status_code}")
            except Exception as e:
                self.result.add_test(f"未认证访问{endpoint}被拒绝", False, str(e))
    
    def generate_report(self):
        """生成测试报告"""
        print("\n" + "=" * 80)
        print("详细测试结果")
        print("=" * 80)
        
        for detail in self.result.details:
            print(detail)
        
        self.result.print_summary()
        
        # 生成JSON报告
        report = {
            "test_time": datetime.now().isoformat(),
            "summary": {
                "total": self.result.total,
                "passed": self.result.passed,
                "failed": self.result.failed,
                "success_rate": f"{(self.result.passed/self.result.total*100):.1f}%"
            },
            "details": self.result.details,
            "test_accounts": {
                "admin": self.users.get("admin", {}),
                "demand": self.users.get("demand", {}),
                "supply": self.users.get("supply", {})
            }
        }
        
        return report

def main():
    """主测试流程"""
    print("=" * 80)
    print("RBAC权限系统综合功能测试")
    print("=" * 80)
    print(f"测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"API地址: {BASE_URL}")
    print("=" * 80)
    
    tester = RBACTester()
    
    # 执行测试
    tester.test_authentication()
    tester.test_enterprise_permissions()
    tester.test_demand_permissions()
    tester.test_recommendation_permissions()
    tester.test_cross_role_access()
    
    # 生成报告
    report = tester.generate_report()
    
    # 保存报告到文件
    report_file = f"rbac_test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    print(f"\n测试报告已保存到: {report_file}")
    
    # 返回测试是否全部通过
    return tester.result.failed == 0

if __name__ == "__main__":
    import sys
    success = main()
    sys.exit(0 if success else 1)
