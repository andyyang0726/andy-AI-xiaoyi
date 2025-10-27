import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Form, Input, Button, Select, InputNumber, DatePicker, Card, message } from 'antd';
import { demandAPI } from '../services/api';

const { TextArea } = Input;
const { RangePicker } = DatePicker;

const DemandCreate = () => {
  const navigate = useNavigate();
  const [form] = Form.useForm();
  const [loading, setLoading] = useState(false);
  const user = JSON.parse(localStorage.getItem('user') || '{}');

  const handleSubmit = async (values) => {
    setLoading(true);
    try {
      const demandData = {
        ...values,
        enterprise_id: user.enterprise_id || 1, // MVP阶段默认企业ID
        timeline_start: values.timeline?.[0]?.toISOString(),
        timeline_end: values.timeline?.[1]?.toISOString()
      };
      delete demandData.timeline;

      const response = await demandAPI.create(demandData);
      message.success('需求创建成功！');
      navigate(`/demands/${response.id}`);
    } catch (error) {
      message.error('创建失败：' + (error.response?.data?.detail || '未知错误'));
    } finally {
      setLoading(false);
    }
  };

  return (
    <Card title="创建新需求">
      <Form
        form={form}
        layout="vertical"
        onFinish={handleSubmit}
        initialValues={{
          priority: 5,
          confidentiality: 'internal'
        }}
      >
        <Form.Item
          label="需求标题"
          name="title"
          rules={[{ required: true, message: '请输入需求标题' }, { min: 5, message: '标题至少5个字符' }]}
        >
          <Input placeholder="例如：智能质检系统开发需求" />
        </Form.Item>

        <Form.Item
          label="需求描述"
          name="description"
          rules={[{ required: true, message: '请输入需求描述' }, { min: 10, message: '描述至少10个字符' }]}
        >
          <TextArea rows={6} placeholder="详细描述您的AI需求..." />
        </Form.Item>

        <Form.Item label="行业标签" name="industry_tags">
          <Select
            mode="multiple"
            placeholder="选择行业"
            options={[
              { value: '制造业', label: '制造业' },
              { value: '金融', label: '金融' },
              { value: '零售', label: '零售' },
              { value: '医疗', label: '医疗' },
              { value: '政务', label: '政务' },
              { value: '教育', label: '教育' }
            ]}
          />
        </Form.Item>

        <Form.Item label="场景标签" name="scenario_tags">
          <Select
            mode="multiple"
            placeholder="选择应用场景"
            options={[
              { value: '图像识别', label: '图像识别' },
              { value: '文本分类', label: '文本分类' },
              { value: '语音识别', label: '语音识别' },
              { value: '推荐系统', label: '推荐系统' },
              { value: '预测分析', label: '预测分析' },
              { value: '目标检测', label: '目标检测' },
              { value: '自然语言处理', label: '自然语言处理' }
            ]}
          />
        </Form.Item>

        <Form.Item label="预算范围（元）">
          <Input.Group compact>
            <Form.Item name="budget_min" noStyle>
              <InputNumber placeholder="最低预算" style={{ width: '50%' }} min={0} />
            </Form.Item>
            <Form.Item name="budget_max" noStyle>
              <InputNumber placeholder="最高预算" style={{ width: '50%' }} min={0} />
            </Form.Item>
          </Input.Group>
        </Form.Item>

        <Form.Item label="预计时间" name="timeline">
          <RangePicker style={{ width: '100%' }} />
        </Form.Item>

        <Form.Item label="保密等级" name="confidentiality">
          <Select>
            <Select.Option value="public">公开</Select.Option>
            <Select.Option value="internal">内部</Select.Option>
            <Select.Option value="confidential">机密</Select.Option>
            <Select.Option value="secret">绝密</Select.Option>
          </Select>
        </Form.Item>

        <Form.Item label="优先级（1-10）" name="priority">
          <InputNumber min={1} max={10} style={{ width: '100%' }} />
        </Form.Item>

        <Form.Item>
          <Button type="primary" htmlType="submit" loading={loading} size="large">
            提交需求
          </Button>
          <Button style={{ marginLeft: 8 }} onClick={() => navigate('/demands')}>
            取消
          </Button>
        </Form.Item>
      </Form>
    </Card>
  );
};

export default DemandCreate;
