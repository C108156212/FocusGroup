import React, { useState } from "react";
import { Layout, Button, Row, Col, Card, Image } from "antd";
import "antd/dist/antd.css";

const App = (props) => {
  return (
    <Layout style={{ minHeight: "100vh" }}>
      <Layout.Header style={{ color: "#FFF" }}>
        <Row>
          <Col span={4}>
            <Button>梗概</Button>
          </Col>
          <Col span={5}>
            <Button>產品熱度</Button>
          </Col>
          <Col span={7}>
            <Button>產品優缺點討論百分比</Button>
          </Col>
          <Col span={5}>
            <Button>異常狀況</Button>
          </Col>
          <Col span={3}>
            <Button>設定</Button>
          </Col>
        </Row>
      </Layout.Header>
      <div className="site-card-wrapper">
        <Row gutter={24}>
          <Col span={12}>
            <Card title="產品F每日熱度" bordered={false}>
              <Image
                width={200}
                src="https://zos.alipayobjects.com/rmsportal/jkjgkEfvpUPVyRjUImniVslZfWPnJuuZ.png"
              />
            </Card>
          </Col>
          <Col span={12}>
            <Card title="產品F優缺點討論圓餅圖" bordered={false}>
              <Image
                width={200}
                src="https://zos.alipayobjects.com/rmsportal/jkjgkEfvpUPVyRjUImniVslZfWPnJuuZ.png"
              />
            </Card>
          </Col>
        </Row>
        <Row gutter={24}>
          <Col span={8}>
            <Card title="異常狀況回報" bordered={false}>
              <Image
                width={200}
                src="https://zos.alipayobjects.com/rmsportal/jkjgkEfvpUPVyRjUImniVslZfWPnJuuZ.png"
              />
            </Card>
          </Col>
          <Col span={8}>
            <Card title="討論最多產品優點前三名" bordered={false}>
              <Image
                width={200}
                src="https://zos.alipayobjects.com/rmsportal/jkjgkEfvpUPVyRjUImniVslZfWPnJuuZ.png"
              />
            </Card>
          </Col>
          <Col span={8}>
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
