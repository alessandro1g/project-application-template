import React, { useState, useEffect } from "react";
import { Pie } from "react-chartjs-2";
import Chart from "chart.js/auto";

function OpenIssuesByCreator({ issues }) {
  const [creatorData, setCreatorData] = useState(null);

  useEffect(() => {
    if (issues && issues.length > 0) {
      const creatorCounts = issues.reduce((acc, issue) => {
        if (issue.state === "open" && issue.creator) {
          acc[issue.creator] = (acc[issue.creator] || 0) + 1;
        }
        return acc;
      }, {});

      const sortedCreators = Object.keys(creatorCounts)
        .sort((a, b) => creatorCounts[b] - creatorCounts[a])
        .slice(0, 10);
      const data = sortedCreators.map((creator) => creatorCounts[creator]);
      const backgroundColors = sortedCreators.map(
        () => `#${Math.floor(Math.random() * 16777215).toString(16)}`
      );

      setCreatorData({
        labels: sortedCreators,
        datasets: [
          {
            data: data,
            backgroundColor: backgroundColors,
            hoverOffset: 4,
          },
        ],
      });
    }
  }, [issues]);

  if (!creatorData) {
    return <div>Loading Open Issues by Creator...</div>;
  }

  return (
    <div className="open-issues-by-creator-container">
      <Pie data={creatorData} />
    </div>
  );
}

export default OpenIssuesByCreator;
