import React, { useState, useEffect } from "react";
import { Line } from "react-chartjs-2";
import Chart from "chart.js/auto";

function IssuesPerEventAnalysis({ issues }) {
  const [chartData, setChartData] = useState(null);

  useEffect(() => {
    if (issues && issues.length > 0) {
      const eventCountsPerIssue = [];

      issues.forEach((issue) => {
        const count = issue.events ? issue.events.length : 0;
        eventCountsPerIssue.push(count);
      });

      const categories = ["0", "1-5", "6-10", "11-15", "16-20", "21+"];
      const categorizedCounts = {
        0: 0,
        "1-5": 0,
        "6-10": 0,
        "11-15": 0,
        "16-20": 0,
        "21+": 0,
      };

      eventCountsPerIssue.forEach((count) => {
        if (count === 0) {
          categorizedCounts["0"]++;
        } else if (count >= 1 && count <= 5) {
          categorizedCounts["1-5"]++;
        } else if (count >= 6 && count <= 10) {
          categorizedCounts["6-10"]++;
        } else if (count >= 11 && count <= 15) {
          categorizedCounts["11-15"]++;
        } else if (count >= 16 && count <= 20) {
          categorizedCounts["16-20"]++;
        } else {
          categorizedCounts["21+"]++;
        }
      });

      const categoriesOrdered = ["0", "1-5", "6-10", "11-15", "16-20", "21+"]; // order
      const counts = categoriesOrdered.map(
        (category) => categorizedCounts[category]
      );

      setChartData({
        labels: categoriesOrdered,
        datasets: [
          {
            label: "Number of Issues",
            data: counts,
            backgroundColor: "rgba(54, 162, 235, 0.5)",
            borderColor: "rgba(54, 162, 235, 1)",
            borderWidth: 1,
            fill: false,
            tension: 0.4,
          },
        ],
      });
    }
  }, [issues]);

  if (!chartData) {
    return <div>Loading Issues per Event Analysis...</div>;
  }

  return (
    <div className="event-analysis-container">
      <Line data={chartData} />
    </div>
  );
}

export default IssuesPerEventAnalysis;
