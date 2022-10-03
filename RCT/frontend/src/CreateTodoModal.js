import React, { useEffect } from "react";
import { Input, Switch, Form, Modal, DatePicker } from "antd";
import moment from "moment";

const CreateTodoModal = (props) => {
  const { visible, onAddTodo, onCancel } = props;

  const [form] = Form.useForm();

  useEffect(() => {
    return () => {
      if (visible) {
        form.resetFields();
      }
    };
  }, [visible, form]);

  const handleAddTodo = (e) => {
    e.preventDefault();
    form.validateFields().then((values) => {
      onAddTodo({ ...values });
    });
  };

  return (
    <Modal
      title="新增待辦"
      visible={visible}
      okText="存檔"
      cancelText="取消"
      onOk={handleAddTodo}
      onCancel={onCancel}
      destroyOnClose={true}
    >
      <Form
        name="todo-form"
        form={form}
        labelCol={{ span: 4 }}
        wrapperCol={{ spane: 20 }}
        initialValues={{ expiredDate: moment(), completed: false }}
      >
        <Form.Item
          label="標題"
          name="title"
          hasFeedback
          rules={[
            { required: true, message: "請填寫標題" },
            { max: 20, message: "字串長度不可超過 20 字元" },
          ]}
        >
          <Input />
        </Form.Item>
        <Form.Item
          label="描述"
          name="description"
          rules={[{ required: true, message: "請填寫描述" }]}
          hasFeedback
        >
          <Input.TextArea />
        </Form.Item>
        <Form.Item
          label="到期日"
          name="expiredDate"
          rules={[{ required: true, message: "請選擇到期日" }]}
          hasFeedback
        >
          <DatePicker
            showTime={{ format: "HH:mm" }}
            format="YYYY-MM-DD HH:mm"
          />
        </Form.Item>
        <Form.Item
          label="完成"
          name="completed"
          valuePropName="checked"
          ruels={[{ required: true }]}
        >
          <Switch checkedChildren="是" unCheckedChildren="否" />
        </Form.Item>
      </Form>
    </Modal>
  );
};

export default CreateTodoModal;
