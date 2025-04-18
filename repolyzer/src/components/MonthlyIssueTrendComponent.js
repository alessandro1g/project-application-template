import React, { useState, useEffect } from "react";
import { Line } from "react-chartjs-2";
import Chart from "chart.js/auto";

function MonthlyIssueTrendComponent({ issues }) {
  const [monthlyTrendData, setMonthlyTrendData] = useState(null);

  useEffect(() => {
    if (issues && issues.length > 0) {
      const monthlyCounts = issues.reduce((acc, issue) => {
        if (issue.created_date) {
          const date = new Date(issue.created_date);
          const monthYear = `${date.getFullYear()}-${String(
            date.getMonth() + 1
          ).padStart(2, "0")}`;
          acc[monthYear] = (acc[monthYear] || 0) + 1;
        }
        return acc;
      }, {});

      const sortedMonths = Object.keys(monthlyCounts).sort();
      const data = sortedMonths.map((month) => monthlyCounts[month]);

      setMonthlyTrendData({
        labels: sortedMonths,
        datasets: [
          {
            label: "Issues Created Monthly",
            data: data,
            fill: false,
            borderColor: "rgb(54, 162, 235)",
            tension: 0.1,
          },
        ],
      });
    }
  }, [issues]);

  if (!monthlyTrendData) {
    return <div>Loading Monthly Issue Trend...</div>;
  }

  return (
    <div className="monthly-trend-container">
      <Line data={monthlyTrendData} />
    </div>
  );
}

export default MonthlyIssueTrendComponent;
