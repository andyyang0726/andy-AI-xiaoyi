import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Row, Col, Card, Statistic, Button, Table, Tag, Space } from 'antd';
import {
  RiseOutlined,
  BankOutlined,
  FileTextOutlined,
  CheckCircleOutlined,
  PlusOutlined
} from '@ant-design/icons';
import { enterpriseAPI, demandAPI } from '../services/api';

const Dashboard = () => {
  const navigate = useNavigate();
  const [stats, setStats] = useState({
    totalEnterprises: 0,
    totalDemands: 0,
    evaluatedDemands: 0,
    matchedDemands: 0
  });
  const [recentDemands, setRecentDemands] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadDashboardData();
  }, []);

  const loadDashboardData = async () => {
    setLoading(true);
    try {
      const [enterprisesRes, demandsRes] = await Promise.all([
        enterpriseAPI.list({ limit: 1 }),
        demandAPI.list({ limit: 10 })
      ]);

      setStats({
        totalEnterprises: enterprisesRes.total,
        totalDemands: demandsRes.total,
        evaluatedDemands: demandsRes.items.filter(d => d.evaluation_result).length,
        matchedDemands: demandsRes.items.filter(d => d.match_results?.length > 0).length
      });

      setRecentDemands(demandsRes.items.slice(0, 5));
    } catch (error) {
      console.error('加载数据失败:', error);
    } finally {
      setLoading(false);
    }
  };

  const statusMap = {
    draft: { text: '草稿', color: 'default' },
    submitted: { text: '已提交', color: 'blue' },
    evaluating: { text: '评估中', color: 'processing' },
    evaluated: { text: '已评估', color: 'success' },
    matching: { text: '匹配中', color: 'processing' },
    matched: { text: '已匹配', color: 'success' },
    in_progress: { text: '进行中', color: 'processing' },
    completed: { text: '已完成', color: 'success' },
    closed: { text: '已关闭', color: 'default' }
  };

  const columns = [
    {
      title: '需求标题',
      dataIndex: 'title',
      key: 'title',
      render: (text, record) => (
        <a onClick={() => navigate(`/demands/${record.id}`)}>{text}</a>
      )
    },
    {
      title: '状态',
      dataIndex: 'status',
      key: 'status',
      render: (status) => {
        const config = statusMap[status] || statusMap.draft;
        return <Tag color={config.color}>{config.text}</Tag>;
      }
    },
    {
      title: '优先级',
      dataIndex: 'priority',
      key: 'priority',
      render: (priority) => {
        const color = priority >= 8 ? 'red' : priority >= 5 ? 'orange' : 'green';
        return <Tag color={color}>{priority}</Tag>;
      }
    },
    {
      title: '创建时间',
      dataIndex: 'created_at',
      key: 'created_at',
      render: (date) => new Date(date).toLocaleDateString('zh-CN')
    }
  ];

  return (
    <div>
      <h2 style={{ marginBottom: 24 }}>工作台</h2>
      
      <Row gutter={16} style={{ marginBottom: 24 }}>
        <Col span={6}>
          <Card>
            <Statistic
              title="企业总数"
              value={stats.totalEnterprises}
              prefix={<BankOutlined />}
              valueStyle={{ color: '#3f8600' }}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="需求总数"
              value={stats.totalDemands}
              prefix={<FileTextOutlined />}
              valueStyle={{ color: '#1890ff' }}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="已评估"
              value={stats.evaluatedDemands}
              prefix={<CheckCircleOutlined />}
              valueStyle={{ color: '#cf1322' }}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="已匹配"
              value={stats.matchedDemands}
              prefix={<RiseOutlined />}
              valueStyle={{ color: '#722ed1' }}
            />
          </Card>
        </Col>
      </Row>

      <Card
        title="最近需求"
        extra={
          <Button
            type="primary"
            icon={<PlusOutlined />}
            onClick={() => navigate('/demands/create')}
          >
            创建需求
          </Button>
        }
      >
        <Table
          columns={columns}
          dataSource={recentDemands}
          rowKey="id"
          loading={loading}
          pagination={false}
        />
      </Card>
    </div>
  );
};

export default Dashboard;
