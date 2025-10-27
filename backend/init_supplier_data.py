"""
初始化供应商测试数据
"""
from sqlalchemy.orm import Session
from app.core.database import SessionLocal, engine
from app.models import Enterprise, User, EnterpriseType, EnterpriseStatus
from app.core.security import get_password_hash
import random
import string


def generate_eid() -> str:
    """生成企业唯一识别码"""
    timestamp = str(int(random.random() * 10000))
    random_str = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    return f"EID-{timestamp}-{random_str}"


def init_test_supplier():
    """初始化测试供应商企业"""
    db = SessionLocal()
    
    try:
        # 检查是否已存在测试企业
        existing = db.query(Enterprise).filter(
            Enterprise.credit_code == "91500000MA5UXXXX01"
        ).first()
        
        if existing:
            print("测试供应商企业已存在，跳过创建")
            return
        
        # 创建小易智联测试供应商
        xiaoyi_enterprise = Enterprise(
            eid=generate_eid(),
            name="重庆小易智联科技有限公司",
            credit_code="91500000MA5UXXXX01",
            legal_person="张明",
            enterprise_type=EnterpriseType.SUPPLY,
            size="medium",
            industry_tags=["制造业", "金融服务", "智慧城市"],
            contact_person="李经理",
            contact_phone="13800138001",
            contact_email="contact@xiaoyi.ai",
            address="重庆市渝北区某某大厦10楼",
            business_scope="专注于计算机视觉和自然语言处理技术，为企业提供AI智能解决方案，包括智能质检、智能客服、OCR识别等产品和服务。",
            ai_capabilities=[
                "computer_vision",
                "nlp",
                "machine_learning",
                "deep_learning"
            ],
            capability_details=[
                {
                    "capability": "computer_vision",
                    "expertise_level": 5,
                    "tech_stack": "YOLOv8, PyTorch, OpenCV, TensorRT",
                    "case_description": "为某大型汽车制造企业开发智能质检系统，通过计算机视觉技术实现零部件缺陷检测，检测准确率达到99.2%，大幅提高生产效率，降低人工成本60%以上。系统已稳定运行2年，累计检测零部件超过500万件。",
                    "client_count": 15,
                    "success_rate": 95
                },
                {
                    "capability": "nlp",
                    "expertise_level": 4,
                    "tech_stack": "BERT, GPT, LangChain, FastAPI",
                    "case_description": "为某城商行开发智能客服系统，基于大语言模型实现自然对话，支持金融业务咨询、账户查询、业务办理等场景。上线后客服人工成本降低40%，用户满意度提升至92%，日均处理咨询量超过5000次。",
                    "client_count": 8,
                    "success_rate": 90
                }
            ],
            industry_experience=[
                {
                    "industry": "制造业",
                    "years": 5,
                    "notable_clients": "某汽车制造企业、某电子厂、某机械厂",
                    "description": "在制造业深耕5年，为多家大型制造企业提供智能质检、设备预测性维护等AI解决方案，累计服务客户15家，项目成功率95%以上。"
                },
                {
                    "industry": "金融服务",
                    "years": 3,
                    "notable_clients": "某城商行、某农商行",
                    "description": "为金融机构提供智能客服、风控系统等AI服务，具备丰富的金融业务理解和合规经验。"
                }
            ],
            success_cases=[
                {
                    "project_name": "某汽车制造企业智能质检系统",
                    "client_name": "某大型汽车制造企业",
                    "industry": "制造业",
                    "duration": "6个月",
                    "budget": "120万元",
                    "technologies": ["computer_vision", "deep_learning"],
                    "background": "客户是国内知名汽车制造企业，年产量超过50万辆。传统人工质检效率低、成本高，且容易出现漏检、误检。客户希望通过AI技术实现自动化质检，提高检测准确率和效率。",
                    "solution": "采用YOLOv8深度学习算法，结合工业相机和边缘计算设备，构建实时智能质检系统。系统支持多种缺陷类型识别（划痕、凹陷、污点等），检测速度达到100件/分钟。使用TensorRT进行模型优化，推理速度提升3倍。部署分布式架构，支持多产线并行检测。",
                    "results": "系统上线后，零部件缺陷检测准确率达到99.2%，检测效率提升10倍，人工成本降低60%。系统已稳定运行2年，累计检测零部件超过500万件，为客户节省成本约800万元/年。客户满意度评分9.5分（满分10分）。"
                },
                {
                    "project_name": "某银行智能客服系统",
                    "client_name": "某城市商业银行",
                    "industry": "金融服务",
                    "duration": "8个月",
                    "budget": "200万元",
                    "technologies": ["nlp", "machine_learning"],
                    "background": "客户是一家城商行，日均客服咨询量超过1万次，人工客服压力大、成本高。客户希望通过智能客服系统分流常见问题，提高服务效率和用户体验。",
                    "solution": "基于BERT和GPT大语言模型，结合金融领域知识库，构建智能对话系统。支持多轮对话、意图识别、实体抽取等功能。集成语音识别和语音合成，支持电话客服场景。采用知识图谱技术构建金融业务知识体系，提高回答准确性。部署混合人工坐席，实现智能+人工协同服务。",
                    "results": "系统上线后，智能客服分流率达到70%，人工客服成本降低40%。用户满意度从78%提升至92%，平均响应时间从5分钟降至30秒。系统日均处理咨询量超过5000次，准确率达到88%。为客户节省人力成本约150万元/年。"
                }
            ],
            team_size=35,
            team_structure="算法工程师15人，后端开发8人，前端开发5人，测试工程师5人，产品经理2人",
            status=EnterpriseStatus.VERIFIED,
            certification_level="优选企业",
            credit_score=96.0
        )
        
        db.add(xiaoyi_enterprise)
        db.commit()
        db.refresh(xiaoyi_enterprise)
        
        # 创建对应的用户账号
        xiaoyi_user = User(
            email="xiaoyi@xiaoyi.ai",
            phone="13800138001",
            full_name="李经理",
            hashed_password=get_password_hash("xiaoyi123"),
            enterprise_id=xiaoyi_enterprise.id,
            is_active=True
        )
        
        db.add(xiaoyi_user)
        db.commit()
        
        print(f"✅ 测试供应商企业创建成功：{xiaoyi_enterprise.name}")
        print(f"   企业ID: {xiaoyi_enterprise.id}")
        print(f"   EID: {xiaoyi_enterprise.eid}")
        print(f"   测试账号: xiaoyi@xiaoyi.ai / xiaoyi123")
        print(f"   信用分: {xiaoyi_enterprise.credit_score}")
        print(f"   认证级别: {xiaoyi_enterprise.certification_level}")
        
    except Exception as e:
        db.rollback()
        print(f"❌ 创建失败: {str(e)}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    print("开始初始化测试供应商数据...")
    init_test_supplier()
    print("✅ 初始化完成！")
