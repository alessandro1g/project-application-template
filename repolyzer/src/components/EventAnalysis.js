import React, { useState, useEffect } from "react";
import { Bar } from "react-chartjs-2";
import Chart from "chart.js/auto";
import { parseISO, isValid } from "date-fns";

function EventAnalysis({ issues }) {
  const [eventData, setEventData] = useState(null);

  useEffect(() => {
    if (issues && issues.length > 0) {
      const dateEventMap = {};

      issues.forEach((issue) => {
        if (issue.events) {
          issue.events.forEach((event) => {
            if (event.event_date && event.event_date !== "N/A 255") {
              const eventTime = parseISO(event.event_date);
              if (isValid(eventTime)) {
                const dateKey = eventTime.toISOString().slice(0, 10);
                dateEventMap[dateKey] = (dateEventMap[dateKey] || 0) + 1;
              } else {
                console.error("Invalid date:", event.event_date);
              }
            }
          });
        }
      });

      const labels = Object.keys(dateEventMap).sort();
      const data = labels.map((date) => dateEventMap[date]);

      setEventData({
        labels: labels,
        datasets: [
          {
            label: "Event Count",
            data: data,
            backgroundColor: "rgba(54, 162, 235, 0.5)",
            borderColor: "rgba(54, 162, 235, 1)",
            borderWidth: 1,
          },
        ],
      });
    }
  }, [issues]);

  if (!eventData) {
    return <div>Loading Event Analysis...</div>;
  }

  return (
    <div className="event-analysis-container">
      <Bar data={eventData} />
    </div>
  );
}

export default EventAnalysis;
