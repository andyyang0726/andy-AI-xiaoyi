import React, { useState, useMemo } from 'react';
import { Outlet, useNavigate, useLocation } from 'react-router-dom';
import {
  Layout as AntLayout,
  Menu,
  Avatar,
  Dropdown,
  Space,
  Typography,
  Tag
} from 'antd';
import {
  DashboardOutlined,
  BankOutlined,
  FileTextOutlined,
  UserOutlined,
  LogoutOutlined,
  RocketOutlined,
  HomeOutlined,
  SafetyCertificateOutlined,
  TeamOutlined
} from '@ant-design/icons';
import { usePermissions } from '../hooks/usePermissions';

const { Header, Sider, Content } = AntLayout;
const { Title } = Typography;

const Layout = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const [collapsed, setCollapsed] = useState(false);
  const permissions = usePermissions();
  
  const user = JSON.parse(localStorage.getItem('user') || '{}');

  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    navigate('/login');
  };

  // 根据用户角色动态生成菜单
  const menuItems = useMemo(() => {
    const iconMap = {
      '/': <DashboardOutlined />,
      '/enterprises': <BankOutlined />,
      '/demands': <FileTextOutlined />,
      '/recommended': <RocketOutlined />,
      '/qualification': <SafetyCertificateOutlined />,
      '/supplier-register': <SafetyCertificateOutlined />,
      '/supplier-home': <HomeOutlined />,
      '/matched-suppliers': <TeamOutlined />,
      '/profile': <UserOutlined />
    };

    return permissions.getMenuItems().map(item => ({
      ...item,
      icon: iconMap[item.key] || <FileTextOutlined />
    }));
  }, [permissions.role]);

  // 获取角色标签
  const getRoleTag = () => {
    if (permissions.isAdmin) {
      return <Tag color="red">管理员</Tag>;
    }
    if (permissions.isDemand) {
      return <Tag color="blue">需求方</Tag>;
    }
    if (permissions.isSupply) {
      return <Tag color="green">供应方</Tag>;
    }
    return null;
  };

  const handleUserMenuClick = ({ key }) => {
    if (key === 'profile') {
      navigate('/profile');
    } else if (key === 'logout') {
      handleLogout();
    }
  };

  const userMenuItems = [
    {
      key: 'profile',
      icon: <UserOutlined />,
      label: '个人信息',
    },
    {
      key: 'logout',
      icon: <LogoutOutlined />,
      label: '退出登录',
    },
  ];

  return (
    <AntLayout style={{ minHeight: '100vh' }}>
      <Sider
        collapsible
        collapsed={collapsed}
        onCollapse={setCollapsed}
        theme="dark"
      >
        <div style={{ 
          padding: '16px', 
          textAlign: 'center',
          color: 'white',
          fontSize: collapsed ? '14px' : '18px',
          fontWeight: 'bold',
          overflow: 'hidden',
          whiteSpace: 'nowrap'
        }}>
          {collapsed ? 'AI平台' : '企业AI需求平台'}
        </div>
        <Menu
          theme="dark"
          selectedKeys={[location.pathname]}
          mode="inline"
          items={menuItems}
          onClick={({ key }) => navigate(key)}
        />
      </Sider>
      <AntLayout>
        <Header style={{ 
          padding: '0 24px', 
          background: '#fff',
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          boxShadow: '0 2px 8px rgba(0,0,0,0.1)'
        }}>
          <Space>
            <Title level={4} style={{ margin: 0 }}>
              企业AI需求对接平台
            </Title>
            {getRoleTag()}
          </Space>
          <Dropdown menu={{ items: userMenuItems, onClick: handleUserMenuClick }}>
            <Space style={{ cursor: 'pointer' }}>
              <Avatar icon={<UserOutlined />} />
              <span>{user.full_name || user.email}</span>
            </Space>
          </Dropdown>
        </Header>
        <Content style={{ margin: '24px 16px', padding: 24, background: '#fff', minHeight: 280 }}>
          <Outlet />
        </Content>
      </AntLayout>
    </AntLayout>
  );
};

export default Layout;
