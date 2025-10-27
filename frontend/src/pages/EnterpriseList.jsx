import React, { useState, useEffect } from 'react';
import { Table, Tag, message } from 'antd';
import { enterpriseAPI } from '../services/api';

const EnterpriseList = () => {
  const [enterprises, setEnterprises] = useState([]);
  const [loading, setLoading] = useState(false);
  const [pagination, setPagination] = useState({ current: 1, pageSize: 10, total: 0 });

  useEffect(() => {
    loadEnterprises();
  }, [pagination.current, pagination.pageSize]);

  const loadEnterprises = async () => {
    setLoading(true);
    try {
      const response = await enterpriseAPI.list({
        skip: (pagination.current - 1) * pagination.pageSize,
        limit: pagination.pageSize
      });
      setEnterprises(response.items);
      setPagination(prev => ({ ...prev, total: response.total }));
    } catch (error) {
      message.error('加载企业列表失败');
    } finally {
      setLoading(false);
    }
  };

  const columns = [
    { title: 'EID', dataIndex: 'eid', key: 'eid', width: 150 },
    { title: '企业名称', dataIndex: 'name', key: 'name' },
    {
      title: '类型',
      dataIndex: 'enterprise_type',
      key: 'enterprise_type',
      render: (type) => {
        const typeMap = { demand: '需求方', supply: '供应方', both: '双重角色' };
        return <Tag>{typeMap[type]}</Tag>;
      }
    },
    {
      title: '行业',
      dataIndex: 'industry_tags',
      key: 'industry_tags',
      render: (tags) => tags?.map(tag => <Tag key={tag}>{tag}</Tag>)
    },
    {
      title: '状态',
      dataIndex: 'status',
      key: 'status',
      render: (status) => {
        const statusMap = {
          pending: { text: '待审核', color: 'warning' },
          verified: { text: '已认证', color: 'success' },
          rejected: { text: '已拒绝', color: 'error' }
        };
        const config = statusMap[status] || statusMap.pending;
        return <Tag color={config.color}>{config.text}</Tag>;
      }
    },
    {
      title: '信用分',
      dataIndex: 'credit_score',
      key: 'credit_score',
      render: (score) => <Tag color={score >= 90 ? 'green' : 'blue'}>{score}</Tag>
    }
  ];

  return (
    <div>
      <h2 style={{ marginBottom: 16 }}>企业管理</h2>
      <Table
        columns={columns}
        dataSource={enterprises}
        rowKey="id"
        loading={loading}
        pagination={{
          ...pagination,
          onChange: (page, pageSize) => {
            setPagination(prev => ({ ...prev, current: page, pageSize }));
          }
        }}
      />
    </div>
  );
};

export default EnterpriseList;
