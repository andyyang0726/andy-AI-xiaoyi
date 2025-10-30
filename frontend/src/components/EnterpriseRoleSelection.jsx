import React, { useState } from 'react';
import { Modal, Card, Row, Col, Typography, Button, Space } from 'antd';
import { 
  ShoppingOutlined, 
  ShopOutlined,
  ArrowRightOutlined,
  CheckOutlined
} from '@ant-design/icons';

const { Title, Paragraph } = Typography;

const EnterpriseRoleSelection = ({ visible, onSelect, onCancel }) => {
  const [selectedRole, setSelectedRole] = useState(null);

  const handleConfirm = () => {
    if (selectedRole) {
      onSelect(selectedRole);
      setSelectedRole(null);
    }
  };

  const roleCards = [
    {
      key: 'demand',
      title: '需求方企业',
      icon: <ShoppingOutlined style={{ fontSize: 48, color: '#1890ff' }} />,
      description: '我需要AI技术解决方案',
      features: [
        '发布AI需求',
        '获取供应商推荐',
        '需求匹配服务',
        '简化资质审核'
      ],
      color: '#e6f7ff',
      borderColor: '#91d5ff'
    },
    {
      key: 'supply',
      title: '供应方企业',
      icon: <ShopOutlined style={{ fontSize: 48, color: '#52c41a' }} />,
      description: '我可以提供AI技术服务',
      features: [
        '展示AI能力',
        '接收需求推荐',
        '企业主页展示',
        '详细资质认证'
      ],
      color: '#f6ffed',
      borderColor: '#b7eb8f'
    }
  ];

  return (
    <Modal
      title={<Title level={3}>选择您的企业角色</Title>}
      open={visible}
      onCancel={() => {
        setSelectedRole(null);
        onCancel();
      }}
      width={800}
      footer={[
        <Button key="cancel" onClick={onCancel}>
          取消
        </Button>,
        <Button
          key="confirm"
          type="primary"
          disabled={!selectedRole}
          onClick={handleConfirm}
          icon={<ArrowRightOutlined />}
        >
          继续填写资质
        </Button>
      ]}
    >
      <Paragraph style={{ marginBottom: 24, fontSize: 16 }}>
        请选择您的企业类型，不同类型的企业需要提交不同的资质信息
      </Paragraph>

      <Row gutter={16}>
        {roleCards.map(role => (
          <Col span={12} key={role.key}>
            <Card
              hoverable
              style={{
                height: '100%',
                backgroundColor: selectedRole === role.key ? role.color : '#fff',
                borderColor: selectedRole === role.key ? role.borderColor : '#d9d9d9',
                borderWidth: selectedRole === role.key ? 2 : 1,
                cursor: 'pointer',
                position: 'relative'
              }}
              onClick={() => setSelectedRole(role.key)}
            >
              {selectedRole === role.key && (
                <CheckOutlined
                  style={{
                    position: 'absolute',
                    top: 10,
                    right: 10,
                    fontSize: 24,
                    color: role.key === 'demand' ? '#1890ff' : '#52c41a'
                  }}
                />
              )}
              
              <Space direction="vertical" size="large" style={{ width: '100%' }}>
                <div style={{ textAlign: 'center' }}>
                  {role.icon}
                </div>
                
                <div>
                  <Title level={4} style={{ marginBottom: 8 }}>
                    {role.title}
                  </Title>
                  <Paragraph type="secondary">
                    {role.description}
                  </Paragraph>
                </div>

                <div>
                  <Paragraph strong style={{ marginBottom: 8 }}>
                    主要功能：
                  </Paragraph>
                  <ul style={{ paddingLeft: 20, marginBottom: 0 }}>
                    {role.features.map((feature, index) => (
                      <li key={index} style={{ marginBottom: 4 }}>
                        {feature}
                      </li>
                    ))}
                  </ul>
                </div>
              </Space>
            </Card>
          </Col>
        ))}
      </Row>
    </Modal>
  );
};

export default EnterpriseRoleSelection;
