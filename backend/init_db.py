"""
数据库初始化脚本 - 创建示例数据
"""
from app.core.database import SessionLocal, engine, Base
from app.core.security import get_password_hash
from app.models import Enterprise, User, Demand
from app.models.enterprise import EnterpriseType, EnterpriseStatus
from app.models.user import UserRole
from app.models.demand import DemandStatus, ConfidentialityLevel
from datetime import datetime, timedelta
import random
import string


def generate_eid() -> str:
    """生成企业唯一识别码"""
    timestamp = str(int(random.random() * 10000))
    random_str = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    return f"EID-{timestamp}-{random_str}"


def init_database():
    """初始化数据库并插入示例数据"""
    print("创建数据库表...")
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    try:
        # 检查是否已有数据
        if db.query(Enterprise).count() > 0:
            print("数据库已有数据，跳过初始化")
            return
        
        print("插入示例企业数据...")
        
        # 创建需求方企业
        enterprises_demand = [
            Enterprise(
                eid=generate_eid(),
                name="重庆长安汽车股份有限公司",
                credit_code="915000002032881838",
                legal_person="朱华荣",
                enterprise_type=EnterpriseType.DEMAND,
                industry_tags=["制造业", "汽车"],
                size="大型",
                contact_person="张经理",
                contact_phone="023-12345678",
                contact_email="zhang@changan.com",
                address="重庆市江北区建新东路260号",
                business_scope="汽车制造、研发、销售",
                status=EnterpriseStatus.VERIFIED,
                certification_level="认证企业",
                credit_score=95.0
            ),
            Enterprise(
                eid=generate_eid(),
                name="重庆市政务服务和公共资源交易中心",
                credit_code="121500000588965523",
                legal_person="李主任",
                enterprise_type=EnterpriseType.DEMAND,
                industry_tags=["政务", "公共服务"],
                size="大型",
                contact_person="王处长",
                contact_phone="023-87654321",
                contact_email="wang@cqzwfw.gov.cn",
                address="重庆市渝北区龙山大道403号",
                business_scope="政务服务、公共资源交易",
                status=EnterpriseStatus.VERIFIED,
                certification_level="认证企业",
                credit_score=98.0
            ),
            Enterprise(
                eid=generate_eid(),
                name="重庆百货大楼股份有限公司",
                credit_code="915000002028800012",
                legal_person="何伟",
                enterprise_type=EnterpriseType.DEMAND,
                industry_tags=["零售", "商业"],
                size="中型",
                contact_person="刘经理",
                contact_phone="023-11223344",
                contact_email="liu@cqbh.com",
                address="重庆市渝中区民权路2号",
                business_scope="零售、批发",
                status=EnterpriseStatus.VERIFIED,
                certification_level="优选企业",
                credit_score=92.0
            )
        ]
        
        # 创建供应方企业
        enterprises_supply = [
            Enterprise(
                eid=generate_eid(),
                name="重庆小易智联科技有限公司",
                credit_code="91500000MA5YQ2XX6H",
                legal_person="陈总",
                enterprise_type=EnterpriseType.SUPPLY,
                industry_tags=["人工智能", "软件开发"],
                size="小型",
                contact_person="陈总",
                contact_phone="023-88990011",
                contact_email="chen@xiaoyi.ai",
                address="重庆市渝北区仙桃数据谷",
                business_scope="AI技术服务、智能系统开发",
                ai_capabilities=["计算机视觉", "自然语言处理", "端侧部署", "智脑OS"],
                status=EnterpriseStatus.VERIFIED,
                certification_level="优选企业",
                credit_score=96.0
            ),
            Enterprise(
                eid=generate_eid(),
                name="重庆紫光华智数字科技有限公司",
                credit_code="91500000MA60ABCD12",
                legal_person="刘总",
                enterprise_type=EnterpriseType.SUPPLY,
                industry_tags=["人工智能", "智慧城市"],
                size="中型",
                contact_person="刘经理",
                contact_phone="023-66778899",
                contact_email="liu@unigroup.com",
                address="重庆市南岸区南坪西路2号",
                business_scope="视频智能分析、智慧城市解决方案",
                ai_capabilities=["计算机视觉", "目标检测", "智能监控"],
                status=EnterpriseStatus.VERIFIED,
                certification_level="认证企业",
                credit_score=93.0
            ),
            Enterprise(
                eid=generate_eid(),
                name="重庆中科云从科技有限公司",
                credit_code="91500000MA60EFGH34",
                legal_person="周总",
                enterprise_type=EnterpriseType.SUPPLY,
                industry_tags=["人工智能", "人脸识别"],
                size="中型",
                contact_person="周工",
                contact_phone="023-55443322",
                contact_email="zhou@cloudwalk.com",
                address="重庆市两江新区黄山大道中段",
                business_scope="人脸识别、生物识别技术",
                ai_capabilities=["人脸识别", "图像识别", "生物识别"],
                status=EnterpriseStatus.VERIFIED,
                certification_level="优选企业",
                credit_score=94.0
            ),
            Enterprise(
                eid=generate_eid(),
                name="重庆特斯联智慧科技股份有限公司",
                credit_code="91500000MA60IJKL56",
                legal_person="艾总",
                enterprise_type=EnterpriseType.BOTH,
                industry_tags=["人工智能", "物联网"],
                size="中型",
                contact_person="艾经理",
                contact_phone="023-44556677",
                contact_email="ai@terminus.io",
                address="重庆市渝中区大坪正街19号",
                business_scope="智慧社区、智慧园区解决方案",
                ai_capabilities=["物联网", "边缘计算", "智能安防"],
                status=EnterpriseStatus.VERIFIED,
                certification_level="认证企业",
                credit_score=91.0
            )
        ]
        
        all_enterprises = enterprises_demand + enterprises_supply
        for ent in all_enterprises:
            db.add(ent)
        
        db.commit()
        print(f"已创建 {len(all_enterprises)} 个企业")
        
        # 创建用户
        print("插入示例用户数据...")
        users = [
            User(
                email="admin@platform.com",
                phone="13800000000",
                full_name="系统管理员",
                hashed_password=get_password_hash("admin123"),
                role=UserRole.ADMIN,
                is_active=True,
                is_superuser=True
            ),
            User(
                email="changan@demo.com",
                phone="13800000001",
                full_name="长安汽车联系人",
                hashed_password=get_password_hash("demo123"),
                role=UserRole.DEMAND,
                enterprise_id=1,
                is_active=True
            ),
            User(
                email="xiaoyi@demo.com",
                phone="13800000002",
                full_name="小易智联联系人",
                hashed_password=get_password_hash("demo123"),
                role=UserRole.SUPPLY,
                enterprise_id=4,
                is_active=True
            )
        ]
        
        for user in users:
            db.add(user)
        
        db.commit()
        print(f"已创建 {len(users)} 个用户")
        
        # 创建示例需求
        print("插入示例需求数据...")
        demands = [
            Demand(
                enterprise_id=1,  # 长安汽车
                title="智能质检系统开发需求",
                description="""
我们是一家大型汽车制造企业，目前在生产线上存在大量的人工质检环节，效率低且容易出现漏检。
希望通过计算机视觉技术实现自动化质检，主要针对焊接点、涂装表面、零部件装配等环节。
我们有大量的历史图像数据，包括合格品和不合格品的照片，约20000张已标注图像。
                """.strip(),
                industry_tags=["制造业", "汽车"],
                scenario_tags=["图像识别", "目标检测", "质量检测"],
                kpis=[
                    {"name": "检测准确率", "target": "≥95%", "metric": "accuracy"},
                    {"name": "漏检率", "target": "≤2%", "metric": "miss_rate"},
                    {"name": "检测速度", "target": "≤1秒/张", "metric": "speed"}
                ],
                budget_min=500000,
                budget_max=1000000,
                timeline_start=datetime.now(),
                timeline_end=datetime.now() + timedelta(days=180),
                data_summary={
                    "types": ["image"],
                    "counts": {"image": 20000},
                    "labeled_ratio": 0.85,
                    "size_bytes": 5000000000,
                    "health_score": 88
                },
                confidentiality=ConfidentialityLevel.INTERNAL,
                status=DemandStatus.SUBMITTED,
                priority=9
            ),
            Demand(
                enterprise_id=2,  # 政务中心
                title="政务服务智能问答系统",
                description="""
重庆市政务服务中心每天接待大量市民咨询，常见问题重复率高，工作人员压力大。
希望开发一个智能问答系统，能够自动回答常见政务问题，包括办事流程、所需材料、办理时限等。
我们整理了约5000条高频问答对，以及大量的政策文件和办事指南文档。
                """.strip(),
                industry_tags=["政务", "公共服务"],
                scenario_tags=["自然语言处理", "问答系统", "知识图谱"],
                kpis=[
                    {"name": "问答准确率", "target": "≥90%", "metric": "accuracy"},
                    {"name": "响应时间", "target": "≤2秒", "metric": "response_time"},
                    {"name": "覆盖率", "target": "≥80%", "metric": "coverage"}
                ],
                budget_min=300000,
                budget_max=600000,
                timeline_start=datetime.now(),
                timeline_end=datetime.now() + timedelta(days=120),
                data_summary={
                    "types": ["text", "document"],
                    "counts": {"qa_pairs": 5000, "documents": 2000},
                    "labeled_ratio": 1.0,
                    "size_bytes": 500000000,
                    "health_score": 92
                },
                confidentiality=ConfidentialityLevel.INTERNAL,
                status=DemandStatus.SUBMITTED,
                priority=8
            ),
            Demand(
                enterprise_id=3,  # 百货大楼
                title="智能客流分析与商品推荐系统",
                description="""
我们是一家大型零售企业，希望通过AI技术优化门店运营。
主要需求包括：1) 基于摄像头的客流统计与热力图分析；2) 基于用户行为的个性化商品推荐。
目前有部分会员消费数据和门店监控视频数据，但数据标注不完整。
                """.strip(),
                industry_tags=["零售", "商业"],
                scenario_tags=["计算机视觉", "推荐系统", "数据分析"],
                kpis=[
                    {"name": "客流统计准确率", "target": "≥90%", "metric": "accuracy"},
                    {"name": "推荐点击率", "target": "提升20%", "metric": "ctr_improvement"},
                    {"name": "转化率", "target": "提升15%", "metric": "conversion"}
                ],
                budget_min=200000,
                budget_max=400000,
                timeline_start=datetime.now(),
                timeline_end=datetime.now() + timedelta(days=150),
                data_summary={
                    "types": ["video", "csv"],
                    "counts": {"video_hours": 5000, "user_records": 100000},
                    "labeled_ratio": 0.3,
                    "size_bytes": 10000000000,
                    "health_score": 65
                },
                confidentiality=ConfidentialityLevel.INTERNAL,
                status=DemandStatus.DRAFT,
                priority=7
            )
        ]
        
        for demand in demands:
            db.add(demand)
        
        db.commit()
        print(f"已创建 {len(demands)} 个需求")
        
        print("\n数据库初始化完成！")
        print("\n=== 测试账号 ===")
        print("管理员: admin@platform.com / admin123")
        print("长安汽车: changan@demo.com / demo123")
        print("小易智联: xiaoyi@demo.com / demo123")
        
    except Exception as e:
        print(f"初始化失败: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    init_database()
