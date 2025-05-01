import React, { useState, useEffect } from "react";
import { Line } from "react-chartjs-2";
import Chart from "chart.js/auto";

function IssueCreationTrendYears({ issues }) {
  const [issueTrendData, setIssueTrendData] = useState(null);

  useEffect(() => {
    if (issues && issues.length > 0) {
      const yearlyCounts = issues.reduce((acc, issue) => {
        if (issue.created_date) {
          const year = new Date(issue.created_date).getFullYear();
          acc[year] = (acc[year] || 0) + 1;
        }
        return acc;
      }, {});

      const years = Object.keys(yearlyCounts).sort();
      const counts = years.map((year) => yearlyCounts[year]);

      setIssueTrendData({
        labels: years,
        datasets: [
          {
            label: "Issues Created",
            data: counts,
            fill: false,
            borderColor: "rgb(75, 192, 192)",
            tension: 0.4,
          },
        ],
      });
    }
  }, [issues]);

  if (!issueTrendData) {
    return <div>Loading Issue Creation Trend (Years)...</div>;
  }

  return (
    <div className="issue-trend-years-container">
      <Line data={issueTrendData} />
    </div>
  );
}

export default IssueCreationTrendYears;
