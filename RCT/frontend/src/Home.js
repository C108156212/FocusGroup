import React from "react";
import { Button, Badge } from "antd";

const Home = (props) => {
  const { todos } = props;

  const getMonthTodos = (value) => {
    return todos.filter(
      (todo) =>
        todo.expiredDate.isSame(value, "year") &&
        todo.expiredDate.isSame(value, "month")
    );
  };

  const monthCellRender = (value) => {
    const monthTodos = getMonthTodos(value);
    return renderTodoItem(monthTodos);
  };

  const getDayTodos = (value) => {
    return todos.filter((todo) => todo.expiredDate.isSame(value, "day"));
  };

  const dateCellRender = (value) => {
    const dayTodos = getDayTodos(value);
    return renderTodoItem(dayTodos);
  };

  const renderTodoItem = (todos) => {
    return (
      <ul style={{ listStyle: "none" }}>
        {todos.map((todo) => (
          <li key={todo.id}>
            <Badge status="warning" text={todo.title} />
          </li>
        ))}
      </ul>
    );
  };

  return (
    <div>
      <Button type="primary">Primary Button</Button>
      {/* <Calendar
        dateCellRender={dateCellRender}
        monthCellRender={monthCellRender}
      ></Calendar> */}
    </div>
  );
};

export default Home;
