import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Table, Button, Tag, Space, message, Popconfirm, Select } from 'antd';
import { PlusOutlined, EyeOutlined, DeleteOutlined, ThunderboltOutlined, RocketOutlined } from '@ant-design/icons';
import { demandAPI } from '../services/api';

const DemandList = () => {
  const navigate = useNavigate();
  const [demands, setDemands] = useState([]);
  const [loading, setLoading] = useState(false);
  const [pagination, setPagination] = useState({ current: 1, pageSize: 10, total: 0 });
  const [statusFilter, setStatusFilter] = useState(null);

  useEffect(() => {
    loadDemands();
  }, [pagination.current, pagination.pageSize, statusFilter]);

  const loadDemands = async () => {
    setLoading(true);
    try {
      const params = {
        skip: (pagination.current - 1) * pagination.pageSize,
        limit: pagination.pageSize
      };
      if (statusFilter) {
        params.status_filter = statusFilter;
      }
      
      const response = await demandAPI.list(params);
      setDemands(response.items);
      setPagination(prev => ({ ...prev, total: response.total }));
    } catch (error) {
      message.error('加载需求列表失败');
    } finally {
      setLoading(false);
    }
  };

  const handleEvaluate = async (id) => {
    try {
      await demandAPI.evaluate(id);
      message.success('评估完成！');
      loadDemands();
    } catch (error) {
      message.error('评估失败');
    }
  };

  const handleMatch = async (id) => {
    try {
      await demandAPI.match(id);
      message.success('匹配完成！');
      loadDemands();
    } catch (error) {
      message.error('匹配失败');
    }
  };

  const handleDelete = async (id) => {
    try {
      await demandAPI.delete(id);
      message.success('删除成功');
      loadDemands();
    } catch (error) {
      message.error('删除失败');
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
      title: 'ID',
      dataIndex: 'id',
      key: 'id',
      width: 60
    },
    {
      title: '需求标题',
      dataIndex: 'title',
      key: 'title',
      render: (text, record) => (
        <a onClick={() => navigate(`/demands/${record.id}`)}>{text}</a>
      )
    },
    {
      title: '行业标签',
      dataIndex: 'industry_tags',
      key: 'industry_tags',
      render: (tags) => tags?.map(tag => <Tag key={tag}>{tag}</Tag>)
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
    },
    {
      title: '操作',
      key: 'action',
      fixed: 'right',
      width: 280,
      render: (_, record) => (
        <Space size="small">
          <Button
            size="small"
            icon={<EyeOutlined />}
            onClick={() => navigate(`/demands/${record.id}`)}
          >
            查看
          </Button>
          {record.status === 'submitted' && (
            <Button
              size="small"
              type="primary"
              icon={<ThunderboltOutlined />}
              onClick={() => handleEvaluate(record.id)}
            >
              评估
            </Button>
          )}
          {record.status === 'evaluated' && (
            <Button
              size="small"
              type="primary"
              icon={<RocketOutlined />}
              onClick={() => handleMatch(record.id)}
            >
              匹配
            </Button>
          )}
          <Popconfirm
            title="确定删除此需求吗？"
            onConfirm={() => handleDelete(record.id)}
            okText="确定"
            cancelText="取消"
          >
            <Button size="small" danger icon={<DeleteOutlined />}>
              删除
            </Button>
          </Popconfirm>
        </Space>
      )
    }
  ];

  return (
    <div>
      <div style={{ marginBottom: 16, display: 'flex', justifyContent: 'space-between' }}>
        <Space>
          <span>状态筛选：</span>
          <Select
            style={{ width: 150 }}
            placeholder="全部状态"
            allowClear
            onChange={setStatusFilter}
            options={Object.entries(statusMap).map(([value, { text }]) => ({
              label: text,
              value
            }))}
          />
        </Space>
        <Button
          type="primary"
          icon={<PlusOutlined />}
          onClick={() => navigate('/demands/create')}
        >
          创建需求
        </Button>
      </div>
      
      <Table
        columns={columns}
        dataSource={demands}
        rowKey="id"
        loading={loading}
        pagination={{
          ...pagination,
          onChange: (page, pageSize) => {
            setPagination(prev => ({ ...prev, current: page, pageSize }));
          }
        }}
        scroll={{ x: 1200 }}
      />
    </div>
  );
};

export default DemandList;
