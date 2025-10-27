import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Card, Descriptions, Tag, Button, Space, message, Progress, List, Spin } from 'antd';
import { ArrowLeftOutlined, ThunderboltOutlined, RocketOutlined } from '@ant-design/icons';
import { demandAPI } from '../services/api';

const DemandDetail = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [demand, setDemand] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadDemand();
  }, [id]);

  const loadDemand = async () => {
    setLoading(true);
    try {
      const response = await demandAPI.get(id);
      setDemand(response);
    } catch (error) {
      message.error('加载需求详情失败');
    } finally {
      setLoading(false);
    }
  };

  const handleEvaluate = async () => {
    try {
      await demandAPI.evaluate(id);
      message.success('评估完成！');
      loadDemand();
    } catch (error) {
      message.error('评估失败');
    }
  };

  const handleMatch = async () => {
    try {
      await demandAPI.match(id);
      message.success('匹配完成！');
      loadDemand();
    } catch (error) {
      message.error('匹配失败');
    }
  };

  if (loading || !demand) {
    return <Spin size="large" style={{ display: 'block', margin: '100px auto' }} />;
  }

  const evaluation = demand.evaluation_result;
  const matches = demand.match_results || [];

  return (
    <div>
      <Button icon={<ArrowLeftOutlined />} onClick={() => navigate('/demands')} style={{ marginBottom: 16 }}>
        返回列表
      </Button>

      <Card title={demand.title} extra={
        <Space>
          {demand.status === 'submitted' && (
            <Button type="primary" icon={<ThunderboltOutlined />} onClick={handleEvaluate}>
              评估需求
            </Button>
          )}
          {demand.status === 'evaluated' && (
            <Button type="primary" icon={<RocketOutlined />} onClick={handleMatch}>
              匹配供应商
            </Button>
          )}
        </Space>
      }>
        <Descriptions column={2} bordered>
          <Descriptions.Item label="需求ID">{demand.id}</Descriptions.Item>
          <Descriptions.Item label="状态">
            <Tag color="blue">{demand.status}</Tag>
          </Descriptions.Item>
          <Descriptions.Item label="行业标签" span={2}>
            {demand.industry_tags?.map(tag => <Tag key={tag}>{tag}</Tag>)}
          </Descriptions.Item>
          <Descriptions.Item label="场景标签" span={2}>
            {demand.scenario_tags?.map(tag => <Tag key={tag} color="green">{tag}</Tag>)}
          </Descriptions.Item>
          <Descriptions.Item label="需求描述" span={2}>
            {demand.description}
          </Descriptions.Item>
          <Descriptions.Item label="预算范围">
            {demand.budget_min && demand.budget_max
              ? `${demand.budget_min.toLocaleString()} - ${demand.budget_max.toLocaleString()} 元`
              : '未设置'}
          </Descriptions.Item>
          <Descriptions.Item label="优先级">
            <Tag color={demand.priority >= 8 ? 'red' : 'orange'}>{demand.priority}</Tag>
          </Descriptions.Item>
          <Descriptions.Item label="创建时间">
            {new Date(demand.created_at).toLocaleString('zh-CN')}
          </Descriptions.Item>
          <Descriptions.Item label="提交时间">
            {demand.submitted_at ? new Date(demand.submitted_at).toLocaleString('zh-CN') : '未提交'}
          </Descriptions.Item>
        </Descriptions>
      </Card>

      {evaluation && (
        <Card title="智能评估结果" style={{ marginTop: 16 }}>
          <Space direction="vertical" style={{ width: '100%' }} size="large">
            <div>
              <p><strong>技术可行性：</strong></p>
              <Progress percent={evaluation.feasibility_score} status="active" />
            </div>
            <div>
              <p><strong>项目就绪度：</strong></p>
              <Progress percent={evaluation.readiness_score} status="active" strokeColor="#52c41a" />
            </div>
            {evaluation.data_health_score && (
              <div>
                <p><strong>数据健康度：</strong></p>
                <Progress percent={evaluation.data_health_score} status="active" strokeColor="#1890ff" />
              </div>
            )}
            <Descriptions column={2} bordered>
              <Descriptions.Item label="风险等级">
                <Tag color={evaluation.risk_level === 'high' ? 'red' : evaluation.risk_level === 'medium' ? 'orange' : 'green'}>
                  {evaluation.risk_level === 'high' ? '高' : evaluation.risk_level === 'medium' ? '中' : '低'}
                </Tag>
              </Descriptions.Item>
              <Descriptions.Item label="推荐路径">
                <Tag color="blue">
                  {evaluation.recommended_path === 'direct' ? '直接交付' :
                    evaluation.recommended_path === 'pilot' ? '试点项目' : 'PoC验证'}
                </Tag>
              </Descriptions.Item>
              <Descriptions.Item label="评估置信度">
                {(evaluation.confidence * 100).toFixed(0)}%
              </Descriptions.Item>
            </Descriptions>
            {evaluation.notes && evaluation.notes.length > 0 && (
              <div>
                <p><strong>改进建议：</strong></p>
                <ul>
                  {evaluation.notes.map((note, index) => (
                    <li key={index}>{note}</li>
                  ))}
                </ul>
              </div>
            )}
          </Space>
        </Card>
      )}

      {matches.length > 0 && (
        <Card title="匹配的供应商" style={{ marginTop: 16 }}>
          <List
            dataSource={matches}
            renderItem={(match, index) => (
              <List.Item key={index}>
                <List.Item.Meta
                  title={
                    <Space>
                      <span>#{index + 1}</span>
                      <strong>{match.vendor_name}</strong>
                      <Tag color="blue">匹配度: {match.score}%</Tag>
                    </Space>
                  }
                  description={
                    <div>
                      <p><strong>匹配理由：</strong></p>
                      {match.reasons?.map((reason, i) => (
                        <Tag key={i} color="green">{reason}</Tag>
                      ))}
                      {match.contact_email && (
                        <p style={{ marginTop: 8 }}>
                          <strong>联系方式：</strong> {match.contact_email}
                        </p>
                      )}
                    </div>
                  }
                />
              </List.Item>
            )}
          />
        </Card>
      )}
    </div>
  );
};

export default DemandDetail;
