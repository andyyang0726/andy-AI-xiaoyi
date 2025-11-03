import React, { useState, useEffect } from 'react';
import {
  Card,
  Table,
  Tag,
  Space,
  Typography,
  Spin,
  Alert,
  Empty,
  Tooltip,
  Row,
  Col,
  Statistic,
  Progress,
  Button,
  Descriptions
} from 'antd';
import {
  BankOutlined,
  RocketOutlined,
  StarOutlined,
  PhoneOutlined,
  MailOutlined,
  EnvironmentOutlined,
  DollarOutlined,
  CalendarOutlined,
  FileTextOutlined
} from '@ant-design/icons';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import { usePermissions } from '../hooks/usePermissions';

const { Title, Text, Paragraph } = Typography;

/**
 * 匹配客户页面 - 供应方专用
 * 显示匹配给我的需求及其客户企业信息
 */
const MatchedClients = () => {
  const [loading, setLoading] = useState(false);
  const [data, setData] = useState([]);
  const [pagination, setPagination] = useState({
    current: 1,
    pageSize: 10,
    total: 0
  });

  const navigate = useNavigate();
  const permissions = usePermissions();

  // 检查权限
  if (!permissions.isSupply && !permissions.isAdmin) {
    return (
      <Card>
        <Alert
          message="权限不足"
          description="只有供应方企业用户可以查看匹配的需求"
          type="error"
          showIcon
        />
      </Card>
    );
  }

  const fetchData = async (page = 1, pageSize = 10) => {
    setLoading(true);
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get(
        `${import.meta.env.VITE_API_BASE_URL}/api/v1/recommendations/my-clients`,
        {
          params: {
            skip: (page - 1) * pageSize,
            limit: pageSize
          },
          headers: {
            Authorization: `Bearer ${token}`
          }
        }
      );

      setData(response.data.items || []);
      setPagination({
        current: page,
        pageSize: pageSize,
        total: response.data.total || 0
      });
    } catch (error) {
      console.error('获取匹配客户失败:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  const handleTableChange = (pagination) => {
    fetchData(pagination.current, pagination.pageSize);
  };

  const handleViewDetail = (demandId) => {
    navigate(`/demands/${demandId}`);
  };

  // 展开行：显示需求详情和客户企业信息
  const expandedRowRender = (record) => {
    const { demand, client_enterprise, match_score, match_reason } = record;

    return (
      <div style={{ padding: '16px 24px', background: '#fafafa' }}>
        <Row gutter={24}>
          {/* 左侧：需求详情 */}
          <Col span={12}>
            <Card 
              title={
                <Space>
                  <FileTextOutlined />
                  <Text strong>需求详情</Text>
                </Space>
              }
              size="small"
            >
              <Descriptions column={1} size="small">
                <Descriptions.Item label="需求标题">
                  {demand.title}
                </Descriptions.Item>
                <Descriptions.Item label="需求描述">
                  <Paragraph ellipsis={{ rows: 3, expandable: true }}>
                    {demand.description}
                  </Paragraph>
                </Descriptions.Item>
                
                {demand.industry_tags && demand.industry_tags.length > 0 && (
                  <Descriptions.Item label="行业标签">
                    <Space wrap>
                      {demand.industry_tags.map((tag, idx) => (
                        <Tag key={idx} color="blue">{tag}</Tag>
                      ))}
                    </Space>
                  </Descriptions.Item>
                )}

                {demand.scenario_tags && demand.scenario_tags.length > 0 && (
                  <Descriptions.Item label="应用场景">
                    <Space wrap>
                      {demand.scenario_tags.map((tag, idx) => (
                        <Tag key={idx} color="green">{tag}</Tag>
                      ))}
                    </Space>
                  </Descriptions.Item>
                )}

                {(demand.budget_min || demand.budget_max) && (
                  <Descriptions.Item label="预算范围">
                    <Space>
                      <DollarOutlined style={{ color: '#faad14' }} />
                      <Text>
                        ¥{demand.budget_min || 0} - ¥{demand.budget_max || '不限'}
                      </Text>
                    </Space>
                  </Descriptions.Item>
                )}

                {(demand.timeline_start || demand.timeline_end) && (
                  <Descriptions.Item label="期望时间">
                    <Space>
                      <CalendarOutlined style={{ color: '#1890ff' }} />
                      <Text>
                        {demand.timeline_start} ~ {demand.timeline_end}
                      </Text>
                    </Space>
                  </Descriptions.Item>
                )}
              </Descriptions>

              {match_reason && (
                <Alert
                  message="匹配原因"
                  description={match_reason}
                  type="info"
                  showIcon
                  icon={<RocketOutlined />}
                  style={{ marginTop: 16 }}
                />
              )}

              <div style={{ marginTop: 16, textAlign: 'center' }}>
                <Button 
                  type="primary" 
                  onClick={() => handleViewDetail(demand.id)}
                >
                  查看需求完整信息
                </Button>
              </div>
            </Card>
          </Col>

          {/* 右侧：客户企业信息 */}
          <Col span={12}>
            <Card
              title={
                <Space>
                  <BankOutlined />
                  <Text strong>客户企业信息</Text>
                </Space>
              }
              size="small"
            >
              {client_enterprise ? (
                <Space direction="vertical" size="middle" style={{ width: '100%' }}>
                  <div>
                    <Text strong style={{ fontSize: 18 }}>
                      {client_enterprise.name}
                    </Text>
                  </div>

                  <Statistic
                    title="匹配度评分"
                    value={(match_score * 100).toFixed(0)}
                    suffix="%"
                    prefix={<StarOutlined />}
                    valueStyle={{ color: match_score > 0.7 ? '#3f8600' : '#1890ff' }}
                  />
                  <Progress
                    percent={(match_score * 100).toFixed(0)}
                    strokeColor={match_score > 0.7 ? '#52c41a' : '#1890ff'}
                  />

                  <Descriptions column={1} size="small">
                    {client_enterprise.industry && (
                      <Descriptions.Item label="所属行业">
                        <Tag color="blue">{client_enterprise.industry}</Tag>
                      </Descriptions.Item>
                    )}

                    {client_enterprise.description && (
                      <Descriptions.Item label="企业简介">
                        <Paragraph ellipsis={{ rows: 3, expandable: true }}>
                          {client_enterprise.description}
                        </Paragraph>
                      </Descriptions.Item>
                    )}

                    {client_enterprise.location && (
                      <Descriptions.Item label="企业地址">
                        <Space size={4}>
                          <EnvironmentOutlined />
                          <Text>{client_enterprise.location}</Text>
                        </Space>
                      </Descriptions.Item>
                    )}

                    {client_enterprise.contact_phone && (
                      <Descriptions.Item label="联系电话">
                        <Space size={4}>
                          <PhoneOutlined />
                          <Text copyable>{client_enterprise.contact_phone}</Text>
                        </Space>
                      </Descriptions.Item>
                    )}

                    {client_enterprise.contact_email && (
                      <Descriptions.Item label="联系邮箱">
                        <Space size={4}>
                          <MailOutlined />
                          <Text copyable>{client_enterprise.contact_email}</Text>
                        </Space>
                      </Descriptions.Item>
                    )}

                    {client_enterprise.certification_level && (
                      <Descriptions.Item label="认证等级">
                        <Tag color="gold">{client_enterprise.certification_level}</Tag>
                      </Descriptions.Item>
                    )}
                  </Descriptions>
                </Space>
              ) : (
                <Empty description="客户企业信息不可用" />
              )}
            </Card>
          </Col>
        </Row>
      </div>
    );
  };

  // 主表格列定义
  const columns = [
    {
      title: '需求标题',
      dataIndex: ['demand', 'title'],
      key: 'title',
      width: 300,
      render: (text, record) => (
        <Space direction="vertical" size={4}>
          <Text strong>{text}</Text>
          <Text type="secondary" style={{ fontSize: 12 }}>
            需求ID: {record.demand.id}
          </Text>
        </Space>
      )
    },
    {
      title: '客户企业',
      dataIndex: ['client_enterprise', 'name'],
      key: 'client_name',
      width: 200,
      render: (text) => (
        <Space>
          <BankOutlined style={{ color: '#1890ff' }} />
          <Text>{text || '未知企业'}</Text>
        </Space>
      )
    },
    {
      title: '匹配度',
      dataIndex: 'match_score',
      key: 'match_score',
      width: 120,
      align: 'center',
      sorter: (a, b) => a.match_score - b.match_score,
      render: (score) => (
        <Tag 
          color={score > 0.7 ? 'success' : 'processing'} 
          icon={<StarOutlined />}
        >
          {(score * 100).toFixed(0)}%
        </Tag>
      )
    },
    {
      title: '需求状态',
      dataIndex: ['demand', 'status'],
      key: 'status',
      width: 100,
      align: 'center',
      render: (status) => {
        const statusMap = {
          draft: { text: '草稿', color: 'default' },
          submitted: { text: '已提交', color: 'processing' },
          evaluated: { text: '已评估', color: 'warning' },
          matched: { text: '已匹配', color: 'success' },
          published: { text: '已发布', color: 'blue' }
        };
        const config = statusMap[status] || { text: status, color: 'default' };
        return <Tag color={config.color}>{config.text}</Tag>;
      }
    },
    {
      title: '创建时间',
      dataIndex: ['demand', 'created_at'],
      key: 'created_at',
      width: 180,
      render: (date) => new Date(date).toLocaleString('zh-CN')
    }
  ];

  return (
    <div className="matched-clients-page">
      <Card>
        <Space direction="vertical" size="large" style={{ width: '100%' }}>
          <div>
            <Title level={3}>
              <RocketOutlined style={{ marginRight: 12 }} />
              推荐需求
            </Title>
            <Paragraph type="secondary">
              根据您企业的能力和行业，系统为您智能推荐以下匹配的需求。点击展开查看详细信息和客户联系方式。
            </Paragraph>
          </div>

          <Table
            loading={loading}
            dataSource={data}
            columns={columns}
            rowKey={(record) => record.demand.id}
            pagination={{
              ...pagination,
              showSizeChanger: true,
              showTotal: (total) => `共 ${total} 个推荐需求`
            }}
            onChange={handleTableChange}
            expandable={{
              expandedRowRender,
              rowExpandable: () => true
            }}
            locale={{
              emptyText: (
                <Empty
                  description="暂无匹配数据"
                  image={Empty.PRESENTED_IMAGE_SIMPLE}
                >
                  <Text type="secondary">
                    当有需求匹配您的企业能力时，推荐信息将显示在这里
                  </Text>
                </Empty>
              )
            }}
          />
        </Space>
      </Card>

      <style jsx="true">{`
        .matched-clients-page .ant-card {
          transition: all 0.3s;
        }
      `}</style>
    </div>
  );
};

export default MatchedClients;
