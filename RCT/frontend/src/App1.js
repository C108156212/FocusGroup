import React, { useState } from "react";
import { Badge, Layout, Menu, Breadcrumb, notification } from "antd";
import { todos as initTodos } from "./data";
import "antd/dist/antd.css";
import { Link, Route, Switch, withRouter } from "react-router-dom";
import { HomeOutlined } from "@ant-design/icons";
import Home from "./Home";
import TodoList from "./TodoList";
import NotFound from "./NotFound";

const App = (props) => {
  const { location } = props;
  const [todos, setTodos] = useState(initTodos);

  const isAnyUncompletedTodoExist = todos.some((todo) => !todo.completed);

  const items = [
    { key: "/", label: <Link to="/">首頁</Link> },
    {
      key: "/todos",
      label: (
        <>
          <Link to="/todos">我的待辦</Link>
          <Badge dot={isAnyUncompletedTodoExist} offset={[6, 0]} />
        </>
      ),
    },
  ];

  const getBreadcrumbItem = () => {
    switch (location.pathname) {
      case "/":
        return <Breadcrumb.Item>首頁</Breadcrumb.Item>;
      case "/todos":
        return <Breadcrumb.Item>我的待辦</Breadcrumb.Item>;
      default:
        return null;
    }
  };

  const handleCompleteChange = (id, isCompleted) => {
    const newTodos = todos.map((todo) => {
      return todo.id === id ? { ...todo, completed: isCompleted } : todo;
    });

    setTodos(newTodos);
  };

  const handleAddTodo = (todo) => {
    setTodos((preTodos) => [
      ...preTodos,
      {
        id: preTodos[preTodos.length - 1].id + 1,
        ...todo,
      },
    ]);

    notification.success({
      message: "通知",
      description: "新增待辦成功",
      duration: 2,
      placemen: "topLeft",
    });
  };

  return (
    <Layout style={{ minHeight: "100vh" }}>
      <Layout.Header style={{ color: "#FFF" }}>
        <h1 style={{ float: "left", color: "#FFF", fontWeight: "700" }}>
          Todo System
        </h1>
        <Menu
          theme="dark"
          mode="horizontal"
          selectedKeys={[location.pathname]}
          style={{ float: "right" }}
          items={items}
        />
      </Layout.Header>
      <Layout.Content style={{ border: "1px solid black", padding: "32px" }}>
        <Breadcrumb>
          <Breadcrumb.Item>
            <Link to="/">
              <HomeOutlined />
            </Link>
          </Breadcrumb.Item>
          {getBreadcrumbItem()}
        </Breadcrumb>
        <div
          style={{ backgroundColor: "FFF", padding: "10px", marginTop: "10px" }}
        >
          <Switch>
            <Route path="/" exact>
              <Home todos={todos} />
            </Route>
            <Route path="/todos">
              {" "}
              <TodoList
                todos={todos}
                onCompleteChange={handleCompleteChange}
                onAddTodo={handleAddTodo}
              />
            </Route>
            <Route>
              <NotFound />
            </Route>
          </Switch>
        </div>
      </Layout.Content>
      <Layout.Footer style={{ textAlign: "center" }}>
        Copyright © 2022 Handsome Boyz All rights reserved
      </Layout.Footer>
    </Layout>
  );
};

export default withRouter(App);
