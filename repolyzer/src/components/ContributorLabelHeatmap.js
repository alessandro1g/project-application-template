// src/components/ContributorLabelHeatmap.js
import React, { useState, useEffect } from "react";
import { HeatMap } from "@nivo/heatmap";

function ContributorLabelHeatmap({ issues }) {
  const [heatmapData, setHeatmapData] = useState(null);

  useEffect(() => {
    if (issues && issues.length > 0) {
      const creatorLabelPairs = [];
      issues.forEach((issue) => {
        if (issue.creator && issue.labels) {
          issue.labels.forEach((label) => {
            creatorLabelPairs.push({ creator: issue.creator, label: label });
          });
        }
      });

      if (creatorLabelPairs.length === 0) {
        console.log("No contributor-label data found.");
        return;
      }

      const creatorCounts = creatorLabelPairs.reduce((acc, { creator }) => {
        acc[creator] = (acc[creator] || 0) + 1;
        return acc;
      }, {});

      const topCreators = Object.entries(creatorCounts)
        .sort(([, countA], [, countB]) => countB - countA)
        .slice(0, 10)
        .map(([creator]) => creator);

      const filteredPairs = creatorLabelPairs.filter(({ creator }) =>
        topCreators.includes(creator)
      );

      const pivotedData = {};
      filteredPairs.forEach(({ creator, label }) => {
        if (!pivotedData[creator]) {
          pivotedData[creator] = {};
        }
        pivotedData[creator][label] = (pivotedData[creator][label] || 0) + 1;
      });

      const formattedData = topCreators.map((creator) => ({
        creator: creator,
        ...Object.entries(pivotedData[creator] || {}).reduce(
          (acc, [label, value]) => ({ ...acc, [label]: value }),
          {}
        ),
      }));

      setHeatmapData(formattedData);
    }
  }, [issues]);

  if (!heatmapData) {
    return <div>Loading Contributor vs Label Heatmap...</div>;
  }

  const keys = Object.keys(
    heatmapData.reduce((acc, row) => ({ ...acc, ...row }), {})
  ).filter((key) => key !== "creator");

  return (
    <div className="contributor-heatmap-container">
      <h2 className="contributor-heatmap-title">
        Top 10 Contributors vs Labels Heatmap
      </h2>
      <div style={{ height: "500px" }}>
        <HeatMap
          data={heatmapData}
          keys={keys}
          index="creator"
          margin={{ top: 60, right: 20, bottom: 60, left: 120 }}
          colors="YlGnBu"
          cellShape="rect"
          cellBorderWidth={1}
          cellBorderColor="#fff"
          tooltip={({ value, row, column }) => (
            <div>
              <strong>{row.creator}</strong> - <strong>{column}</strong>:{" "}
              {value}
            </div>
          )}
          legends={[
            {
              anchor: "bottom-right",
              direction: "row",
              translateY: 60,
              translateX: 20,
              itemWidth: 20,
              itemHeight: 14,
              itemsSpacing: 4,
              itemTextColor: "#999",
              symbolSize: 14,
              effects: [
                {
                  on: "hover",
                  style: {
                    itemTextColor: "#000",
                  },
                },
              ],
            },
          ]}
        />
      </div>
    </div>
  );
}

export default ContributorLabelHeatmap;
