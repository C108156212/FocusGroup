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

// @mui material components
import Grid from "@mui/material/Grid";
import Card from "@mui/material/Card";

// Material Dashboard 2 React components
import MDBox from "components/MDBox";
import MDTypography from "components/MDTypography";

// Material Dashboard 2 React example components
import DashboardLayout from "examples/LayoutContainers/DashboardLayout";
import DashboardNavbar from "examples/Navbars/DashboardNavbar";
import ReportsLineChart from "examples/Charts/LineCharts/ReportsLineChart";
import ComplexStatisticsCard from "examples/Cards/StatisticsCards/ComplexStatisticsCard";
import DataTable from "examples/Tables/DataTable";

// Data
import newsCommentData from "layouts/tables/data/newsCommentData";

import React, { useState, useEffect } from "react";

function Dashboard() {
  const { columns, rows } = newsCommentData();

  const [Data, setData] = useState({
    CommentCount: 0,
    CommentAmount: "+0",
    CommentLabel: "none",
    PositiveCount: 0,
    PositiveAmount: "+0",
    PositiveLabel: "none",
    NegativeCount: 0,
    NegativeAmount: "+0",
    NegativeLabel: "none",
    NeutralCount: 0,
    NeutralAmount: "+0",
    NeutralLabel: "none",
    ChartDescription: "none",
    ChartDate: "none",
    ChartData: {
      labels: ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
      datasets: { label: "Pos: 0 Neg: 0 Neu: 0 Total", data: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] },
    },
  });

  useEffect(() => {
    fetch("/dashboard").then((res) =>
      res.json().then((data) => {
        setData({
          CommentCount: data.KeySearch.CommentCount,
          CommentAmount: data.KeySearch.CommentAmount,
          CommentLabel: data.KeySearch.CommentLabel,
          PositiveCount: data.KeySearch.PositiveCount,
          PositiveAmount: data.KeySearch.PositiveAmount,
          PositiveLabel: data.KeySearch.PositiveLabel,
          NegativeCount: data.KeySearch.NegativeCount,
          NegativeAmount: data.KeySearch.NegativeAmount,
          NegativeLabel: data.KeySearch.NegativeLabel,
          NeutralCount: data.KeySearch.NeutralCount,
          NeutralAmount: data.KeySearch.NeutralAmount,
          NeutralLabel: data.KeySearch.NeutralLabel,
          ChartDescription: data.KeySearch.ChartDescription,
          ChartDate: data.KeySearch.ChartDate,
          ChartData: data.KeySearch.ChartData,
        });
      })
    );
  }, []);

  return (
    <DashboardLayout>
      <DashboardNavbar />
      <MDBox py={3}>
        <Grid container spacing={3}>
          <Grid item xs={12} md={6} lg={3}>
            <MDBox mb={1.5}>
              <ComplexStatisticsCard
                color="dark"
                icon="leaderboard"
                title="討論數總計"
                count={`${Data.CommentCount} 則`}
                percentage={{
                  color: "success",
                  amount: Data.CommentAmount,
                  label: Data.CommentLabel,
                }}
              />
            </MDBox>
          </Grid>
          <Grid item xs={12} md={6} lg={3}>
            <MDBox mb={1.5}>
              <ComplexStatisticsCard
                color="info"
                icon="leaderboard"
                title="正面回應數"
                count={`${Data.PositiveCount} 則`}
                percentage={{
                  color: "success",
                  amount: Data.PositiveAmount,
                  label: Data.PositiveLabel,
                }}
              />
            </MDBox>
          </Grid>
          <Grid item xs={12} md={6} lg={3}>
            <MDBox mb={1.5}>
              <ComplexStatisticsCard
                color="primary"
                icon="leaderboard"
                title="負面回應數"
                count={`${Data.NegativeCount} 則`}
                percentage={{
                  color: "success",
                  amount: Data.NegativeAmount,
                  label: Data.NegativeLabel,
                }}
              />
            </MDBox>
          </Grid>
          <Grid item xs={12} md={6} lg={3}>
            <MDBox mb={1.5}>
              <ComplexStatisticsCard
                color="success"
                icon="leaderboard"
                title="中立回應數"
                count={`${Data.NeutralCount} 則`}
                percentage={{
                  color: "success",
                  amount: Data.NeutralAmount,
                  label: Data.NeutralLabel,
                }}
              />
            </MDBox>
          </Grid>
        </Grid>
        <MDBox mt={4.5}>
          <Grid container spacing={6}>
            <Grid item xs={12} md={6} lg={8}>
              <MDBox mb={3}>
                <ReportsLineChart
                  color="warning"
                  title="討論熱度趨勢"
                  description={Data.ChartDescription}
                  date={Data.ChartDate}
                  chart={Data.ChartData}
                />
              </MDBox>
            </Grid>
            <Grid item xs={12} lg={4}>
              <Card>
                <MDBox
                  mx={2}
                  mt={-3}
                  py={3}
                  px={2}
                  variant="gradient"
                  bgColor="info"
                  borderRadius="lg"
                  coloredShadow="info"
                >
                  <MDTypography variant="h6" color="white">
                    最新評論
                  </MDTypography>
                </MDBox>
                <MDBox pt={3}>
                  <Grid container spacing={3}>
                    <DataTable
                      table={{ columns, rows }}
                      isSorted={false}
                      entriesPerPage={false}
                      showTotalEntries={false}
                      noEndBorder
                    />
                  </Grid>
                </MDBox>
              </Card>
            </Grid>
          </Grid>
        </MDBox>
      </MDBox>
    </DashboardLayout>
  );
}

export default Dashboard;
