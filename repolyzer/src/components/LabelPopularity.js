import React, { useState, useEffect } from "react";
import { Bar } from "react-chartjs-2";
import Chart from "chart.js/auto";

function LabelPopularity({ issues }) {
  const [labelData, setLabelData] = useState(null);

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

      const sortedLabels = Object.keys(labelCounts)
        .sort((a, b) => labelCounts[b] - labelCounts[a])
        .slice(0, 10);
      const data = sortedLabels.map((label) => labelCounts[label]);

      setLabelData({
        labels: sortedLabels,
        datasets: [
          {
            label: "Label Popularity (Top 10)",
            data: data,
            backgroundColor: "rgba(255, 99, 132, 0.5)",
            borderColor: "rgba(255, 99, 132, 1)",
            borderWidth: 1,
          },
        ],
      });
    }
  }, [issues]);

  if (!labelData) {
    return <div>Loading Label Popularity...</div>;
  }

  return (
    <div className="label-popularity-container">
      <Bar data={labelData} />
    </div>
  );
}

export default LabelPopularity;
