import React, { useState, useEffect } from "react";
import { Bar } from "react-chartjs-2";
import Chart from "chart.js/auto";

function IssueCountByLabel({ issues }) {
  const [labelCountsData, setLabelCountsData] = useState(null);

  useEffect(() => {
    if (issues && issues.length > 0) {
      const labelCounts = issues.reduce((acc, issue) => {
        if (issue.labels) {
          issue.labels.forEach((label) => {
            acc[label] = (acc[label] || 0) + 1;
          });
        }
        return acc;
      }, {});

      const labels = Object.keys(labelCounts);
      const data = labels.map((label) => labelCounts[label]);

      setLabelCountsData({
        labels: labels,
        datasets: [
          {
            label: "Issue Count",
            data: data,
            backgroundColor: "rgba(255, 99, 132, 0.5)",
            borderColor: "rgba(255, 99, 132, 1)",
            borderWidth: 1,
          },
        ],
      });
    }
  }, [issues]);

  if (!labelCountsData) {
    return <div>Loading Issue Count by Label...</div>;
  }

  return (
    <div className="issue-label-count-container">
      <Bar data={labelCountsData} />
    </div>
  );
}

export default IssueCountByLabel;
