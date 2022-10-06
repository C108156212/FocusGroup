import React from "react";
import ReactDOM from "react-dom/client";
import App from "./Register";
import { BrowserRouter } from "react-router-dom";
import moment from "moment";
import "moment/locale/zh-tw";
import { ConfigProvider } from "antd";
import zhTW from "antd/es/locale/zh_TW";
moment.locale("zh-tw");

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(
  <BrowserRouter>
    <ConfigProvider locale={zhTW}>
      <App />
    </ConfigProvider>
  </BrowserRouter>
);
