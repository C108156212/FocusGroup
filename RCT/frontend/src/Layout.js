import {
  UploadOutlined,
  UserOutlined,
  VideoCameraOutlined,
  AccountBookOutlined,
} from "@ant-design/icons";
import { Link, Route, Switch, withRouter } from "react-router-dom";
import { Layout, Menu } from "antd";
import React from "react";
import "./layout.css";
import FrontPage from "./FrontPage";
import ProductA from "./ProductA";
import ProductB from "./ProductB";
import ProductC from "./ProductC";
import ProductD from "./ProductD";
import ProductE from "./ProductE";
import ProductF from "./ProductF";
import "antd/dist/antd.css";
const { Header, Content, Footer, Sider } = Layout;

const items = [
  { key: "/", label: <Link to="/">首頁</Link> },
  { key: "/productA", label: <Link to="/productA">產品A</Link> },
  {
    key: "/productB",
    label: <Link to="/productB">產品B</Link>,
  },
  {
    key: "/productC",
    label: <Link to="/productC">產品C</Link>,
  },
  {
    key: "/productD",
    label: <Link to="/productD">產品D</Link>,
  },
  {
    key: "/productE",
    label: <Link to="/productE">產品E</Link>,
  },
  {
    key: "/productF",
    label: <Link to="/productF">產品F</Link>,
  },
];

const App = () => (
  <Layout>
    <Sider
      breakpoint="lg"
      collapsedWidth="0"
      onBreakpoint={(broken) => {
        console.log(broken);
      }}
      onCollapse={(collapsed, type) => {
        console.log(collapsed, type);
      }}
    >
      <div className="logo" />
      <Menu
        theme="dark"
        mode="inline"
        defaultSelectedKeys={["4"]}
        items={items}
        style={{ height: "100%" }}
      />
    </Sider>
    <Layout>
      <Header
        className="site-layout-sub-header-background"
        style={{
          padding: 0,
        }}
      />
      <Content
        style={{
          margin: "24px 16px 0",
          height: "100%",
        }}
      >
        <Switch>
          <Route path="/" exact>
            <FrontPage />
          </Route>
          <Route path="/productA">
            <ProductA />
          </Route>
          <Route path="/productB">
            <ProductB />
          </Route>
          <Route path="/productC">
            <ProductC />
          </Route>
          <Route path="/productD">
            <ProductD />
          </Route>
          <Route path="/productE">
            <ProductE />
          </Route>
          <Route path="/productF">
            <ProductF />
          </Route>
          <Route>{/* <NotFound /> */}</Route>
        </Switch>
      </Content>
      <Footer
        style={{
          textAlign: "center",
        }}
      >
        Ant Design ©2018 Created by Ant UED
      </Footer>
    </Layout>
  </Layout>
);

export default withRouter(App);
