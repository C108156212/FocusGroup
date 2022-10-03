import React from "react";
import { Result, Button } from "antd";
import { Link } from "react-router-dom";

const NotFound = () => {
  return (
    <Result
      status="404"
      title="抱歉，頁面不存在!"
      extra={
        <Link to="/">
          <Button type="primary">回首頁</Button>
        </Link>
      }
    />
  );
};

export default NotFound;
