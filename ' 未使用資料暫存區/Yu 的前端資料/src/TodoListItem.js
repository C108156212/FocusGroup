import React from "react";
import { Card, Tag, Checkbox } from "antd";
import { FieldTimeOutlined } from "@ant-design/icons";
import moment from "moment";

const TodoListItem = (props) => {
  const { todo, onCompleteChange } = props;
  const { id, completed, title, description, expiredDate } = todo;
  return (
    <Card
      title={
        <span style={{ display: "flex" }}>
          <Checkbox
            onChange={() => {
              onCompleteChange(id, !completed);
            }}
            checked={completed}
          />
          <span
            style={{
              whiteSpace: "pre-wrap",
              textDecoration: completed ? "line-through" : "none",
              marginLeft: "6px",
            }}
          >
            {title}
          </span>
        </span>
      }
      extra={
        <Tag color={completed ? "blue" : "orange"}>
          {completed ? "完成" : "未完成"}
        </Tag>
      }
    >
      <div>
        <div
          style={{
            textDecoration: completed ? "line-through" : "none",
            marginBottom: "20px",
            wordWrap: "break-word",
          }}
        >
          {description}
        </div>
        <div style={{ color: "#AEAEAE" }}>
          <FieldTimeOutlined style={{ marginRight: "3px" }} />
          {moment(expiredDate).format("YYYY-MM-DD hh:mm")}
        </div>
      </div>
    </Card>
  );
};

export default TodoListItem;
