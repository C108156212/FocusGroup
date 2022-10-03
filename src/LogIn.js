import { Button, Checkbox, Form, Input, Layout, Col, Row } from "antd";
import React from "react";
import "antd/dist/antd.css";
const { Header } = Layout;

const App = () => {
  const onFinish = (values) => {
    console.log("Success:", values);
  };

  const onFinishFailed = (errorInfo) => {
    console.log("Failed:", errorInfo);
  };

  return (
    <div>
      <Header
        className="site-layout-sub-header-background"
        style={{
          padding: 0,
        }}
      >
        <h2 style={{ float: "left", color: "#FFF", fontWeight: "700" }}>
          產品售後回饋與熱度分析系統
        </h2>
      </Header>
      <Form
        style={{ padding: "50px" }}
        name="basic"
        labelCol={{
          span: 8,
        }}
        wrapperCol={{
          span: 8,
        }}
        initialValues={{
          remember: true,
        }}
        onFinish={onFinish}
        onFinishFailed={onFinishFailed}
        autoComplete="off"
      >
        <Form.Item
          label="帳號"
          name="username"
          rules={[
            {
              required: true,
              message: "請輸入您的帳號！",
            },
          ]}
        >
          <Input />
        </Form.Item>

        <Form.Item
          label="密碼"
          name="password"
          rules={[
            {
              required: true,
              message: "請輸入您的密碼！",
            },
          ]}
        >
          <Input.Password />
        </Form.Item>

        <Form.Item
          name="remember"
          valuePropName="checked"
          wrapperCol={{
            offset: 8,
            span: 16,
          }}
        >
          <Checkbox>記住我的帳號</Checkbox>
        </Form.Item>

        <Form.Item
          wrapperCol={{
            offset: 8,
            span: 16,
          }}
        >
          <Button type="primary" htmlType="submit">
            登入
          </Button>
        </Form.Item>
      </Form>
    </div>
  );
};

export default App;
