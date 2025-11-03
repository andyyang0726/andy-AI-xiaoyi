"""
直接通过SQL更新用户角色
"""
from app.core.database import SessionLocal, engine
from sqlalchemy import text

def migrate_roles_via_sql():
    """通过原始SQL更新角色"""
    db = SessionLocal()
    
    try:
        # 首先查看当前的角色分布
        result = db.execute(text("SELECT role, COUNT(*) as count FROM users GROUP BY role")).fetchall()
        print("当前角色分布:")
        for row in result:
            print(f"  {row[0]}: {row[1]}人")
        
        print("\n开始迁移...")
        
        # 将 ENTERPRISE_ADMIN 改为 DEMAND（默认）
        result = db.execute(text("""
            UPDATE users 
            SET role = 'demand' 
            WHERE role = 'enterprise_admin'
        """))
        print(f"✅ 更新了 {result.rowcount} 个 enterprise_admin -> demand")
        
        # 将 ENTERPRISE_USER 改为 DEMAND
        result = db.execute(text("""
            UPDATE users 
            SET role = 'demand' 
            WHERE role = 'enterprise_user'
        """))
        print(f"✅ 更新了 {result.rowcount} 个 enterprise_user -> demand")
        
        # 将 EXPERT 改为 SUPPLY
        result = db.execute(text("""
            UPDATE users 
            SET role = 'supply' 
            WHERE role = 'expert'
        """))
        print(f"✅ 更新了 {result.rowcount} 个 expert -> supply")
        
        # 根据企业类型更新角色
        result = db.execute(text("""
            UPDATE users 
            SET role = 'supply' 
            WHERE enterprise_id IN (
                SELECT id FROM enterprises WHERE enterprise_type = 'SUPPLY'
            ) AND role != 'admin'
        """))
        print(f"✅ 根据企业类型更新了 {result.rowcount} 个用户为 supply")
        
        # 提交更改
        db.commit()
        
        # 显示更新后的角色分布
        result = db.execute(text("SELECT role, COUNT(*) as count FROM users GROUP BY role")).fetchall()
        print("\n更新后的角色分布:")
        for row in result:
            print(f"  {row[0]}: {row[1]}人")
        
        print("\n✅ 角色迁移成功！")
        
    except Exception as e:
        print(f"❌ 迁移失败: {str(e)}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    print("=" * 60)
    print("SQL角色迁移脚本")
    print("=" * 60)
    migrate_roles_via_sql()
    print("=" * 60)
