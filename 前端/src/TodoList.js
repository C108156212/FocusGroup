import React, { useState } from "react";
import { Button, List, Radio, Input } from "antd";
import TodoListItem from "./TodoListItem";
import { PlusOutlined } from "@ant-design/icons";
import CreateTodoModal from "./CreateTodoModal";

const TodoList = (props) => {
  const { todos, onCompleteChange, onAddTodo } = props;
  const [queryType, setQueryType] = useState("all");
  const [showCreateModal, setShowCreateModal] = useState(false);

  const handleQueryTypeChange = (e) => {
    setQueryType(e.target.value);
  };

  const getTodos = () => {
    switch (queryType) {
      case "completed":
        return todos.filter((todo) => todo.completed);
      case "uncompleted":
        return todos.filter((todo) => !todo.completed);
      case "all":
      default:
        return todos;
    }
  };

  const handleOpenTodoModal = () => {
    setShowCreateModal(true);
  };

  const handleCancel = () => {
    setShowCreateModal(false);
  };

  const handleAddTodo = (todo) => {
    onAddTodo(todo);
    setShowCreateModal(false);
  };

  return (
    <div>
      <CreateTodoModal
        visible={showCreateModal}
        onAddTodo={handleAddTodo}
        onCancel={handleCancel}
      />
      <div style={{ margin: "10px 0px", display: "flex" }}>
        <Radio.Group
          value={queryType}
          buttonStyle="solid"
          onChange={handleQueryTypeChange}
        >
          <Radio.Button value="all">全部</Radio.Button>
          <Radio.Button value="completed">已完成</Radio.Button>
          <Radio.Button value="uncompleted">未完成</Radio.Button>
        </Radio.Group>
        <Button
          type="primary"
          icon={<PlusOutlined />}
          style={{ marginLeft: "auto" }}
          onClick={handleOpenTodoModal}
        >
          新增待辦
        </Button>
      </div>
      <List
        grid={{ gutter: 16, column: 4 }}
        dataSource={getTodos()}
        renderItem={(todo) => (
          <List.Item>
            <TodoListItem todo={todo} onCompleteChange={onCompleteChange} />
          </List.Item>
        )}
      />
    </div>
  );
};

export default TodoList;
