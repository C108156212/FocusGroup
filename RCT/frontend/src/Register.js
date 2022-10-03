import { Button, Form, Input, Layout, Select } from "antd";
import React from "react";
import "antd/dist/antd.css";
const { Header } = Layout;
const { Option } = Select;

const layout = {
  labelCol: {
    span: 8,
  },
  wrapperCol: {
    span: 8,
  },
};
/* eslint-disable no-template-curly-in-string */

const validateMessages = {
  required: "${label} is required!",
  types: {
    email: "${label}不是有效的電子信箱！",
  },
};
/* eslint-enable no-template-curly-in-string */

const App = () => {
  const onFinish = (values) => {
    console.log(values);
  };
  const prefixSelector = (
    <Form.Item name="prefix" noStyle>
      <Select
        style={{
          width: 70,
        }}
      >
        <Option value="02">+02</Option>
        <Option value="03">+03</Option>
        <Option value="037">+037</Option>
        <Option value="04">+04</Option>
        <Option value="049">+49</Option>
        <Option value="05">+05</Option>
        <Option value="06">+06</Option>
        <Option value="07">+07</Option>
        <Option value="08">+08</Option>
        <Option value="089">+089</Option>
        <Option value="082">+082</Option>
        <Option value="0826">+0826</Option>
        <Option value="0836">+0836</Option>
      </Select>
    </Form.Item>
  );
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
        {...layout}
        name="nest-messages"
        onFinish={onFinish}
        validateMessages={validateMessages}
      >
        <Form.Item
          name={"account"}
          label="帳號"
          rules={[
            {
              required: true,
            },
          ]}
        >
          <Input />
        </Form.Item>
        <Form.Item
          name={"password"}
          label="密碼"
          rules={[
            {
              required: true,
            },
          ]}
        >
          <Input.Password />
        </Form.Item>
        <Form.Item
          name="confirm"
          label="確認密碼"
          dependencies={["password"]}
          hasFeedback
          rules={[
            {
              required: true,
              message: "請確認您的密碼！",
            },
            ({ getFieldValue }) => ({
              validator(_, value) {
                if (!value || getFieldValue("password") === value) {
                  return Promise.resolve();
                }

                return Promise.reject(new Error("您輸入的兩個密碼不一致！"));
              },
            }),
          ]}
        >
          <Input.Password />
        </Form.Item>
        <Form.Item
          name="name"
          label="公司名稱"
          rules={[
            {
              required: true,
              message: "請輸入您的公司名稱！",
              whitespace: true,
            },
          ]}
        >
          <Input />
        </Form.Item>
        <Form.Item
          name="email"
          label="電子信箱"
          rules={[
            {
              type: "email",
              message: "此為無效的電子信箱！",
            },
            {
              required: true,
              message: "請輸入您的電子信箱！",
            },
          ]}
        >
          <Input />
        </Form.Item>
        <Form.Item name="phone" label="公司市話">
          <Input
            addonBefore={prefixSelector}
            style={{
              width: "100%",
            }}
          />
        </Form.Item>

        <Form.Item wrapperCol={{ ...layout.wrapperCol, offset: 8 }}>
          <Button type="primary" htmlType="submit">
            註冊
          </Button>
        </Form.Item>
      </Form>
    </div>
  );
};

export default App;
