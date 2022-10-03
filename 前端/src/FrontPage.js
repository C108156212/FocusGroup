import React, { useState } from "react";
import {
  Layout,
  Button,
  Row,
  Col,
  Card,
  Image,
  Checkbox,
  Form,
  Input,
} from "antd";
import Register from "./LogIn";
import "antd/dist/antd.css";

const App = (props) => {
  return (
    <Layout style={{ minHeight: "100vh" }}>
      <div className="site-card-wrapper">
        <Row gutter={24}>
          <Col span={12}>
            <Card title="目前最熱產品" bordered={false}>
              <Image
                width={200}
                src="https://zos.alipayobjects.com/rmsportal/jkjgkEfvpUPVyRjUImniVslZfWPnJuuZ.png"
              />
            </Card>
          </Col>
          <Col span={12}>
            <Card title="討論最多產品優點前三名" bordered={false}>
              <Image
                width={200}
                src="https://zos.alipayobjects.com/rmsportal/jkjgkEfvpUPVyRjUImniVslZfWPnJuuZ.png"
              />
            </Card>
          </Col>
        </Row>
        <Row gutter={24}>
          <Col span={12}>
            <Card title="產品熱度前三名" bordered={false}>
              <Image
                width={200}
                src="https://zos.alipayobjects.com/rmsportal/jkjgkEfvpUPVyRjUImniVslZfWPnJuuZ.png"
              />
            </Card>
          </Col>
          <Col span={12}>
            <Card title="討論最多產品缺點前三名" bordered={false}>
              <Image
                width={200}
                src="https://zos.alipayobjects.com/rmsportal/jkjgkEfvpUPVyRjUImniVslZfWPnJuuZ.png"
              />
            </Card>
          </Col>
        </Row>
      </div>
    </Layout>
  );
};

export default App;
