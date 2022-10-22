/* eslint-disable react/prop-types */
/* eslint-disable react/function-component-definition */
/**
=========================================================
* Material Dashboard 2 React - v2.1.0
=========================================================

* Product Page: https://www.creative-tim.com/product/material-dashboard-react
* Copyright 2022 Creative Tim (https://www.creative-tim.com)

Coded by www.creative-tim.com

 =========================================================

* The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
*/

// Material Dashboard 2 React components
import MDBox from "components/MDBox";
import MDTypography from "components/MDTypography";

import React, { useState, useEffect } from "react";

export default function getTableData() {
  const [Data, setData] = useState({
    ArticleTitle: [],
    ArticleURL: [],
    ArticleOrientation: [],
    CommentContent: [],
    CommentOrientation: [],
  });

  useEffect(() => {
    fetch("/dashboard").then((res) =>
      res.json().then((data) => {
        setData({
          ArticleTitle: data.NewsTable.ArticleTitle,
          ArticleURL: data.NewsTable.ArticleURL,
          ArticleOrientation: data.NewsTable.ArticleOrientation,
          CommentContent: data.NewsTable.CommentContent,
          CommentOrientation: data.NewsTable.CommentOrientation,
        });
      })
    );
  }, []);

  function getRowsList(num) {
    const list = [];
    for (let i = 0; i < num; i += 1) {
      list.push({
        article: (
          <MDBox lineHeight={1} textAlign="left">
            <MDTypography
              component="a"
              href={Data.ArticleURL[i]}
              display="block"
              variant="caption"
              color="text"
              fontWeight="medium"
            >
              {Data.ArticleTitle[i]}
            </MDTypography>
            <MDTypography variant="caption">{Data.ArticleOrientation[i]}</MDTypography>
          </MDBox>
        ),
        comment: (
          <MDTypography
            display="flex"
            variant="caption"
            color="text"
            fontWeight="medium"
            textAlign="left"
            width={200}
          >
            {Data.CommentContent[i]}
          </MDTypography>
        ),
        orientation: (
          <MDTypography display="flex" variant="caption" color="text" fontWeight="medium">
            {Data.CommentOrientation[i]}
          </MDTypography>
        ),
      });
    }
    return list;
  }

  return {
    columns: [
      { Header: "文章熱度", accessor: "article", width: "20%", align: "left" },
      { Header: "評論內容", accessor: "comment", width: "60%", align: "left" },
      { Header: "評論面向", accessor: "orientation", width: "20%", align: "center" },
    ],

    rows: getRowsList(10),
  };
}
