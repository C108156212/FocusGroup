import React, { useState } from "react";
import { Layout, Menu, Breadcrumb, Row, Col } from "antd";
import { HomeOutlined } from "@ant-design/icons";
import { Link, Route, Switch, withRouter } from "react-router-dom";
import "antd/dist/antd.css";
import NotFound from "./NotFound";
import ManageUser from "./ManageUser";
import ManageSpace from "./ManageSpace";
import OpenDoorRecord from "./OpenDoorRecord";
import ManageQuestion from "./ManageQuestion";
import Login from "./Login";

const items = [
  { key: "/", label: <Link to="/">各空間管理</Link> },
  {
    key: "/manageuser",
    label: (
      <>
        <Link to="/manageuser">使用者管理</Link>
        {/* <Badge dot={isAnyUncompletedTodoExist} offset={[6, 0]} /> */}
      </>
    ),
  },
  {
    key: "/opendoorrecord",
    label: (
      <>
        <Link to="/opendoorrecord">開門紀錄</Link>
        {/* <Badge dot={isAnyUncompletedTodoExist} offset={[6, 0]} /> */}
      </>
    ),
  },
  {
    key: "/managequestion",
    label: (
      <>
        <Link to="/managequestion">問題回饋管理</Link>
        {/* <Badge dot={isAnyUncompletedTodoExist} offset={[6, 0]} /> */}
      </>
    ),
  },
];

const App = (props) => {
  const { location } = props;

  const getBreadcrumbItem = () => {
    switch (location.pathname) {
      case "/":
        return <Breadcrumb.Item>各空間管理</Breadcrumb.Item>;
      case "/manageuser":
        return <Breadcrumb.Item>使用者管理</Breadcrumb.Item>;
      case "/opendoorrecord":
        return <Breadcrumb.Item>開門紀錄</Breadcrumb.Item>;
      case "/managequestion":
        return <Breadcrumb.Item>問題回饋管理</Breadcrumb.Item>;
      default:
        return null;
    }
  };

  const doLogin = () => {
    setDologin(false);
  };

  const doLogout = () => {
    setDologin(true);
  };

  const [dologin, setDologin] = useState(false);

  return dologin ? (
    <Login doLogin={doLogin} />
  ) : (
    <Layout style={{ minHeight: "100vh" }}>
      <Layout.Header style={{ color: "#FFF" }}>
        <h1 style={{ float: "left", color: "#FFF", fontWeight: "700" }}>
          門禁管理系統
        </h1>
        <div style={{ float: "right" }}>
          <a onClick={doLogout}>登出</a>
        </div>
      </Layout.Header>
      <Layout className="site-layout-background">
        <Layout.Sider className="site-layout-background" width={160}>
          <Menu
            mode="inline"
            defaultSelectedKeys={["1"]}
            defaultOpenKeys={["sub1"]}
            selectedKeys={[location.pathname]}
            style={{
              height: "100%",
            }}
            items={items}
          />
        </Layout.Sider>
        <Layout.Content style={{ padding: "12px" }}>
          <Breadcrumb>
            <Breadcrumb.Item>
              <Link to="/">
                <HomeOutlined />
              </Link>
            </Breadcrumb.Item>
            {getBreadcrumbItem()}
          </Breadcrumb>
          <Switch>
            <Route path="/" exact>
              <ManageSpace />
            </Route>
            <Route path="/manageuser">
              <ManageUser />
            </Route>
            <Route path="/opendoorrecord">
              <OpenDoorRecord />
            </Route>
            <Route path="/managequestion">
              <ManageQuestion />
            </Route>
            <Route>
              <NotFound />
            </Route>
          </Switch>
        </Layout.Content>
      </Layout>
      <Layout.Footer style={{ textAlign: "center" }}>
        Copyright © 2022 門禁管理系統 reserved
      </Layout.Footer>
    </Layout>
  );
};

export default withRouter(App);
