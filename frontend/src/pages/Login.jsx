import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Form, Input, Button, message, Tabs, Space, Divider } from 'antd';
import { UserOutlined, LockOutlined, MailOutlined, PhoneOutlined, ShopOutlined } from '@ant-design/icons';
import { authAPI } from '../services/api';

const Login = () => {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [activeTab, setActiveTab] = useState('login');

  const handleLogin = async (values) => {
    setLoading(true);
    try {
      const response = await authAPI.login(values);
      localStorage.setItem('token', response.access_token);
      localStorage.setItem('user', JSON.stringify(response.user));
      message.success('登录成功！');
      navigate('/');
    } catch (error) {
      message.error(error.response?.data?.detail || '登录失败');
    } finally {
      setLoading(false);
    }
  };

  const handleRegister = async (values) => {
    setLoading(true);
    try {
      await authAPI.register(values);
      message.success('注册成功！请登录');
      setActiveTab('login');
    } catch (error) {
      message.error(error.response?.data?.detail || '注册失败');
    } finally {
      setLoading(false);
    }
  };

  const loginForm = (
    <Form onFinish={handleLogin} size="large">
      <Form.Item
        name="email"
        rules={[
          { required: true, message: '请输入邮箱' },
          { type: 'email', message: '请输入有效的邮箱地址' }
        ]}
      >
        <Input prefix={<MailOutlined />} placeholder="邮箱" />
      </Form.Item>
      <Form.Item
        name="password"
        rules={[{ required: true, message: '请输入密码' }]}
      >
        <Input.Password prefix={<LockOutlined />} placeholder="密码" />
      </Form.Item>
      <Form.Item>
        <Button type="primary" htmlType="submit" block loading={loading}>
          登录
        </Button>
      </Form.Item>
      <div style={{ textAlign: 'center', color: '#666', fontSize: '12px' }}>
        测试账号：admin@platform.com / admin123
      </div>
    </Form>
  );

  const registerForm = (
    <Form onFinish={handleRegister} size="large">
      <Form.Item
        name="email"
        rules={[
          { required: true, message: '请输入邮箱' },
          { type: 'email', message: '请输入有效的邮箱地址' }
        ]}
      >
        <Input prefix={<MailOutlined />} placeholder="邮箱" />
      </Form.Item>
      <Form.Item
        name="phone"
        rules={[{ pattern: /^1[3-9]\d{9}$/, message: '请输入有效的手机号' }]}
      >
        <Input prefix={<PhoneOutlined />} placeholder="手机号（可选）" />
      </Form.Item>
      <Form.Item
        name="full_name"
        rules={[{ required: true, message: '请输入姓名' }]}
      >
        <Input prefix={<UserOutlined />} placeholder="姓名" />
      </Form.Item>
      <Form.Item
        name="password"
        rules={[
          { required: true, message: '请输入密码' },
          { min: 6, message: '密码至少6位' }
        ]}
      >
        <Input.Password prefix={<LockOutlined />} placeholder="密码" />
      </Form.Item>
      <Form.Item
        name="confirm"
        dependencies={['password']}
        rules={[
          { required: true, message: '请确认密码' },
          ({ getFieldValue }) => ({
            validator(_, value) {
              if (!value || getFieldValue('password') === value) {
                return Promise.resolve();
              }
              return Promise.reject(new Error('两次输入的密码不一致'));
            },
          }),
        ]}
      >
        <Input.Password prefix={<LockOutlined />} placeholder="确认密码" />
      </Form.Item>
      <Form.Item>
        <Button type="primary" htmlType="submit" block loading={loading}>
          注册
        </Button>
      </Form.Item>
    </Form>
  );

  const tabItems = [
    { key: 'login', label: '登录', children: loginForm },
    { key: 'register', label: '注册', children: registerForm }
  ];

  return (
    <div className="login-container">
      <div className="login-box">
        <h1 className="login-title">企业AI需求对接平台</h1>
        <Tabs activeKey={activeTab} onChange={setActiveTab} items={tabItems} centered />
        
        <Divider style={{ marginTop: 32 }}>其他入口</Divider>
        
        <Space direction="vertical" style={{ width: '100%' }}>
          <Button
            icon={<ShopOutlined />}
            onClick={() => navigate('/supplier-register')}
            block
            size="large"
            type="dashed"
          >
            供应商企业入驻
          </Button>
          <div style={{ textAlign: 'center', color: '#999', fontSize: '12px' }}>
            💡 供应商企业入驻后可获得精准需求推荐
          </div>
        </Space>
      </div>
    </div>
  );
};

export default Login;
