import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Steps,
  Form,
  Input,
  Select,
  Button,
  Card,
  Space,
  message,
  Row,
  Col,
  Upload,
  Alert,
  Divider,
  Tag,
  Modal,
  Progress,
  Typography
} from 'antd';
import {
  SafetyCertificateOutlined,
  FileTextOutlined,
  TeamOutlined,
  CheckCircleOutlined,
  UploadOutlined,
  InfoCircleOutlined,
  EyeOutlined
} from '@ant-design/icons';
import api from '../services/api';

const { Step } = Steps;
const { TextArea } = Input;
const { Title, Text, Paragraph } = Typography;
const { Option } = Select;

// 行业选项
const INDUSTRY_OPTIONS = [
  '制造业', '金融服务', '医疗健康', '零售电商', '交通物流',
  '教育培训', '智慧城市', '能源电力', '农业', '文化娱乐',
  '政务服务', '建筑地产', '通信运营', '安防监控', '汽车'
];

// 企业规模选项
const COMPANY_SIZES = [
  { value: 'small', label: '小型（1-50人）' },
  { value: 'medium', label: '中型（51-500人）' },
  { value: 'large', label: '大型（500人以上）' }
];

const DemandQualification = () => {
  const navigate = useNavigate();
  const [form] = Form.useForm();
  const [currentStep, setCurrentStep] = useState(0);
  const [loading, setLoading] = useState(false);
  const [previewVisible, setPreviewVisible] = useState(false);
  const [enterpriseInfo, setEnterpriseInfo] = useState(null);
  const [formData, setFormData] = useState({
    // 企业基本信息
    credit_code: '',
    legal_person: '',
    size: '',
    address: '',
    business_scope: '',
    
    // 企业资质
    business_license: null,
    registration_certificate: null,
    tax_certificate: null,
    other_certificates: [],
    
    // 联系信息
    contact_person: '',
    contact_phone: '',
    contact_email: '',
    
    // 业务信息
    industry_tags: [],
    main_products: '',
    annual_revenue: '',
    employee_count: 0,
    established_year: ''
  });

  useEffect(() => {
    fetchEnterpriseInfo();
  }, []);

  const fetchEnterpriseInfo = async () => {
    try {
      const user = JSON.parse(localStorage.getItem('user'));
      const response = await api.get(`/enterprises/${user.enterprise_id}`);
      setEnterpriseInfo(response.data);
      
      // 检查是否已有资质信息
      if (response.data.qualification_status === 'verified') {
        Modal.info({
          title: '企业资质已认证',
          content: '您的企业资质已通过审核，可以直接发布需求。',
          onOk: () => navigate('/demands/create')
        });
      }
    } catch (error) {
      message.error('获取企业信息失败');
    }
  };

  // 计算完成度
  const calculateCompleteness = () => {
    let score = 0;
    
    // 基本信息 (30分)
    if (formData.credit_code) score += 8;
    if (formData.legal_person) score += 5;
    if (formData.size) score += 5;
    if (formData.address) score += 5;
    if (formData.business_scope && formData.business_scope.length >= 20) score += 7;
    
    // 企业资质 (40分)
    if (formData.business_license) score += 15;
    if (formData.registration_certificate) score += 10;
    if (formData.tax_certificate) score += 10;
    if (formData.other_certificates && formData.other_certificates.length > 0) score += 5;
    
    // 联系信息 (15分)
    if (formData.contact_person) score += 5;
    if (formData.contact_phone) score += 5;
    if (formData.contact_email) score += 5;
    
    // 业务信息 (15分)
    if (formData.industry_tags && formData.industry_tags.length > 0) score += 5;
    if (formData.main_products) score += 5;
    if (formData.annual_revenue) score += 3;
    if (formData.established_year) score += 2;
    
    return Math.min(score, 100);
  };

  const completeness = calculateCompleteness();

  // 步骤1: 企业基本信息
  const renderBasicInfo = () => (
    <Card title={<><FileTextOutlined /> 企业基本信息</>} bordered={false}>
      <Alert
        message="重要提示"
        description="请填写真实的企业信息，这些信息将用于审核您的企业资质。虚假信息将导致审核不通过。"
        type="warning"
        showIcon
        style={{ marginBottom: 24 }}
      />
      
      <Row gutter={16}>
        <Col span={12}>
          <Form.Item
            label="统一社会信用代码"
            name="credit_code"
            rules={[
              { required: true, message: '请输入统一社会信用代码' },
              { pattern: /^[0-9A-Z]{18}$/, message: '请输入18位有效信用代码' }
            ]}
          >
            <Input
              placeholder="18位统一社会信用代码"
              size="large"
              maxLength={18}
            />
          </Form.Item>
        </Col>
        <Col span={12}>
          <Form.Item
            label="法人代表"
            name="legal_person"
            rules={[{ required: true, message: '请输入法人代表' }]}
          >
            <Input placeholder="请输入法人代表姓名" size="large" />
          </Form.Item>
        </Col>
      </Row>

      <Row gutter={16}>
        <Col span={12}>
          <Form.Item
            label="企业规模"
            name="size"
            rules={[{ required: true, message: '请选择企业规模' }]}
          >
            <Select placeholder="请选择企业规模" size="large">
              {COMPANY_SIZES.map(size => (
                <Option key={size.value} value={size.value}>{size.label}</Option>
              ))}
            </Select>
          </Form.Item>
        </Col>
        <Col span={12}>
          <Form.Item
            label="成立年份"
            name="established_year"
            rules={[{ required: true, message: '请输入成立年份' }]}
          >
            <Input placeholder="例如：2015" size="large" maxLength={4} />
          </Form.Item>
        </Col>
      </Row>

      <Form.Item
        label="企业地址"
        name="address"
        rules={[{ required: true, message: '请输入企业地址' }]}
      >
        <Input placeholder="详细地址（省市区街道门牌号）" size="large" />
      </Form.Item>

      <Form.Item
        label="主营业务描述"
        name="business_scope"
        rules={[
          { required: true, message: '请描述主营业务' },
          { min: 20, message: '请详细描述，至少20字' }
        ]}
      >
        <TextArea
          rows={4}
          placeholder="请详细描述企业的主营业务范围、核心产品和服务（建议100-300字）"
          showCount
          maxLength={500}
        />
      </Form.Item>

      <Form.Item
        label="主要产品/服务"
        name="main_products"
        rules={[{ required: true, message: '请输入主要产品或服务' }]}
      >
        <Input placeholder="例如：汽车零部件制造、智能质检设备" size="large" />
      </Form.Item>
    </Card>
  );

  // 步骤2: 企业资质证明
  const renderQualifications = () => (
    <Card title={<><SafetyCertificateOutlined /> 企业资质证明</>} bordered={false}>
      <Alert
        message="资质要求"
        description="请上传清晰的企业资质证明文件，支持jpg、png、pdf格式。营业执照和组织机构代码证为必传项。"
        type="info"
        showIcon
        style={{ marginBottom: 24 }}
      />

      <Form.Item
        label={
          <Space>
            营业执照
            <Tag color="red">必传</Tag>
          </Space>
        }
        name="business_license"
        rules={[{ required: true, message: '请上传营业执照' }]}
        tooltip="请上传清晰的营业执照扫描件或照片"
      >
        <Upload
          listType="picture-card"
          maxCount={1}
          accept="image/*,application/pdf"
        >
          <div>
            <UploadOutlined />
            <div style={{ marginTop: 8 }}>上传营业执照</div>
          </div>
        </Upload>
      </Form.Item>

      <Form.Item
        label={
          <Space>
            组织机构代码证
            <Tag color="red">必传</Tag>
          </Space>
        }
        name="registration_certificate"
        rules={[{ required: true, message: '请上传组织机构代码证' }]}
        tooltip="如已三证合一，可上传统一社会信用代码证书"
      >
        <Upload
          listType="picture-card"
          maxCount={1}
          accept="image/*,application/pdf"
        >
          <div>
            <UploadOutlined />
            <div style={{ marginTop: 8 }}>上传代码证</div>
          </div>
        </Upload>
      </Form.Item>

      <Form.Item
        label={
          <Space>
            税务登记证
            <Tag color="orange">建议上传</Tag>
          </Space>
        }
        name="tax_certificate"
        tooltip="有助于提高审核通过率"
      >
        <Upload
          listType="picture-card"
          maxCount={1}
          accept="image/*,application/pdf"
        >
          <div>
            <UploadOutlined />
            <div style={{ marginTop: 8 }}>上传税务登记证</div>
          </div>
        </Upload>
      </Form.Item>

      <Form.Item
        label={
          <Space>
            其他资质证明
            <Tag color="blue">可选</Tag>
          </Space>
        }
        name="other_certificates"
        tooltip="如ISO认证、行业资质、专利证书等"
      >
        <Upload
          listType="picture-card"
          maxCount={5}
          accept="image/*,application/pdf"
          multiple
        >
          <div>
            <PlusOutlined />
            <div style={{ marginTop: 8 }}>上传其他证书</div>
          </div>
        </Upload>
      </Form.Item>
    </Card>
  );

  // 步骤3: 联系与业务信息
  const renderContactAndBusiness = () => (
    <Card title={<><TeamOutlined /> 联系与业务信息</>} bordered={false}>
      <Divider orientation="left">联系信息</Divider>
      
      <Row gutter={16}>
        <Col span={8}>
          <Form.Item
            label="联系人姓名"
            name="contact_person"
            rules={[{ required: true, message: '请输入联系人姓名' }]}
          >
            <Input placeholder="企业联系人" size="large" />
          </Form.Item>
        </Col>
        <Col span={8}>
          <Form.Item
            label="联系电话"
            name="contact_phone"
            rules={[
              { required: true, message: '请输入联系电话' },
              { pattern: /^1[3-9]\d{9}$/, message: '请输入有效的手机号' }
            ]}
          >
            <Input placeholder="11位手机号" size="large" />
          </Form.Item>
        </Col>
        <Col span={8}>
          <Form.Item
            label="联系邮箱"
            name="contact_email"
            rules={[
              { required: true, message: '请输入联系邮箱' },
              { type: 'email', message: '请输入有效的邮箱地址' }
            ]}
          >
            <Input placeholder="企业邮箱" size="large" />
          </Form.Item>
        </Col>
      </Row>

      <Divider orientation="left">业务信息</Divider>

      <Form.Item
        label="所属行业"
        name="industry_tags"
        rules={[
          { required: true, message: '请至少选择一个行业' },
          { type: 'array', min: 1, message: '请至少选择一个行业' }
        ]}
      >
        <Select
          mode="multiple"
          placeholder="请选择所属行业（可多选）"
          size="large"
          maxTagCount="responsive"
        >
          {INDUSTRY_OPTIONS.map(industry => (
            <Option key={industry} value={industry}>{industry}</Option>
          ))}
        </Select>
      </Form.Item>

      <Row gutter={16}>
        <Col span={12}>
          <Form.Item
            label="员工人数"
            name="employee_count"
            rules={[{ required: true, message: '请输入员工人数' }]}
          >
            <InputNumber
              min={1}
              placeholder="企业员工总数"
              style={{ width: '100%' }}
              size="large"
            />
          </Form.Item>
        </Col>
        <Col span={12}>
          <Form.Item
            label="年营业额（万元）"
            name="annual_revenue"
            tooltip="选填，有助于提高资质审核通过率"
          >
            <Input placeholder="例如：5000" size="large" />
          </Form.Item>
        </Col>
      </Row>
    </Card>
  );

  // 预览模态框
  const renderPreview = () => {
    const values = form.getFieldsValue();
    
    return (
      <Modal
        title="企业资质信息预览"
        open={previewVisible}
        onCancel={() => setPreviewVisible(false)}
        width={800}
        footer={[
          <Button key="close" onClick={() => setPreviewVisible(false)}>
            关闭
          </Button>
        ]}
      >
        <Card>
          <Space direction="vertical" size="large" style={{ width: '100%' }}>
            <div>
              <Title level={4}>企业基本信息</Title>
              <Paragraph>
                <Text strong>企业名称：</Text>{enterpriseInfo?.name || '未填写'}<br />
                <Text strong>信用代码：</Text>{values.credit_code || '未填写'}<br />
                <Text strong>法人代表：</Text>{values.legal_person || '未填写'}<br />
                <Text strong>企业规模：</Text>
                {values.size ? COMPANY_SIZES.find(s => s.value === values.size)?.label : '未填写'}<br />
                <Text strong>成立年份：</Text>{values.established_year || '未填写'}<br />
                <Text strong>企业地址：</Text>{values.address || '未填写'}
              </Paragraph>
            </div>

            <div>
              <Title level={4}>主营业务</Title>
              <Paragraph>{values.business_scope || '未填写'}</Paragraph>
              <Text strong>主要产品/服务：</Text>{values.main_products || '未填写'}
            </div>

            <div>
              <Title level={4}>联系信息</Title>
              <Paragraph>
                <Text strong>联系人：</Text>{values.contact_person || '未填写'}<br />
                <Text strong>电话：</Text>{values.contact_phone || '未填写'}<br />
                <Text strong>邮箱：</Text>{values.contact_email || '未填写'}
              </Paragraph>
            </div>

            <div>
              <Title level={4}>业务信息</Title>
              <Space wrap>
                {(values.industry_tags || []).map(tag => (
                  <Tag key={tag} color="blue">{tag}</Tag>
                ))}
              </Space>
              <Paragraph style={{ marginTop: 8 }}>
                <Text strong>员工人数：</Text>{values.employee_count || 0}人<br />
                {values.annual_revenue && (
                  <><Text strong>年营业额：</Text>{values.annual_revenue}万元</>
                )}
              </Paragraph>
            </div>

            <div>
              <Title level={4}>资质证明</Title>
              <Space direction="vertical">
                <Tag color="green">✓ 营业执照已上传</Tag>
                <Tag color="green">✓ 组织机构代码证已上传</Tag>
                {values.tax_certificate && <Tag color="green">✓ 税务登记证已上传</Tag>}
                {values.other_certificates && values.other_certificates.length > 0 && (
                  <Tag color="blue">其他证书{values.other_certificates.length}份</Tag>
                )}
              </Space>
            </div>
          </Space>
        </Card>
      </Modal>
    );
  };

  // 提交表单
  const handleSubmit = async () => {
    try {
      const values = await form.validateFields();
      setLoading(true);

      // 构造提交数据
      const submitData = {
        ...values,
        qualification_status: 'pending',  // 待审核状态
        qualification_submitted_at: new Date().toISOString()
      };

      // 调用API提交资质信息
      const user = JSON.parse(localStorage.getItem('user'));
      await api.put(`/enterprises/${user.enterprise_id}/qualification`, submitData);
      
      Modal.success({
        title: '资质信息提交成功！',
        content: (
          <div>
            <p>您的企业资质信息已提交审核，我们将在<strong>3个工作日</strong>内完成审核。</p>
            <p>审核通过后，您将可以发布AI需求。</p>
            <p>如有问题，请联系平台客服：400-xxx-xxxx</p>
          </div>
        ),
        onOk: () => navigate('/demands')
      });

    } catch (error) {
      if (error.errorFields) {
        message.error('请完善必填信息');
      } else {
        message.error(error.response?.data?.detail || '提交失败，请重试');
      }
    } finally {
      setLoading(false);
    }
  };

  // 步骤配置
  const steps = [
    {
      title: '基本信息',
      icon: <FileTextOutlined />,
      content: renderBasicInfo()
    },
    {
      title: '资质证明',
      icon: <SafetyCertificateOutlined />,
      content: renderQualifications()
    },
    {
      title: '联系与业务',
      icon: <TeamOutlined />,
      content: renderContactAndBusiness()
    }
  ];

  // 切换步骤
  const next = async () => {
    try {
      let fieldsToValidate = [];
      switch (currentStep) {
        case 0:
          fieldsToValidate = [
            'credit_code', 'legal_person', 'size', 'established_year',
            'address', 'business_scope', 'main_products'
          ];
          break;
        case 1:
          fieldsToValidate = ['business_license', 'registration_certificate'];
          break;
        case 2:
          fieldsToValidate = [
            'contact_person', 'contact_phone', 'contact_email',
            'industry_tags', 'employee_count'
          ];
          break;
        default:
          break;
      }

      if (fieldsToValidate.length > 0) {
        await form.validateFields(fieldsToValidate);
      }

      // 保存当前步骤的数据
      const currentValues = form.getFieldsValue();
      setFormData({ ...formData, ...currentValues });

      setCurrentStep(currentStep + 1);
    } catch (error) {
      message.error('请完善必填信息');
    }
  };

  const prev = () => {
    const currentValues = form.getFieldsValue();
    setFormData({ ...formData, ...currentValues });
    setCurrentStep(currentStep - 1);
  };

  return (
    <div style={{ background: '#f0f2f5', minHeight: '100vh', padding: '24px' }}>
      <Card
        style={{ maxWidth: 1000, margin: '0 auto' }}
        title={
          <Space>
            <Title level={2} style={{ margin: 0 }}>需求方企业资质录入</Title>
            <Tag color="orange">必须完成</Tag>
          </Space>
        }
      >
        {/* 完成度提示 */}
        <Alert
          message={
            <Space>
              <span>资质完成度：</span>
              <Progress
                percent={completeness}
                steps={10}
                size="small"
                style={{ width: 200 }}
                strokeColor={completeness >= 80 ? '#52c41a' : completeness >= 60 ? '#faad14' : '#ff4d4f'}
              />
              <span>{completeness}分</span>
            </Space>
          }
          description={
            completeness < 60
              ? '💡 提示：请完善企业资质信息，完成度需达到60分以上才能提交审核。'
              : completeness < 80
              ? '👍 不错：资质信息已比较完整，建议补充更多信息以提高审核通过率。'
              : '🎉 优秀：资质信息非常完整，审核通过率高！'
          }
          type={completeness >= 80 ? 'success' : completeness >= 60 ? 'warning' : 'info'}
          showIcon
          style={{ marginBottom: 24 }}
        />

        {/* 步骤条 */}
        <Steps current={currentStep} style={{ marginBottom: 32 }}>
          {steps.map(item => (
            <Step key={item.title} title={item.title} icon={item.icon} />
          ))}
        </Steps>

        {/* 表单内容 */}
        <Form
          form={form}
          layout="vertical"
          initialValues={formData}
          onValuesChange={(_, allValues) => setFormData(allValues)}
        >
          <div style={{ minHeight: 400 }}>
            {steps[currentStep].content}
          </div>
        </Form>

        {/* 操作按钮 */}
        <div style={{ marginTop: 32, textAlign: 'center' }}>
          <Space size="large">
            {currentStep > 0 && (
              <Button size="large" onClick={prev}>
                上一步
              </Button>
            )}
            
            <Button
              icon={<EyeOutlined />}
              onClick={() => {
                setFormData(form.getFieldsValue());
                setPreviewVisible(true);
              }}
              size="large"
            >
              预览资质信息
            </Button>

            {currentStep < steps.length - 1 && (
              <Button type="primary" onClick={next} size="large">
                下一步
              </Button>
            )}
            
            {currentStep === steps.length - 1 && (
              <Button
                type="primary"
                onClick={handleSubmit}
                loading={loading}
                size="large"
                icon={<CheckCircleOutlined />}
                disabled={completeness < 60}
              >
                提交审核
              </Button>
            )}
          </Space>
        </div>

        {/* 帮助提示 */}
        <Divider />
        <Alert
          message="💡 审核说明"
          description={
            <ul style={{ margin: 0, paddingLeft: 20 }}>
              <li>提交后3个工作日内完成审核，请保持联系方式畅通</li>
              <li>审核通过后，即可发布AI需求并获得供应商推荐</li>
              <li>请确保上传的资质证明文件清晰可辨</li>
              <li>如有问题，请联系平台客服：400-xxx-xxxx</li>
            </ul>
          }
          type="info"
          showIcon
        />
      </Card>

      {/* 预览模态框 */}
      {renderPreview()}
    </div>
  );
};

export default DemandQualification;
