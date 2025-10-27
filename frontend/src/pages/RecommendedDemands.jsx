import React, { useState, useEffect } from 'react';
import { Card, Table, Tag, Button, message, Space, Progress, Tooltip, Empty } from 'antd';
import { StarOutlined, RocketOutlined, FileTextOutlined } from '@ant-design/icons';
import { useNavigate } from 'react-router-dom';
import api from '../services/api';

const RecommendedDemands = () => {
  const [loading, setLoading] = useState(false);
  const [recommendations, setRecommendations] = useState([]);
  const [enterpriseInfo, setEnterpriseInfo] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    fetchRecommendations();
  }, []);

  const fetchRecommendations = async () => {
    try {
      setLoading(true);
      
      // 从localStorage获取用户信息
      const userStr = localStorage.getItem('user');
      if (!userStr) {
        message.error('请先登录');
        navigate('/login');
        return;
      }
      
      const user = JSON.parse(userStr);
      
      // 检查是否为供应方企业
      if (!user.enterprise_id) {
        message.warning('您还没有关联企业');
        return;
      }

      // 获取推荐需求
      const response = await api.get(`/demands/recommended/${user.enterprise_id}`);
      setRecommendations(response.data.recommendations || []);
      setEnterpriseInfo({
        id: response.data.enterprise_id,
        name: response.data.enterprise_name
      });
    } catch (error) {
      console.error('获取推荐需求失败:', error);
      if (error.response?.status === 400) {
        message.warning('只有供应方企业可以查看推荐需求');
      } else {
        message.error('获取推荐需求失败');
      }
    } finally {
      setLoading(false);
    }
  };

  const getScoreColor = (score) => {
    if (score >= 85) return '#52c41a';
    if (score >= 70) return '#1890ff';
    if (score >= 60) return '#faad14';
    return '#f5222d';
  };

  const getScoreLevel = (score) => {
    if (score >= 85) return '高度匹配';
    if (score >= 70) return '较好匹配';
    if (score >= 60) return '一般匹配';
    return '匹配度低';
  };

  const columns = [
    {
      title: '匹配度',
      key: 'score',
      width: 100,
      fixed: 'left',
      render: (_, record) => (
        <Tooltip title={getScoreLevel(record.score)}>
          <Progress
            type="circle"
            percent={record.score}
            width={60}
            strokeColor={getScoreColor(record.score)}
            format={(percent) => `${percent}`}
          />
        </Tooltip>
      ),
      sorter: (a, b) => b.score - a.score,
      defaultSortOrder: 'descend'
    },
    {
      title: '需求标题',
      dataIndex: 'demand_title',
      key: 'demand_title',
      width: 250,
      render: (text, record) => (
        <Space direction="vertical" size={0}>
          <a onClick={() => navigate(`/demands/${record.demand_id}`)}>
            {text}
          </a>
          <Tag color="blue" icon={<FileTextOutlined />}>
            {record.status === 'submitted' ? '已提交' :
             record.status === 'evaluated' ? '已评估' :
             record.status === 'matched' ? '已匹配' : record.status}
          </Tag>
        </Space>
      )
    },
    {
      title: '需求描述',
      dataIndex: 'demand_description',
      key: 'demand_description',
      ellipsis: true,
      width: 300
    },
    {
      title: '行业标签',
      dataIndex: 'industry_tags',
      key: 'industry_tags',
      width: 150,
      render: (tags) => (
        <>
          {tags?.map((tag, index) => (
            <Tag key={index} color="blue">{tag}</Tag>
          ))}
        </>
      )
    },
    {
      title: '技术场景',
      dataIndex: 'scenario_tags',
      key: 'scenario_tags',
      width: 200,
      render: (tags) => (
        <>
          {tags?.slice(0, 3).map((tag, index) => (
            <Tag key={index} color="green">{tag}</Tag>
          ))}
          {tags?.length > 3 && <Tag>+{tags.length - 3}</Tag>}
        </>
      )
    },
    {
      title: '预算范围',
      dataIndex: 'budget_range',
      key: 'budget_range',
      width: 120
    },
    {
      title: '匹配理由',
      dataIndex: 'match_reasons',
      key: 'match_reasons',
      width: 200,
      render: (reasons) => (
        <Space direction="vertical" size={2}>
          {reasons?.map((reason, index) => (
            <Tag key={index} icon={<StarOutlined />} color="gold">
              {reason}
            </Tag>
          ))}
        </Space>
      )
    },
    {
      title: '详细评分',
      key: 'score_breakdown',
      width: 200,
      render: (_, record) => {
        const breakdown = record.score_breakdown || {};
        return (
          <Space direction="vertical" size={4}>
            <div>行业匹配: {breakdown.industry_match}分</div>
            <div>技术匹配: {breakdown.semantic_similarity}分</div>
            <div>信用评分: {breakdown.credit_score}分</div>
          </Space>
        );
      }
    },
    {
      title: '操作',
      key: 'action',
      width: 150,
      fixed: 'right',
      render: (_, record) => (
        <Space>
          <Button
            type="primary"
            size="small"
            icon={<RocketOutlined />}
            onClick={() => navigate(`/demands/${record.demand_id}`)}
          >
            查看详情
          </Button>
        </Space>
      )
    }
  ];

  return (
    <div>
      <Card
        title={
          <Space>
            <RocketOutlined />
            <span>为您推荐的需求</span>
            {enterpriseInfo && (
              <Tag color="blue">{enterpriseInfo.name}</Tag>
            )}
          </Space>
        }
        extra={
          <Button onClick={fetchRecommendations} loading={loading}>
            刷新推荐
          </Button>
        }
      >
        {recommendations.length === 0 && !loading ? (
          <Empty
            description="暂无推荐需求"
            image={Empty.PRESENTED_IMAGE_SIMPLE}
          >
            <p>系统会根据您的企业能力自动推荐匹配的需求</p>
          </Empty>
        ) : (
          <>
            <div style={{ marginBottom: 16, padding: '12px', background: '#f0f2f5', borderRadius: 4 }}>
              <Space direction="vertical" size={4}>
                <div>
                  <StarOutlined style={{ color: '#faad14' }} /> 
                  {' '}系统根据您的企业能力、行业经验、技术特长等维度，为您智能推荐了 <b>{recommendations.length}</b> 个匹配需求
                </div>
                <div style={{ fontSize: 12, color: '#666' }}>
                  匹配分数越高，说明该需求与您的企业能力越匹配，建议优先关注高分需求
                </div>
              </Space>
            </div>

            <Table
              columns={columns}
              dataSource={recommendations}
              rowKey="demand_id"
              loading={loading}
              pagination={{
                pageSize: 10,
                showSizeChanger: true,
                showQuickJumper: true,
                showTotal: (total) => `共 ${total} 条推荐`
              }}
              scroll={{ x: 1500 }}
            />
          </>
        )}
      </Card>
    </div>
  );
};

export default RecommendedDemands;
