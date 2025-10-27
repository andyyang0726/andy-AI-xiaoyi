import React, { useState, useEffect } from 'react';
import { Card, Row, Col, Statistic, Tag, Progress, List, Avatar, Space, Button, Empty, Badge, Tabs } from 'antd';
import {
  RocketOutlined,
  TrophyOutlined,
  StarOutlined,
  CheckCircleOutlined,
  ThunderboltOutlined,
  TeamOutlined,
  BulbOutlined,
  FileTextOutlined,
  BarChartOutlined
} from '@ant-design/icons';
import { useNavigate } from 'react-router-dom';
import api from '../services/api';

const SupplierHome = () => {
  const [loading, setLoading] = useState(false);
  const [enterpriseInfo, setEnterpriseInfo] = useState(null);
  const [recommendations, setRecommendations] = useState([]);
  const [stats, setStats] = useState({
    totalRecommendations: 0,
    highMatch: 0,
    mediumMatch: 0,
    lowMatch: 0
  });
  const navigate = useNavigate();

  useEffect(() => {
    loadSupplierData();
  }, []);

  const loadSupplierData = async () => {
    try {
      setLoading(true);
      const userStr = localStorage.getItem('user');
      if (!userStr) {
        navigate('/login');
        return;
      }
      
      const user = JSON.parse(userStr);
      if (!user.enterprise_id) {
        return;
      }

      // 获取企业信息
      const enterpriseRes = await api.get(`/enterprises/${user.enterprise_id}`);
      setEnterpriseInfo(enterpriseRes.data);

      // 获取推荐需求
      const recommendRes = await api.get(`/demands/recommended/${user.enterprise_id}?top_k=20`);
      const recs = recommendRes.data.recommendations || [];
      setRecommendations(recs);

      // 计算统计数据
      const highMatch = recs.filter(r => r.score >= 85).length;
      const mediumMatch = recs.filter(r => r.score >= 70 && r.score < 85).length;
      const lowMatch = recs.filter(r => r.score < 70).length;

      setStats({
        totalRecommendations: recs.length,
        highMatch,
        mediumMatch,
        lowMatch
      });
    } catch (error) {
      console.error('加载供应商数据失败:', error);
    } finally {
      setLoading(false);
    }
  };

  const getScoreColor = (score) => {
    if (score >= 85) return '#52c41a';
    if (score >= 70) return '#1890ff';
    return '#faad14';
  };

  const getScoreLevel = (score) => {
    if (score >= 85) return { text: '高度匹配', color: 'success' };
    if (score >= 70) return { text: '较好匹配', color: 'processing' };
    return { text: '一般匹配', color: 'warning' };
  };

  if (!enterpriseInfo) {
    return (
      <Card loading={loading}>
        <Empty description="请先关联企业信息" />
      </Card>
    );
  }

  return (
    <div style={{ padding: '0 0 24px 0' }}>
      {/* 企业信息卡片 */}
      <Card
        style={{ marginBottom: 24 }}
        bordered={false}
      >
        <Row gutter={24}>
          <Col span={6}>
            <div style={{ textAlign: 'center' }}>
              <Avatar
                size={120}
                style={{ backgroundColor: '#1890ff', fontSize: 48 }}
              >
                {enterpriseInfo.name.substring(2, 4)}
              </Avatar>
              <h2 style={{ marginTop: 16, marginBottom: 8 }}>{enterpriseInfo.name}</h2>
              <Space>
                <Tag color="blue">{enterpriseInfo.enterprise_type === 'SUPPLY' ? '供应方' : '供需双方'}</Tag>
                <Tag color="gold" icon={<StarOutlined />}>
                  {enterpriseInfo.certification_level || '认证企业'}
                </Tag>
              </Space>
              <div style={{ marginTop: 16 }}>
                <Progress
                  type="circle"
                  percent={enterpriseInfo.credit_score}
                  format={() => `${enterpriseInfo.credit_score}分`}
                  strokeColor={{
                    '0%': '#108ee9',
                    '100%': '#87d068',
                  }}
                />
                <div style={{ marginTop: 8, color: '#666' }}>企业信用评分</div>
              </div>
            </div>
          </Col>
          <Col span={18}>
            <Tabs
              defaultActiveKey="1"
              items={[
                {
                  key: '1',
                  label: '企业概况',
                  children: (
                    <div>
                      <Row gutter={[16, 16]}>
                        <Col span={12}>
                          <div><strong>企业规模：</strong>{enterpriseInfo.size || '-'}</div>
                        </Col>
                        <Col span={12}>
                          <div><strong>联系人：</strong>{enterpriseInfo.contact_person || '-'}</div>
                        </Col>
                        <Col span={12}>
                          <div><strong>联系电话：</strong>{enterpriseInfo.contact_phone || '-'}</div>
                        </Col>
                        <Col span={12}>
                          <div><strong>联系邮箱：</strong>{enterpriseInfo.contact_email || '-'}</div>
                        </Col>
                        <Col span={24}>
                          <div><strong>公司地址：</strong>{enterpriseInfo.address || '-'}</div>
                        </Col>
                        <Col span={24}>
                          <div><strong>业务范围：</strong>{enterpriseInfo.business_scope || '-'}</div>
                        </Col>
                      </Row>
                    </div>
                  )
                },
                {
                  key: '2',
                  label: 'AI能力标签',
                  children: (
                    <Space wrap>
                      {enterpriseInfo.ai_capabilities?.map((cap, index) => (
                        <Tag key={index} color="blue" icon={<ThunderboltOutlined />}>
                          {cap}
                        </Tag>
                      )) || <span style={{ color: '#999' }}>暂无AI能力标签</span>}
                    </Space>
                  )
                },
                {
                  key: '3',
                  label: '行业经验',
                  children: (
                    <Space wrap>
                      {enterpriseInfo.industry_tags?.map((tag, index) => (
                        <Tag key={index} color="green" icon={<BulbOutlined />}>
                          {tag}
                        </Tag>
                      )) || <span style={{ color: '#999' }}>暂无行业标签</span>}
                    </Space>
                  )
                }
              ]}
            />
          </Col>
        </Row>
      </Card>

      {/* 统计数据 */}
      <Row gutter={16} style={{ marginBottom: 24 }}>
        <Col span={6}>
          <Card>
            <Statistic
              title="推荐需求总数"
              value={stats.totalRecommendations}
              prefix={<RocketOutlined />}
              valueStyle={{ color: '#1890ff' }}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="高度匹配"
              value={stats.highMatch}
              prefix={<TrophyOutlined />}
              valueStyle={{ color: '#52c41a' }}
              suffix={<span style={{ fontSize: 14, color: '#999' }}>/ 85分以上</span>}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="较好匹配"
              value={stats.mediumMatch}
              prefix={<StarOutlined />}
              valueStyle={{ color: '#1890ff' }}
              suffix={<span style={{ fontSize: 14, color: '#999' }}>/ 70-85分</span>}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="一般匹配"
              value={stats.lowMatch}
              prefix={<BarChartOutlined />}
              valueStyle={{ color: '#faad14' }}
              suffix={<span style={{ fontSize: 14, color: '#999' }}>/ 70分以下</span>}
            />
          </Card>
        </Col>
      </Row>

      {/* 推荐需求列表 */}
      <Card
        title={
          <Space>
            <RocketOutlined />
            <span>为您推荐的热门需求</span>
            <Badge count={stats.highMatch} style={{ backgroundColor: '#52c41a' }} />
          </Space>
        }
        extra={
          <Button type="primary" onClick={() => navigate('/recommended')}>
            查看全部推荐
          </Button>
        }
      >
        {recommendations.length === 0 ? (
          <Empty description="暂无推荐需求" />
        ) : (
          <List
            itemLayout="horizontal"
            dataSource={recommendations.slice(0, 5)}
            renderItem={(item) => {
              const levelInfo = getScoreLevel(item.score);
              return (
                <List.Item
                  actions={[
                    <Button
                      type="link"
                      icon={<FileTextOutlined />}
                      onClick={() => navigate(`/demands/${item.demand_id}`)}
                    >
                      查看详情
                    </Button>
                  ]}
                >
                  <List.Item.Meta
                    avatar={
                      <Progress
                        type="circle"
                        percent={item.score}
                        width={60}
                        strokeColor={getScoreColor(item.score)}
                        format={(percent) => `${percent}`}
                      />
                    }
                    title={
                      <Space>
                        <a onClick={() => navigate(`/demands/${item.demand_id}`)}>
                          {item.demand_title}
                        </a>
                        <Tag color={levelInfo.color}>{levelInfo.text}</Tag>
                      </Space>
                    }
                    description={
                      <div>
                        <div style={{ marginBottom: 8 }}>
                          {item.demand_description}
                        </div>
                        <Space wrap>
                          {item.industry_tags?.map((tag, idx) => (
                            <Tag key={idx} color="blue">{tag}</Tag>
                          ))}
                          {item.scenario_tags?.slice(0, 3).map((tag, idx) => (
                            <Tag key={idx} color="green">{tag}</Tag>
                          ))}
                        </Space>
                        <div style={{ marginTop: 8 }}>
                          <Space>
                            <span style={{ color: '#999' }}>匹配理由：</span>
                            {item.match_reasons?.map((reason, idx) => (
                              <Tag key={idx} icon={<CheckCircleOutlined />} color="gold">
                                {reason}
                              </Tag>
                            ))}
                          </Space>
                        </div>
                        <div style={{ marginTop: 8, color: '#999' }}>
                          预算范围：{item.budget_range}
                        </div>
                      </div>
                    }
                  />
                </List.Item>
              );
            }}
          />
        )}
      </Card>
    </div>
  );
};

export default SupplierHome;
