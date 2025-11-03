"""
数据库角色迁移脚本
将现有用户角色更新为新的RBAC系统
"""
from app.core.database import SessionLocal, engine
from app.models.user import User, UserRole
from app.models.enterprise import Enterprise

def migrate_user_roles():
    """迁移用户角色"""
    db = SessionLocal()
    
    try:
        # 获取所有用户
        users = db.query(User).all()
        
        print(f"开始迁移 {len(users)} 个用户的角色...")
        
        for user in users:
            # 根据邮箱判断是否为管理员
            if user.email in ['admin@platform.com', 'admin@example.com']:
                user.role = UserRole.ADMIN
                print(f"✅ {user.email} -> ADMIN")
                
            # 如果用户有企业ID，根据企业类型设置角色
            elif user.enterprise_id:
                enterprise = db.query(Enterprise).filter(
                    Enterprise.id == user.enterprise_id
                ).first()
                
                if enterprise:
                    if enterprise.enterprise_type == 'SUPPLY':
                        user.role = UserRole.SUPPLY
                        print(f"✅ {user.email} -> SUPPLY (企业: {enterprise.name})")
                    elif enterprise.enterprise_type == 'DEMAND':
                        user.role = UserRole.DEMAND
                        print(f"✅ {user.email} -> DEMAND (企业: {enterprise.name})")
                    else:
                        # 默认为需求方
                        user.role = UserRole.DEMAND
                        print(f"⚠️  {user.email} -> DEMAND (默认)")
                else:
                    # 没找到企业，默认为需求方
                    user.role = UserRole.DEMAND
                    print(f"⚠️  {user.email} -> DEMAND (无企业)")
            else:
                # 没有企业ID，默认为需求方
                user.role = UserRole.DEMAND
                print(f"⚠️  {user.email} -> DEMAND (无企业)")
        
        # 提交更改
        db.commit()
        print(f"\n✅ 成功迁移 {len(users)} 个用户的角色！")
        
        # 显示统计
        admin_count = db.query(User).filter(User.role == UserRole.ADMIN).count()
        demand_count = db.query(User).filter(User.role == UserRole.DEMAND).count()
        supply_count = db.query(User).filter(User.role == UserRole.SUPPLY).count()
        
        print(f"\n📊 角色统计:")
        print(f"  - 管理员: {admin_count}")
        print(f"  - 需求方: {demand_count}")
        print(f"  - 供应方: {supply_count}")
        
    except Exception as e:
        print(f"❌ 迁移失败: {str(e)}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    print("=" * 60)
    print("用户角色迁移脚本")
    print("=" * 60)
    migrate_user_roles()
    print("=" * 60)
