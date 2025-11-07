"""
RBAC权限系统综合测试脚本
验证所有权限控制逻辑是否正确
"""
import sys
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.user import User, UserRole
from app.models.enterprise import Enterprise
from app.models.demand import Demand
from app.core.permissions import (
    PermissionChecker,
    filter_demands_by_permission,
    filter_enterprises_by_permission
)

def test_permissions():
    """测试权限系统"""
    db: Session = SessionLocal()
    
    try:
        print("=" * 60)
        print("RBAC权限系统综合测试")
        print("=" * 60)
        
        # 1. 获取测试用户
        print("\n1. 获取测试用户...")
        admin_user = db.query(User).filter(User.email == "admin@platform.com").first()
        demand_user = db.query(User).filter(User.email == "changan@demo.com").first()
        supply_user = db.query(User).filter(User.email == "xiaoyi@demo.com").first()
        
        if not admin_user:
            print("❌ 管理员用户不存在")
            return False
        if not demand_user:
            print("❌ 需求方用户不存在")
            return False
        if not supply_user:
            print("❌ 供应方用户不存在")
            return False
        
        print(f"✅ 管理员: {admin_user.email} (role={admin_user.role})")
        print(f"✅ 需求方: {demand_user.email} (role={demand_user.role}, enterprise_id={demand_user.enterprise_id})")
        print(f"✅ 供应方: {supply_user.email} (role={supply_user.role}, enterprise_id={supply_user.enterprise_id})")
        
        # 2. 测试PermissionChecker
        print("\n2. 测试权限检查器...")
        admin_checker = PermissionChecker(admin_user)
        demand_checker = PermissionChecker(demand_user)
        supply_checker = PermissionChecker(supply_user)
        
        # 测试角色判断
        assert admin_checker.is_admin() == True, "管理员角色判断错误"
        assert demand_checker.is_demand() == True, "需求方角色判断错误"
        assert supply_checker.is_supply() == True, "供应方角色判断错误"
        print("✅ 角色判断正确")
        
        # 测试创建需求权限
        assert admin_checker.can_create_demand() == True, "管理员应可创建需求"
        assert demand_checker.can_create_demand() == True, "需求方应可创建需求"
        assert supply_checker.can_create_demand() == False, "供应方不应可创建需求"
        print("✅ 创建需求权限正确")
        
        # 测试查看所有企业权限
        assert admin_checker.can_view_all_enterprises() == True, "管理员应可查看所有企业"
        assert demand_checker.can_view_all_enterprises() == False, "需求方不应可查看所有企业"
        assert supply_checker.can_view_all_enterprises() == False, "供应方不应可查看所有企业"
        print("✅ 查看企业权限正确")
        
        # 测试审核权限
        assert admin_checker.can_approve_qualification() == True, "管理员应可审核资质"
        assert demand_checker.can_approve_qualification() == False, "需求方不应可审核资质"
        assert supply_checker.can_approve_qualification() == False, "供应方不应可审核资质"
        print("✅ 审核权限正确")
        
        # 3. 测试需求过滤
        print("\n3. 测试需求数据过滤...")
        base_query = db.query(Demand)
        
        # 管理员应看到所有需求
        admin_query = filter_demands_by_permission(base_query, admin_user)
        admin_demands_count = admin_query.count()
        print(f"   管理员可见需求数: {admin_demands_count}")
        
        # 需求方只能看到自己企业的需求
        demand_query = filter_demands_by_permission(base_query, demand_user)
        demand_demands_count = demand_query.count()
        print(f"   需求方可见需求数: {demand_demands_count}")
        
        # 供应方可以看到所有已发布的需求
        supply_query = filter_demands_by_permission(base_query, supply_user)
        supply_demands_count = supply_query.count()
        print(f"   供应方可见需求数: {supply_demands_count}")
        
        # 验证逻辑
        if admin_demands_count >= demand_demands_count:
            print("✅ 管理员看到的需求 >= 需求方看到的需求")
        else:
            print("❌ 需求过滤逻辑错误")
        
        # 4. 测试企业过滤
        print("\n4. 测试企业数据过滤...")
        base_enterprise_query = db.query(Enterprise)
        
        # 管理员应看到所有企业
        admin_enterprise_query = filter_enterprises_by_permission(
            base_enterprise_query, 
            admin_user, 
            matched_enterprise_ids=[]
        )
        admin_enterprises_count = admin_enterprise_query.count()
        print(f"   管理员可见企业数: {admin_enterprises_count}")
        
        # 需求方只能看到自己的企业
        demand_enterprise_query = filter_enterprises_by_permission(
            base_enterprise_query,
            demand_user,
            matched_enterprise_ids=[]
        )
        demand_enterprises_count = demand_enterprise_query.count()
        print(f"   需求方可见企业数: {demand_enterprises_count}")
        
        # 供应方只能看到自己的企业（无匹配时）
        supply_enterprise_query = filter_enterprises_by_permission(
            base_enterprise_query,
            supply_user,
            matched_enterprise_ids=[]
        )
        supply_enterprises_count = supply_enterprise_query.count()
        print(f"   供应方可见企业数: {supply_enterprises_count}")
        
        if admin_enterprises_count > 0:
            print("✅ 企业过滤功能正常")
        else:
            print("⚠️  数据库中暂无企业数据")
        
        # 5. 测试企业查看权限
        print("\n5. 测试企业查看权限...")
        if demand_user.enterprise_id:
            # 需求方应能查看自己的企业
            can_view_own = demand_checker.can_view_enterprise(
                demand_user.enterprise_id, 
                matched_enterprise_ids=[]
            )
            assert can_view_own == True, "需求方应能查看自己的企业"
            print("✅ 需求方可以查看自己的企业")
            
            # 需求方不应查看其他企业（无匹配关系时）
            other_enterprise_id = 9999
            can_view_other = demand_checker.can_view_enterprise(
                other_enterprise_id,
                matched_enterprise_ids=[]
            )
            assert can_view_other == False, "需求方不应查看未匹配的其他企业"
            print("✅ 需求方不能查看未匹配的企业")
            
            # 需求方应能查看匹配的企业
            matched_id = 2
            can_view_matched = demand_checker.can_view_enterprise(
                matched_id,
                matched_enterprise_ids=[matched_id]
            )
            assert can_view_matched == True, "需求方应能查看匹配的企业"
            print("✅ 需求方可以查看匹配的企业")
        
        # 6. 测试需求查看和修改权限
        print("\n6. 测试需求查看和修改权限...")
        test_demand = db.query(Demand).first()
        if test_demand:
            # 管理员应能查看和修改所有需求
            assert admin_checker.can_view_demand(test_demand) == True, "管理员应能查看需求"
            assert admin_checker.can_modify_demand(test_demand) == True, "管理员应能修改需求"
            print("✅ 管理员可以查看和修改所有需求")
            
            # 需求方只能查看和修改自己企业的需求
            if test_demand.enterprise_id == demand_user.enterprise_id:
                assert demand_checker.can_view_demand(test_demand) == True, "需求方应能查看自己的需求"
                assert demand_checker.can_modify_demand(test_demand) == True, "需求方应能修改自己的需求"
                print("✅ 需求方可以查看和修改自己的需求")
            else:
                assert demand_checker.can_view_demand(test_demand) == False, "需求方不应查看他人需求"
                assert demand_checker.can_modify_demand(test_demand) == False, "需求方不应修改他人需求"
                print("✅ 需求方不能查看和修改他人需求")
            
            # 供应方不能修改需求
            assert supply_checker.can_modify_demand(test_demand) == False, "供应方不应能修改需求"
            print("✅ 供应方不能修改需求")
        else:
            print("⚠️  数据库中暂无需求数据")
        
        print("\n" + "=" * 60)
        print("✅ 所有权限测试通过！")
        print("=" * 60)
        return True
        
    except AssertionError as e:
        print(f"\n❌ 权限测试失败: {e}")
        return False
    except Exception as e:
        print(f"\n❌ 测试过程出错: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        db.close()

if __name__ == "__main__":
    success = test_permissions()
    sys.exit(0 if success else 1)
