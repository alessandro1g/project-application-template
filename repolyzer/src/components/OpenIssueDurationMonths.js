import React, { useState, useEffect } from "react";
import { Bar } from "react-chartjs-2";
import Chart from "chart.js/auto";
import { differenceInMonths } from "date-fns";

function OpenIssueDurationMonths({ issues }) {
  const [durationData, setDurationData] = useState(null);

  useEffect(() => {
    if (issues && issues.length > 0) {
      const durations = issues
        .map((issue) => {
          if (issue.created_date) {
            const createdDate = new Date(issue.created_date);
            const closedDate = issue.closed_date
              ? new Date(issue.closed_date)
              : new Date();
            const duration = differenceInMonths(closedDate, createdDate);
            return duration;
          }
          return null;
        })
        .filter((duration) => duration !== null);

      const durationCounts = durations.reduce((acc, duration) => {
        acc[duration] = (acc[duration] || 0) + 1;
        return acc;
      }, {});

      const months = Object.keys(durationCounts).sort(
        (a, b) => parseInt(a) - parseInt(b)
      );
      const counts = months.map((month) => durationCounts[month]);

      setDurationData({
        labels: months,
        datasets: [
          {
            label: "Issue Duration (Months)",
            data: counts,
            backgroundColor: "rgba(153, 102, 255, 0.5)",
            borderColor: "rgba(153, 102, 255, 1)",
            borderWidth: 1,
          },
        ],
      });
    }
  }, [issues]);

  if (!durationData) {
    return <div>Loading Open Issue Duration (Months)...</div>;
  }

  return (
    <div className="issue-duration-container">
      <Bar data={durationData} />
    </div>
  );
}

export default OpenIssueDurationMonths;
