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
  Progress
} from 'antd';
import {
  ShopOutlined,
  RocketOutlined,
  TrophyOutlined,
  StarOutlined,
  PhoneOutlined,
  MailOutlined,
  EnvironmentOutlined
} from '@ant-design/icons';
import axios from 'axios';
import { usePermissions } from '../hooks/usePermissions';

const { Title, Text, Paragraph } = Typography;

/**
 * 匹配供应商页面 - 需求方专用
 * 显示我的需求以及匹配到的供应商列表
 */
const MatchedSuppliers = () => {
  const [loading, setLoading] = useState(false);
  const [data, setData] = useState([]);
  const [pagination, setPagination] = useState({
    current: 1,
    pageSize: 10,
    total: 0
  });

  const permissions = usePermissions();

  // 检查权限
  if (!permissions.isDemand && !permissions.isAdmin) {
    return (
      <Card>
        <Alert
          message="权限不足"
          description="只有需求方企业用户可以查看匹配的供应商"
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
        `${import.meta.env.VITE_API_BASE_URL}/api/v1/recommendations/my-suppliers`,
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
      console.error('获取匹配供应商失败:', error);
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

  // 渲染供应商卡片
  const renderSupplierCard = (supplier) => {
    const { enterprise, score, reason } = supplier;
    
    return (
      <Card
        key={enterprise.id}
        size="small"
        className="supplier-card"
        hoverable
        style={{ marginBottom: 12 }}
      >
        <Row gutter={16} align="middle">
          <Col span={16}>
            <Space direction="vertical" size={4} style={{ width: '100%' }}>
              <Space>
                <ShopOutlined style={{ color: '#1890ff', fontSize: 18 }} />
                <Text strong style={{ fontSize: 16 }}>{enterprise.name}</Text>
              </Space>
              
              <Space size="small">
                <Tag color="blue">{enterprise.industry || '未知行业'}</Tag>
                {enterprise.certification_level && (
                  <Tag color="gold" icon={<TrophyOutlined />}>
                    {enterprise.certification_level}
                  </Tag>
                )}
              </Space>

              {enterprise.description && (
                <Paragraph 
                  ellipsis={{ rows: 2 }} 
                  style={{ marginBottom: 4, color: '#666' }}
                >
                  {enterprise.description}
                </Paragraph>
              )}

              <Space size="middle" style={{ fontSize: 12, color: '#999' }}>
                {enterprise.location && (
                  <Space size={4}>
                    <EnvironmentOutlined />
                    <Text type="secondary">{enterprise.location}</Text>
                  </Space>
                )}
                {enterprise.contact_phone && (
                  <Space size={4}>
                    <PhoneOutlined />
                    <Text type="secondary">{enterprise.contact_phone}</Text>
                  </Space>
                )}
                {enterprise.contact_email && (
                  <Space size={4}>
                    <MailOutlined />
                    <Text type="secondary">{enterprise.contact_email}</Text>
                  </Space>
                )}
              </Space>

              {reason && (
                <Alert
                  message="推荐理由"
                  description={reason}
                  type="info"
                  showIcon
                  icon={<RocketOutlined />}
                  style={{ marginTop: 8 }}
                />
              )}
            </Space>
          </Col>

          <Col span={8} style={{ textAlign: 'center' }}>
            <Statistic
              title="匹配度"
              value={(score * 100).toFixed(0)}
              suffix="%"
              prefix={<StarOutlined />}
              valueStyle={{ color: score > 0.7 ? '#3f8600' : '#1890ff' }}
            />
            <Progress
              percent={(score * 100).toFixed(0)}
              strokeColor={score > 0.7 ? '#52c41a' : '#1890ff'}
              size="small"
              style={{ marginTop: 8 }}
            />
          </Col>
        </Row>
      </Card>
    );
  };

  // 需求展开行渲染
  const expandedRowRender = (record) => {
    const { matched_suppliers, match_count } = record;

    if (!matched_suppliers || matched_suppliers.length === 0) {
      return (
        <Empty 
          description="暂无匹配的供应商" 
          image={Empty.PRESENTED_IMAGE_SIMPLE}
        />
      );
    }

    return (
      <div style={{ padding: '16px 24px', background: '#fafafa' }}>
        <Space direction="vertical" size="middle" style={{ width: '100%' }}>
          <Title level={5}>
            <RocketOutlined style={{ marginRight: 8 }} />
            为您推荐 {match_count} 家供应商
          </Title>
          {matched_suppliers.map(supplier => renderSupplierCard(supplier))}
        </Space>
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
      title: '需求描述',
      dataIndex: ['demand', 'description'],
      key: 'description',
      ellipsis: {
        showTitle: false,
      },
      render: (text) => (
        <Tooltip placement="topLeft" title={text}>
          <Text>{text}</Text>
        </Tooltip>
      )
    },
    {
      title: '匹配供应商数',
      dataIndex: 'match_count',
      key: 'match_count',
      width: 120,
      align: 'center',
      render: (count) => (
        <Tag color={count > 0 ? 'success' : 'default'} icon={<ShopOutlined />}>
          {count} 家
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
    <div className="matched-suppliers-page">
      <Card>
        <Space direction="vertical" size="large" style={{ width: '100%' }}>
          <div>
            <Title level={3}>
              <RocketOutlined style={{ marginRight: 12 }} />
              推荐供应商
            </Title>
            <Paragraph type="secondary">
              根据您的需求，系统为您智能推荐以下匹配的供应商企业。点击展开查看详细信息和联系方式。
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
              showTotal: (total) => `共 ${total} 个需求`
            }}
            onChange={handleTableChange}
            expandable={{
              expandedRowRender,
              rowExpandable: (record) => record.match_count > 0
            }}
            locale={{
              emptyText: (
                <Empty
                  description="暂无匹配数据"
                  image={Empty.PRESENTED_IMAGE_SIMPLE}
                >
                  <Text type="secondary">
                    创建需求并完成匹配后，推荐的供应商将显示在这里
                  </Text>
                </Empty>
              )
            }}
          />
        </Space>
      </Card>

      <style jsx="true">{`
        .matched-suppliers-page .supplier-card {
          border-left: 3px solid #1890ff;
          transition: all 0.3s;
        }
        
        .matched-suppliers-page .supplier-card:hover {
          box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
          border-left-color: #40a9ff;
        }
      `}</style>
    </div>
  );
};

export default MatchedSuppliers;
