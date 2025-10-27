import React, { useState } from 'react';
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
  Tag,
  Row,
  Col,
  Upload,
  InputNumber,
  Rate,
  Divider,
  Alert,
  Tooltip,
  Progress,
  Typography,
  List,
  Modal
} from 'antd';
import {
  ShopOutlined,
  SafetyCertificateOutlined,
  RobotOutlined,
  TrophyOutlined,
  UploadOutlined,
  PlusOutlined,
  DeleteOutlined,
  InfoCircleOutlined,
  EyeOutlined,
  CheckCircleOutlined
} from '@ant-design/icons';
import api from '../services/api';

const { Step } = Steps;
const { TextArea } = Input;
const { Title, Text, Paragraph } = Typography;
const { Option } = Select;

// AI技术能力选项
const AI_CAPABILITIES = [
  { value: 'computer_vision', label: '计算机视觉', icon: '👁️' },
  { value: 'nlp', label: '自然语言处理', icon: '💬' },
  { value: 'speech', label: '语音识别/合成', icon: '🎤' },
  { value: 'machine_learning', label: '机器学习', icon: '🤖' },
  { value: 'deep_learning', label: '深度学习', icon: '🧠' },
  { value: 'knowledge_graph', label: '知识图谱', icon: '🕸️' },
  { value: 'recommendation', label: '推荐系统', icon: '🎯' },
  { value: 'intelligent_search', label: '智能搜索', icon: '🔍' },
  { value: 'data_mining', label: '数据挖掘', icon: '⛏️' },
  { value: 'reinforcement_learning', label: '强化学习', icon: '🎮' },
  { value: 'edge_computing', label: '边缘计算', icon: '📡' },
  { value: 'ai_chip', label: 'AI芯片', icon: '💾' }
];

// 行业标签选项
const INDUSTRY_TAGS = [
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

// 专业水平选项
const EXPERTISE_LEVELS = [
  { value: 1, label: '初级' },
  { value: 2, label: '中级' },
  { value: 3, label: '高级' },
  { value: 4, label: '专家级' },
  { value: 5, label: '行业领先' }
];

const SupplierRegister = () => {
  const navigate = useNavigate();
  const [form] = Form.useForm();
  const [currentStep, setCurrentStep] = useState(0);
  const [loading, setLoading] = useState(false);
  const [previewVisible, setPreviewVisible] = useState(false);
  const [formData, setFormData] = useState({
    // 基本信息
    name: '',
    credit_code: '',
    legal_person: '',
    size: '',
    contact_person: '',
    contact_phone: '',
    contact_email: '',
    address: '',
    business_scope: '',
    
    // AI能力
    ai_capabilities: [],
    capability_details: [],
    
    // 行业经验
    industry_tags: [],
    industry_experience: [],
    
    // 成功案例
    success_cases: [],
    
    // 团队信息
    team_size: 0,
    key_personnel: []
  });

  // 计算完成度
  const calculateCompleteness = () => {
    let score = 0;
    
    // 基本信息 (30分)
    if (formData.name) score += 5;
    if (formData.credit_code) score += 5;
    if (formData.legal_person) score += 3;
    if (formData.size) score += 3;
    if (formData.contact_person) score += 3;
    if (formData.contact_phone) score += 3;
    if (formData.contact_email) score += 3;
    if (formData.business_scope) score += 5;
    
    // AI能力 (35分)
    if (formData.ai_capabilities?.length > 0) score += 10;
    if (formData.ai_capabilities?.length >= 3) score += 5;
    if (formData.capability_details?.length > 0) score += 10;
    if (formData.capability_details?.length >= 2) score += 10;
    
    // 行业经验 (20分)
    if (formData.industry_tags?.length > 0) score += 5;
    if (formData.industry_tags?.length >= 3) score += 5;
    if (formData.industry_experience?.length > 0) score += 10;
    
    // 成功案例 (15分)
    if (formData.success_cases?.length > 0) score += 8;
    if (formData.success_cases?.length >= 2) score += 7;
    
    return Math.min(score, 100);
  };

  const completeness = calculateCompleteness();

  // 步骤1: 基本信息
  const renderBasicInfo = () => (
    <Card title={<><ShopOutlined /> 企业基本信息</>} bordered={false}>
      <Alert
        message="提示"
        description="请填写真实的企业信息，这将影响您的企业认证和信用评级。"
        type="info"
        showIcon
        style={{ marginBottom: 24 }}
      />
      
      <Row gutter={16}>
        <Col span={12}>
          <Form.Item
            label="企业名称"
            name="name"
            rules={[{ required: true, message: '请输入企业名称' }]}
          >
            <Input
              placeholder="例如：重庆小易智联科技有限公司"
              size="large"
            />
          </Form.Item>
        </Col>
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
            />
          </Form.Item>
        </Col>
      </Row>

      <Row gutter={16}>
        <Col span={12}>
          <Form.Item
            label="法人代表"
            name="legal_person"
            rules={[{ required: true, message: '请输入法人代表' }]}
          >
            <Input placeholder="请输入法人代表姓名" size="large" />
          </Form.Item>
        </Col>
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
      </Row>

      <Row gutter={16}>
        <Col span={8}>
          <Form.Item
            label="联系人"
            name="contact_person"
            rules={[{ required: true, message: '请输入联系人' }]}
          >
            <Input placeholder="企业联系人姓名" size="large" />
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
    </Card>
  );

  // 步骤2: AI能力展示
  const renderAICapabilities = () => {
    const selectedCapabilities = Form.useWatch('ai_capabilities', form) || [];
    const capabilityDetails = Form.useWatch('capability_details', form) || [];

    return (
      <Card title={<><RobotOutlined /> AI技术能力</>} bordered={false}>
        <Alert
          message="核心环节"
          description="详细的AI能力展示将大幅提高匹配成功率！请选择您擅长的AI技术，并提供具体案例。"
          type="warning"
          showIcon
          style={{ marginBottom: 24 }}
        />

        <Form.Item
          label={
            <Space>
              AI技术方向
              <Tooltip title="请选择贵司掌握的AI技术（可多选）">
                <InfoCircleOutlined style={{ color: '#1890ff' }} />
              </Tooltip>
            </Space>
          }
          name="ai_capabilities"
          rules={[
            { required: true, message: '请至少选择一项AI技术能力' },
            { type: 'array', min: 1, message: '请至少选择一项AI技术能力' }
          ]}
        >
          <Select
            mode="multiple"
            placeholder="请选择AI技术方向"
            size="large"
            maxTagCount="responsive"
            optionLabelProp="label"
          >
            {AI_CAPABILITIES.map(cap => (
              <Option key={cap.value} value={cap.value} label={cap.label}>
                <Space>
                  <span>{cap.icon}</span>
                  <span>{cap.label}</span>
                </Space>
              </Option>
            ))}
          </Select>
        </Form.Item>

        {selectedCapabilities.length > 0 && (
          <>
            <Divider>能力详情与案例</Divider>
            
            <Form.List name="capability_details">
              {(fields, { add, remove }) => (
                <>
                  {fields.map((field, index) => (
                    <Card
                      key={field.key}
                      type="inner"
                      title={`能力展示 ${index + 1}`}
                      extra={
                        <Button
                          type="link"
                          danger
                          icon={<DeleteOutlined />}
                          onClick={() => remove(field.name)}
                        >
                          删除
                        </Button>
                      }
                      style={{ marginBottom: 16 }}
                    >
                      <Row gutter={16}>
                        <Col span={12}>
                          <Form.Item
                            {...field}
                            label="技术方向"
                            name={[field.name, 'capability']}
                            rules={[{ required: true, message: '请选择技术方向' }]}
                          >
                            <Select placeholder="选择要展示的技术" size="large">
                              {AI_CAPABILITIES.filter(cap => 
                                selectedCapabilities.includes(cap.value)
                              ).map(cap => (
                                <Option key={cap.value} value={cap.value}>
                                  {cap.icon} {cap.label}
                                </Option>
                              ))}
                            </Select>
                          </Form.Item>
                        </Col>
                        <Col span={12}>
                          <Form.Item
                            {...field}
                            label="专业水平"
                            name={[field.name, 'expertise_level']}
                            rules={[{ required: true, message: '请选择专业水平' }]}
                          >
                            <Select placeholder="评估专业水平" size="large">
                              {EXPERTISE_LEVELS.map(level => (
                                <Option key={level.value} value={level.value}>
                                  {'⭐'.repeat(level.value)} {level.label}
                                </Option>
                              ))}
                            </Select>
                          </Form.Item>
                        </Col>
                      </Row>

                      <Form.Item
                        {...field}
                        label="技术栈"
                        name={[field.name, 'tech_stack']}
                        rules={[{ required: true, message: '请输入技术栈' }]}
                      >
                        <Input
                          placeholder="例如：TensorFlow, PyTorch, BERT, YOLO, OpenCV"
                          size="large"
                        />
                      </Form.Item>

                      <Form.Item
                        {...field}
                        label="成功案例描述"
                        name={[field.name, 'case_description']}
                        rules={[
                          { required: true, message: '请描述相关成功案例' },
                          { min: 50, message: '请详细描述，至少50字' }
                        ]}
                      >
                        <TextArea
                          rows={3}
                          placeholder="请详细描述该技术的应用案例：客户背景、解决的问题、技术方案、项目成果（建议100-200字）"
                          showCount
                          maxLength={500}
                        />
                      </Form.Item>

                      <Row gutter={16}>
                        <Col span={12}>
                          <Form.Item
                            {...field}
                            label="服务客户数量"
                            name={[field.name, 'client_count']}
                          >
                            <InputNumber
                              min={0}
                              placeholder="该技术服务过的客户数"
                              style={{ width: '100%' }}
                              size="large"
                            />
                          </Form.Item>
                        </Col>
                        <Col span={12}>
                          <Form.Item
                            {...field}
                            label="项目成功率"
                            name={[field.name, 'success_rate']}
                          >
                            <InputNumber
                              min={0}
                              max={100}
                              placeholder="项目成功率（%）"
                              style={{ width: '100%' }}
                              formatter={value => `${value}%`}
                              parser={value => value.replace('%', '')}
                              size="large"
                            />
                          </Form.Item>
                        </Col>
                      </Row>
                    </Card>
                  ))}
                  
                  <Button
                    type="dashed"
                    onClick={() => add()}
                    block
                    icon={<PlusOutlined />}
                    size="large"
                  >
                    添加能力展示（建议至少添加2项）
                  </Button>
                </>
              )}
            </Form.List>
          </>
        )}
      </Card>
    );
  };

  // 步骤3: 行业经验
  const renderIndustryExperience = () => (
    <Card title={<><TrophyOutlined /> 行业经验与资质</>} bordered={false}>
      <Form.Item
        label="服务行业"
        name="industry_tags"
        rules={[
          { required: true, message: '请至少选择一个行业' },
          { type: 'array', min: 1, message: '请至少选择一个行业' }
        ]}
      >
        <Select
          mode="multiple"
          placeholder="请选择服务过的行业（可多选）"
          size="large"
          maxTagCount="responsive"
        >
          {INDUSTRY_TAGS.map(tag => (
            <Option key={tag} value={tag}>{tag}</Option>
          ))}
        </Select>
      </Form.Item>

      <Divider>行业经验详情</Divider>

      <Form.List name="industry_experience">
        {(fields, { add, remove }) => (
          <>
            {fields.map((field, index) => (
              <Card
                key={field.key}
                type="inner"
                title={`行业经验 ${index + 1}`}
                extra={
                  <Button
                    type="link"
                    danger
                    icon={<DeleteOutlined />}
                    onClick={() => remove(field.name)}
                  >
                    删除
                  </Button>
                }
                style={{ marginBottom: 16 }}
              >
                <Row gutter={16}>
                  <Col span={12}>
                    <Form.Item
                      {...field}
                      label="行业名称"
                      name={[field.name, 'industry']}
                      rules={[{ required: true, message: '请选择行业' }]}
                    >
                      <Select placeholder="选择行业" size="large">
                        {INDUSTRY_TAGS.map(tag => (
                          <Option key={tag} value={tag}>{tag}</Option>
                        ))}
                      </Select>
                    </Form.Item>
                  </Col>
                  <Col span={12}>
                    <Form.Item
                      {...field}
                      label="从业年限"
                      name={[field.name, 'years']}
                      rules={[{ required: true, message: '请输入从业年限' }]}
                    >
                      <InputNumber
                        min={0}
                        max={50}
                        placeholder="年"
                        style={{ width: '100%' }}
                        size="large"
                      />
                    </Form.Item>
                  </Col>
                </Row>

                <Form.Item
                  {...field}
                  label="典型客户"
                  name={[field.name, 'notable_clients']}
                  rules={[{ required: true, message: '请输入典型客户' }]}
                >
                  <Input
                    placeholder="例如：中国移动、招商银行、华为等（逗号分隔）"
                    size="large"
                  />
                </Form.Item>

                <Form.Item
                  {...field}
                  label="项目经验描述"
                  name={[field.name, 'description']}
                  rules={[{ required: true, message: '请描述项目经验' }]}
                >
                  <TextArea
                    rows={3}
                    placeholder="请描述在该行业的项目经验和成果"
                    showCount
                    maxLength={300}
                  />
                </Form.Item>
              </Card>
            ))}
            
            <Button
              type="dashed"
              onClick={() => add()}
              block
              icon={<PlusOutlined />}
              size="large"
            >
              添加行业经验
            </Button>
          </>
        )}
      </Form.List>

      <Divider>认证与资质</Divider>

      <Form.Item
        label="企业认证"
        name="certifications"
        tooltip="请上传相关资质证书（支持jpg、png、pdf格式）"
      >
        <Upload
          listType="picture-card"
          maxCount={5}
        >
          <div>
            <PlusOutlined />
            <div style={{ marginTop: 8 }}>上传证书</div>
          </div>
        </Upload>
      </Form.Item>

      <Row gutter={16}>
        <Col span={12}>
          <Form.Item
            label="团队规模"
            name="team_size"
            rules={[{ required: true, message: '请输入团队规模' }]}
          >
            <InputNumber
              min={1}
              placeholder="AI相关技术团队人数"
              style={{ width: '100%' }}
              size="large"
            />
          </Form.Item>
        </Col>
        <Col span={12}>
          <Form.Item
            label="核心团队构成"
            name="team_structure"
          >
            <Input
              placeholder="例如：算法工程师10人，数据科学家5人"
              size="large"
            />
          </Form.Item>
        </Col>
      </Row>
    </Card>
  );

  // 步骤4: 成功案例
  const renderSuccessCases = () => (
    <Card title={<><CheckCircleOutlined /> 成功案例展示</>} bordered={false}>
      <Alert
        message="案例质量提示"
        description="详细的成功案例能显著提升您的竞争力！建议至少提供2个完整案例。"
        type="success"
        showIcon
        style={{ marginBottom: 24 }}
      />

      <Form.List name="success_cases">
        {(fields, { add, remove }) => (
          <>
            {fields.map((field, index) => (
              <Card
                key={field.key}
                type="inner"
                title={`成功案例 ${index + 1}`}
                extra={
                  <Button
                    type="link"
                    danger
                    icon={<DeleteOutlined />}
                    onClick={() => remove(field.name)}
                  >
                    删除
                  </Button>
                }
                style={{ marginBottom: 16 }}
              >
                <Form.Item
                  {...field}
                  label="项目名称"
                  name={[field.name, 'project_name']}
                  rules={[{ required: true, message: '请输入项目名称' }]}
                >
                  <Input placeholder="例如：某银行智能客服系统" size="large" />
                </Form.Item>

                <Row gutter={16}>
                  <Col span={12}>
                    <Form.Item
                      {...field}
                      label="客户名称"
                      name={[field.name, 'client_name']}
                      rules={[{ required: true, message: '请输入客户名称' }]}
                    >
                      <Input placeholder="客户企业名称" size="large" />
                    </Form.Item>
                  </Col>
                  <Col span={12}>
                    <Form.Item
                      {...field}
                      label="所属行业"
                      name={[field.name, 'industry']}
                      rules={[{ required: true, message: '请选择行业' }]}
                    >
                      <Select placeholder="选择行业" size="large">
                        {INDUSTRY_TAGS.map(tag => (
                          <Option key={tag} value={tag}>{tag}</Option>
                        ))}
                      </Select>
                    </Form.Item>
                  </Col>
                </Row>

                <Row gutter={16}>
                  <Col span={12}>
                    <Form.Item
                      {...field}
                      label="项目周期"
                      name={[field.name, 'duration']}
                      rules={[{ required: true, message: '请输入项目周期' }]}
                    >
                      <Input placeholder="例如：6个月" size="large" />
                    </Form.Item>
                  </Col>
                  <Col span={12}>
                    <Form.Item
                      {...field}
                      label="项目金额"
                      name={[field.name, 'budget']}
                    >
                      <Input placeholder="例如：100万元（可选）" size="large" />
                    </Form.Item>
                  </Col>
                </Row>

                <Form.Item
                  {...field}
                  label="应用的AI技术"
                  name={[field.name, 'technologies']}
                  rules={[{ required: true, message: '请选择应用的技术' }]}
                >
                  <Select
                    mode="multiple"
                    placeholder="选择项目中使用的AI技术"
                    size="large"
                  >
                    {AI_CAPABILITIES.map(cap => (
                      <Option key={cap.value} value={cap.value}>
                        {cap.icon} {cap.label}
                      </Option>
                    ))}
                  </Select>
                </Form.Item>

                <Form.Item
                  {...field}
                  label="项目背景与挑战"
                  name={[field.name, 'background']}
                  rules={[
                    { required: true, message: '请描述项目背景' },
                    { min: 30, message: '请详细描述，至少30字' }
                  ]}
                >
                  <TextArea
                    rows={3}
                    placeholder="客户面临什么问题？为什么需要这个项目？"
                    showCount
                    maxLength={500}
                  />
                </Form.Item>

                <Form.Item
                  {...field}
                  label="解决方案"
                  name={[field.name, 'solution']}
                  rules={[
                    { required: true, message: '请描述解决方案' },
                    { min: 50, message: '请详细描述，至少50字' }
                  ]}
                >
                  <TextArea
                    rows={4}
                    placeholder="采用了什么技术方案？如何实施？技术亮点是什么？"
                    showCount
                    maxLength={800}
                  />
                </Form.Item>

                <Form.Item
                  {...field}
                  label="项目成果"
                  name={[field.name, 'results']}
                  rules={[
                    { required: true, message: '请描述项目成果' },
                    { min: 30, message: '请详细描述，至少30字' }
                  ]}
                >
                  <TextArea
                    rows={3}
                    placeholder="取得了什么成果？带来了什么价值？有量化指标最好（如准确率提升、成本降低等）"
                    showCount
                    maxLength={500}
                  />
                </Form.Item>

                <Form.Item
                  {...field}
                  label="案例图片"
                  name={[field.name, 'images']}
                  tooltip="上传项目截图或效果图"
                >
                  <Upload
                    listType="picture-card"
                    maxCount={3}
                  >
                    <div>
                      <PlusOutlined />
                      <div style={{ marginTop: 8 }}>上传图片</div>
                    </div>
                  </Upload>
                </Form.Item>
              </Card>
            ))}
            
            <Button
              type="dashed"
              onClick={() => add()}
              block
              icon={<PlusOutlined />}
              size="large"
            >
              添加成功案例
            </Button>
          </>
        )}
      </Form.List>
    </Card>
  );

  // 预览模态框
  const renderPreview = () => {
    const values = form.getFieldsValue();
    
    return (
      <Modal
        title="企业信息预览"
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
              <Title level={3}>{values.name || '企业名称'}</Title>
              <Space>
                <Tag color="blue">{values.size ? COMPANY_SIZES.find(s => s.value === values.size)?.label : '企业规模'}</Tag>
                <Tag color="green">信用分：80分</Tag>
                <Tag color="orange">待认证</Tag>
              </Space>
            </div>

            <div>
              <Title level={5}>主营业务</Title>
              <Paragraph>{values.business_scope || '暂无描述'}</Paragraph>
            </div>

            <div>
              <Title level={5}>AI技术能力</Title>
              <Space wrap>
                {(values.ai_capabilities || []).map(cap => {
                  const capInfo = AI_CAPABILITIES.find(c => c.value === cap);
                  return (
                    <Tag key={cap} color="blue" style={{ fontSize: 14, padding: '4px 12px' }}>
                      {capInfo?.icon} {capInfo?.label}
                    </Tag>
                  );
                })}
              </Space>
            </div>

            {values.capability_details && values.capability_details.length > 0 && (
              <div>
                <Title level={5}>核心能力展示</Title>
                <List
                  dataSource={values.capability_details}
                  renderItem={(item, index) => {
                    const capInfo = AI_CAPABILITIES.find(c => c.value === item.capability);
                    const level = EXPERTISE_LEVELS.find(l => l.value === item.expertise_level);
                    return (
                      <List.Item>
                        <List.Item.Meta
                          title={
                            <Space>
                              <span>{capInfo?.icon} {capInfo?.label}</span>
                              <Tag color="orange">{level?.label}</Tag>
                            </Space>
                          }
                          description={
                            <div>
                              <div><strong>技术栈：</strong>{item.tech_stack}</div>
                              <div style={{ marginTop: 8 }}>{item.case_description}</div>
                              {item.client_count && (
                                <div style={{ marginTop: 4 }}>
                                  <Tag>服务客户：{item.client_count}家</Tag>
                                  {item.success_rate && <Tag>成功率：{item.success_rate}%</Tag>}
                                </div>
                              )}
                            </div>
                          }
                        />
                      </List.Item>
                    );
                  }}
                />
              </div>
            )}

            <div>
              <Title level={5}>服务行业</Title>
              <Space wrap>
                {(values.industry_tags || []).map(tag => (
                  <Tag key={tag} color="purple">{tag}</Tag>
                ))}
              </Space>
            </div>

            {values.team_size && (
              <div>
                <Title level={5}>团队信息</Title>
                <Text>AI技术团队：{values.team_size}人</Text>
                {values.team_structure && <Text> / {values.team_structure}</Text>}
              </div>
            )}

            {values.success_cases && values.success_cases.length > 0 && (
              <div>
                <Title level={5}>成功案例（{values.success_cases.length}个）</Title>
                {values.success_cases.map((caseItem, index) => (
                  <Card key={index} type="inner" style={{ marginTop: 8 }}>
                    <Title level={5}>{caseItem.project_name}</Title>
                    <Space>
                      <Tag>{caseItem.client_name}</Tag>
                      <Tag color="blue">{caseItem.industry}</Tag>
                      {caseItem.duration && <Tag>周期：{caseItem.duration}</Tag>}
                    </Space>
                    <Paragraph style={{ marginTop: 8 }}>
                      <strong>方案：</strong>{caseItem.solution}
                    </Paragraph>
                    <Paragraph>
                      <strong>成果：</strong>{caseItem.results}
                    </Paragraph>
                  </Card>
                ))}
              </div>
            )}
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
        enterprise_type: 'supply',  // 供应方
        status: 'pending',          // 待审核
        credit_score: 80.0          // 初始信用分
      };

      // 调用注册API
      const response = await api.post('/enterprises/register', submitData);
      
      message.success('注册成功！您的信息已提交审核，我们将在3个工作日内完成审核。');
      
      // 跳转到登录页或成功页
      setTimeout(() => {
        navigate('/login');
      }, 2000);

    } catch (error) {
      if (error.errorFields) {
        message.error('请完善表单信息');
      } else {
        message.error(error.response?.data?.detail || '注册失败，请重试');
      }
    } finally {
      setLoading(false);
    }
  };

  // 步骤配置
  const steps = [
    {
      title: '基本信息',
      icon: <ShopOutlined />,
      content: renderBasicInfo()
    },
    {
      title: 'AI能力',
      icon: <RobotOutlined />,
      content: renderAICapabilities()
    },
    {
      title: '行业经验',
      icon: <TrophyOutlined />,
      content: renderIndustryExperience()
    },
    {
      title: '成功案例',
      icon: <CheckCircleOutlined />,
      content: renderSuccessCases()
    }
  ];

  // 切换步骤
  const next = async () => {
    try {
      // 根据当前步骤验证对应的字段
      let fieldsToValidate = [];
      switch (currentStep) {
        case 0:
          fieldsToValidate = [
            'name', 'credit_code', 'legal_person', 'size',
            'contact_person', 'contact_phone', 'contact_email',
            'address', 'business_scope'
          ];
          break;
        case 1:
          fieldsToValidate = ['ai_capabilities'];
          break;
        case 2:
          fieldsToValidate = ['industry_tags', 'team_size'];
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
    // 保存当前数据
    const currentValues = form.getFieldsValue();
    setFormData({ ...formData, ...currentValues });
    setCurrentStep(currentStep - 1);
  };

  return (
    <div style={{ background: '#f0f2f5', minHeight: '100vh', padding: '24px' }}>
      <Card
        style={{ maxWidth: 1200, margin: '0 auto' }}
        title={
          <Space>
            <Title level={2} style={{ margin: 0 }}>供应商企业入驻</Title>
            <Tag color="blue">重庆AI供需对接平台</Tag>
          </Space>
        }
      >
        {/* 完成度提示 */}
        <Alert
          message={
            <Space>
              <span>资料完成度：</span>
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
              ? '💡 提示：资料完成度越高，匹配成功率越高！建议完善到80分以上。'
              : completeness < 80
              ? '👍 不错：资料已比较完整，继续完善AI能力和成功案例可获得更多推荐。'
              : '🎉 优秀：资料非常完整，您将获得更多精准的需求推荐！'
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
              预览企业信息
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
              >
                提交入驻申请
              </Button>
            )}
          </Space>
        </div>

        {/* 帮助提示 */}
        <Divider />
        <Alert
          message="💡 入驻指南"
          description={
            <ul style={{ margin: 0, paddingLeft: 20 }}>
              <li>详细填写AI能力和成功案例，可大幅提高匹配准确率</li>
              <li>提交后3个工作日内完成审核，请保持联系方式畅通</li>
              <li>审核通过后，系统将自动为您匹配合适的需求</li>
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

export default SupplierRegister;
