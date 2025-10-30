import React, { useState, useEffect } from 'react';
import { 
  Card, 
  Descriptions, 
  Button, 
  Modal, 
  Form, 
  Input, 
  message, 
  Tabs,
  Tag,
  Space,
  Divider,
  Alert,
  Row,
  Col
} from 'antd';
import { 
  UserOutlined, 
  MailOutlined, 
  PhoneOutlined, 
  EditOutlined,
  BankOutlined,
  SafetyCertificateOutlined,
  CheckCircleOutlined,
  ClockCircleOutlined,
  CloseCircleOutlined
} from '@ant-design/icons';
import { useNavigate } from 'react-router-dom';
import api from '../services/api';
import EnterpriseRoleSelection from '../components/EnterpriseRoleSelection';

const Profile = () => {
  const navigate = useNavigate();
  const [user, setUser] = useState(null);
  const [enterprise, setEnterprise] = useState(null);
  const [loading, setLoading] = useState(true);
  const [editModalVisible, setEditModalVisible] = useState(false);
  const [passwordModalVisible, setPasswordModalVisible] = useState(false);
  const [roleSelectionVisible, setRoleSelectionVisible] = useState(false);
  const [form] = Form.useForm();
  const [passwordForm] = Form.useForm();

  useEffect(() => {
    fetchUserProfile();
  }, []);

  const fetchUserProfile = async () => {
    try {
      setLoading(true);
      const userData = JSON.parse(localStorage.getItem('user') || '{}');
      setUser(userData);

      // 如果用户有关联企业，获取企业信息
      if (userData.enterprise_id) {
        const response = await api.get(`/enterprises/${userData.enterprise_id}`);
        setEnterprise(response.data);
      }
    } catch (error) {
      message.error('获取用户信息失败');
      console.error('Error fetching profile:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleEditProfile = () => {
    form.setFieldsValue({
      full_name: user.full_name,
      phone: user.phone,
    });
    setEditModalVisible(true);
  };

  const handleUpdateProfile = async (values) => {
    try {
      // 这里需要添加更新用户信息的API端点
      message.success('个人信息更新成功');
      setEditModalVisible(false);
      
      // 更新本地存储的用户信息
      const updatedUser = { ...user, ...values };
      localStorage.setItem('user', JSON.stringify(updatedUser));
      setUser(updatedUser);
    } catch (error) {
      message.error('更新失败：' + (error.response?.data?.detail || '未知错误'));
    }
  };

  const handleChangePassword = async (values) => {
    try {
      // 这里需要添加修改密码的API端点
      message.success('密码修改成功，请重新登录');
      setPasswordModalVisible(false);
      passwordForm.resetFields();
      
      // 登出并跳转到登录页
      setTimeout(() => {
        localStorage.removeItem('token');
        localStorage.removeItem('user');
        navigate('/login');
      }, 1500);
    } catch (error) {
      message.error('修改密码失败：' + (error.response?.data?.detail || '未知错误'));
    }
  };

  const getQualificationStatusTag = (status) => {
    const statusMap = {
      unverified: { color: 'default', icon: <CloseCircleOutlined />, text: '未提交' },
      pending: { color: 'processing', icon: <ClockCircleOutlined />, text: '待审核' },
      verified: { color: 'success', icon: <CheckCircleOutlined />, text: '已通过' },
      rejected: { color: 'error', icon: <CloseCircleOutlined />, text: '已拒绝' }
    };
    const config = statusMap[status] || statusMap.unverified;
    return <Tag color={config.color} icon={config.icon}>{config.text}</Tag>;
  };

  const getEnterpriseTypeTag = (type) => {
    const typeMap = {
      demand: { color: 'blue', text: '需求方' },
      supply: { color: 'green', text: '供应方' },
      both: { color: 'purple', text: '需求+供应' }
    };
    const config = typeMap[type] || { color: 'default', text: type };
    return <Tag color={config.color}>{config.text}</Tag>;
  };

  const getEnterpriseStatusTag = (status) => {
    const statusMap = {
      pending: { color: 'processing', text: '待审核' },
      verified: { color: 'success', text: '已认证' },
      rejected: { color: 'error', text: '已拒绝' }
    };
    const config = statusMap[status] || { color: 'default', text: status };
    return <Tag color={config.color}>{config.text}</Tag>;
  };

  const renderUserInfo = () => (
    <Card 
      title={
        <Space>
          <UserOutlined />
          <span>个人信息</span>
        </Space>
      }
      extra={
        <Button 
          type="primary" 
          icon={<EditOutlined />} 
          onClick={handleEditProfile}
        >
          编辑信息
        </Button>
      }
      loading={loading}
    >
      <Descriptions bordered column={2}>
        <Descriptions.Item label="姓名" span={1}>
          {user?.full_name || '-'}
        </Descriptions.Item>
        <Descriptions.Item label="角色" span={1}>
          <Tag color="blue">{user?.role || '-'}</Tag>
        </Descriptions.Item>
        <Descriptions.Item label="邮箱" span={1}>
          <Space>
            <MailOutlined />
            {user?.email || '-'}
          </Space>
        </Descriptions.Item>
        <Descriptions.Item label="手机号" span={1}>
          <Space>
            <PhoneOutlined />
            {user?.phone || '未设置'}
          </Space>
        </Descriptions.Item>
        <Descriptions.Item label="账号状态" span={1}>
          {user?.is_active ? (
            <Tag color="success">正常</Tag>
          ) : (
            <Tag color="error">已禁用</Tag>
          )}
        </Descriptions.Item>
        <Descriptions.Item label="注册时间" span={1}>
          {user?.created_at ? new Date(user.created_at).toLocaleString('zh-CN') : '-'}
        </Descriptions.Item>
        <Descriptions.Item label="最后登录" span={2}>
          {user?.last_login ? new Date(user.last_login).toLocaleString('zh-CN') : '首次登录'}
        </Descriptions.Item>
      </Descriptions>

      <Divider />

      <Space>
        <Button 
          type="default" 
          onClick={() => setPasswordModalVisible(true)}
        >
          修改密码
        </Button>
      </Space>
    </Card>
  );

  const renderEnterpriseInfo = () => {
    if (!user?.enterprise_id) {
      return (
        <Card 
          title={
            <Space>
              <BankOutlined />
              <span>企业信息</span>
            </Space>
          }
        >
          <Alert
            message="未关联企业"
            description={
              <div>
                <p>您的账号尚未关联企业信息。请选择您的企业角色并完成资质注册。</p>
                <p style={{ marginTop: 8, color: '#666' }}>
                  <strong>需求方企业</strong>：需要AI技术解决方案的企业<br/>
                  <strong>供应方企业</strong>：提供AI技术服务的企业
                </p>
                <Space style={{ marginTop: 16 }}>
                  <Button 
                    type="primary" 
                    size="large"
                    onClick={() => setRoleSelectionVisible(true)}
                  >
                    选择角色并注册企业
                  </Button>
                  <Button 
                    onClick={() => navigate('/enterprises')}
                  >
                    查看企业列表
                  </Button>
                </Space>
              </div>
            }
            type="info"
            showIcon
          />
        </Card>
      );
    }

    if (!enterprise) {
      return (
        <Card 
          title={
            <Space>
              <BankOutlined />
              <span>企业信息</span>
            </Space>
          }
          loading={loading}
        />
      );
    }

    return (
      <Card 
        title={
          <Space>
            <BankOutlined />
            <span>企业信息</span>
          </Space>
        }
        extra={
          <Button 
            type="primary" 
            onClick={() => navigate(`/enterprises`)}
          >
            管理企业
          </Button>
        }
      >
        <Descriptions bordered column={2}>
          <Descriptions.Item label="企业名称" span={2}>
            <strong>{enterprise.name}</strong>
          </Descriptions.Item>
          <Descriptions.Item label="企业类型" span={1}>
            {getEnterpriseTypeTag(enterprise.enterprise_type)}
          </Descriptions.Item>
          <Descriptions.Item label="认证状态" span={1}>
            {getEnterpriseStatusTag(enterprise.status)}
          </Descriptions.Item>
          <Descriptions.Item label="统一社会信用代码" span={2}>
            {enterprise.credit_code || '-'}
          </Descriptions.Item>
          <Descriptions.Item label="法定代表人" span={1}>
            {enterprise.legal_person || '-'}
          </Descriptions.Item>
          <Descriptions.Item label="企业规模" span={1}>
            {enterprise.size || '-'}
          </Descriptions.Item>
          <Descriptions.Item label="联系人" span={1}>
            {enterprise.contact_person || '-'}
          </Descriptions.Item>
          <Descriptions.Item label="联系电话" span={1}>
            {enterprise.contact_phone || '-'}
          </Descriptions.Item>
          <Descriptions.Item label="联系邮箱" span={2}>
            {enterprise.contact_email || '-'}
          </Descriptions.Item>
          <Descriptions.Item label="企业地址" span={2}>
            {enterprise.address || '-'}
          </Descriptions.Item>
          {enterprise.industry_tags && enterprise.industry_tags.length > 0 && (
            <Descriptions.Item label="行业标签" span={2}>
              {enterprise.industry_tags.map(tag => (
                <Tag key={tag}>{tag}</Tag>
              ))}
            </Descriptions.Item>
          )}
          {enterprise.ai_capabilities && enterprise.ai_capabilities.length > 0 && (
            <Descriptions.Item label="AI能力" span={2}>
              {enterprise.ai_capabilities.map(cap => (
                <Tag color="blue" key={cap}>{cap}</Tag>
              ))}
            </Descriptions.Item>
          )}
          <Descriptions.Item label="信用评分" span={1}>
            <Tag color="gold">{enterprise.credit_score || '-'} 分</Tag>
          </Descriptions.Item>
          <Descriptions.Item label="认证级别" span={1}>
            {enterprise.certification_level || '-'}
          </Descriptions.Item>
        </Descriptions>

        {/* 需求方企业资质信息 */}
        {enterprise.enterprise_type !== 'supply' && (
          <>
            <Divider orientation="left">
              <Space>
                <SafetyCertificateOutlined />
                企业资质信息
              </Space>
            </Divider>
            
            <Descriptions bordered column={2}>
              <Descriptions.Item label="资质状态" span={2}>
                {getQualificationStatusTag(enterprise.qualification_status || 'unverified')}
              </Descriptions.Item>
              
              {enterprise.qualification_submitted_at && (
                <Descriptions.Item label="提交时间" span={1}>
                  {new Date(enterprise.qualification_submitted_at).toLocaleString('zh-CN')}
                </Descriptions.Item>
              )}
              
              {enterprise.qualification_verified_at && (
                <Descriptions.Item label="审核时间" span={1}>
                  {new Date(enterprise.qualification_verified_at).toLocaleString('zh-CN')}
                </Descriptions.Item>
              )}
              
              {enterprise.established_year && (
                <Descriptions.Item label="成立年份" span={1}>
                  {enterprise.established_year}
                </Descriptions.Item>
              )}
              
              {enterprise.employee_count > 0 && (
                <Descriptions.Item label="员工人数" span={1}>
                  {enterprise.employee_count} 人
                </Descriptions.Item>
              )}
              
              {enterprise.annual_revenue && (
                <Descriptions.Item label="年营业额" span={2}>
                  {enterprise.annual_revenue}
                </Descriptions.Item>
              )}
              
              {enterprise.main_products && (
                <Descriptions.Item label="主要产品/服务" span={2}>
                  {enterprise.main_products}
                </Descriptions.Item>
              )}
            </Descriptions>

            {enterprise.qualification_status === 'unverified' && (
              <Alert
                message="企业资质未提交"
                description={
                  <div>
                    <p>您的企业资质尚未提交，请完善企业资质信息后才能提交需求。</p>
                    <Button 
                      type="primary" 
                      onClick={() => navigate('/qualification')}
                    >
                      立即完善资质
                    </Button>
                  </div>
                }
                type="warning"
                showIcon
                style={{ marginTop: 16 }}
              />
            )}

            {enterprise.qualification_status === 'pending' && (
              <Alert
                message="企业资质审核中"
                description="您的企业资质正在审核中，请耐心等待审核结果。"
                type="info"
                showIcon
                style={{ marginTop: 16 }}
              />
            )}

            {enterprise.qualification_status === 'rejected' && (
              <Alert
                message="企业资质审核未通过"
                description={
                  <div>
                    <p>您的企业资质审核未通过，请修改后重新提交。</p>
                    <Button 
                      type="primary" 
                      onClick={() => navigate('/qualification')}
                    >
                      重新提交资质
                    </Button>
                  </div>
                }
                type="error"
                showIcon
                style={{ marginTop: 16 }}
              />
            )}
          </>
        )}
      </Card>
    );
  };

  const handleRoleSelection = (role) => {
    setRoleSelectionVisible(false);
    // 根据角色导航到不同的注册页面
    if (role === 'demand') {
      // 需求方 - 跳转到简化的资质录入页面
      navigate('/qualification');
    } else if (role === 'supply') {
      // 供应方 - 跳转到详细的供应商注册页面
      navigate('/supplier-register');
    }
  };

  const tabItems = [
    {
      key: 'user',
      label: '个人信息',
      children: renderUserInfo()
    },
    {
      key: 'enterprise',
      label: '企业信息',
      children: renderEnterpriseInfo()
    }
  ];

  return (
    <div>
      <Row gutter={[16, 16]}>
        <Col span={24}>
          <Tabs items={tabItems} defaultActiveKey="user" />
        </Col>
      </Row>

      {/* 编辑个人信息弹窗 */}
      <Modal
        title="编辑个人信息"
        open={editModalVisible}
        onCancel={() => setEditModalVisible(false)}
        footer={null}
        width={600}
      >
        <Form
          form={form}
          layout="vertical"
          onFinish={handleUpdateProfile}
        >
          <Form.Item
            label="姓名"
            name="full_name"
            rules={[{ required: true, message: '请输入姓名' }]}
          >
            <Input prefix={<UserOutlined />} placeholder="请输入姓名" />
          </Form.Item>

          <Form.Item
            label="手机号"
            name="phone"
            rules={[
              { pattern: /^1[3-9]\d{9}$/, message: '请输入有效的手机号' }
            ]}
          >
            <Input prefix={<PhoneOutlined />} placeholder="请输入手机号" />
          </Form.Item>

          <Form.Item>
            <Space>
              <Button type="primary" htmlType="submit">
                保存
              </Button>
              <Button onClick={() => setEditModalVisible(false)}>
                取消
              </Button>
            </Space>
          </Form.Item>
        </Form>
      </Modal>

      {/* 修改密码弹窗 */}
      <Modal
        title="修改密码"
        open={passwordModalVisible}
        onCancel={() => setPasswordModalVisible(false)}
        footer={null}
        width={500}
      >
        <Form
          form={passwordForm}
          layout="vertical"
          onFinish={handleChangePassword}
        >
          <Form.Item
            label="当前密码"
            name="old_password"
            rules={[{ required: true, message: '请输入当前密码' }]}
          >
            <Input.Password placeholder="请输入当前密码" />
          </Form.Item>

          <Form.Item
            label="新密码"
            name="new_password"
            rules={[
              { required: true, message: '请输入新密码' },
              { min: 6, message: '密码至少6位' }
            ]}
          >
            <Input.Password placeholder="请输入新密码" />
          </Form.Item>

          <Form.Item
            label="确认新密码"
            name="confirm_password"
            dependencies={['new_password']}
            rules={[
              { required: true, message: '请确认新密码' },
              ({ getFieldValue }) => ({
                validator(_, value) {
                  if (!value || getFieldValue('new_password') === value) {
                    return Promise.resolve();
                  }
                  return Promise.reject(new Error('两次输入的密码不一致'));
                },
              }),
            ]}
          >
            <Input.Password placeholder="请再次输入新密码" />
          </Form.Item>

          <Form.Item>
            <Space>
              <Button type="primary" htmlType="submit">
                确认修改
              </Button>
              <Button onClick={() => setPasswordModalVisible(false)}>
                取消
              </Button>
            </Space>
          </Form.Item>
        </Form>
      </Modal>

      {/* 企业角色选择弹窗 */}
      <EnterpriseRoleSelection
        visible={roleSelectionVisible}
        onSelect={handleRoleSelection}
        onCancel={() => setRoleSelectionVisible(false)}
      />
    </div>
  );
};

export default Profile;
