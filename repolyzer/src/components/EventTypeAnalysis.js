import React, { useState, useEffect } from "react";
import { Line } from "react-chartjs-2";
import Chart from "chart.js/auto";

function EventTypeAnalysis({ issues }) {
  const [eventTypeData, setEventTypeData] = useState(null);

  useEffect(() => {
    if (issues && issues.length > 0) {
      const issueDict = {};
      issues.forEach((issue) => {
        if (issue.events) {
          issue.events.forEach((event) => {
            const eventTimeStr = event.event_date;
            if (eventTimeStr) {
              try {
                const eventTime = new Date(eventTimeStr);
                const monthYear = `${
                  eventTime.getMonth() + 1
                }-${eventTime.getFullYear()}`;
                if (!issueDict[monthYear]) {
                  issueDict[monthYear] = {};
                }
                issueDict[monthYear][event.event_type] =
                  (issueDict[monthYear][event.event_type] || 0) + 1;
              } catch (error) {
                console.error("Error parsing date:", error);
              }
            }
          });
        }
      });

      const months = Object.keys(issueDict).sort();
      const eventTypes = new Set();
      Object.values(issueDict).forEach((monthData) => {
        Object.keys(monthData).forEach((eventType) =>
          eventTypes.add(eventType)
        );
      });

      const datasets = Array.from(eventTypes).map((eventType) => {
        const counts = months.map(
          (month) => issueDict[month]?.[eventType] || 0
        );
        return {
          label: eventType,
          data: counts,
          fill: false,
          borderColor: `#${Math.floor(Math.random() * 16777215).toString(16)}`,
          tension: 0.1,
        };
      });

      setEventTypeData({
        labels: months,
        datasets: datasets,
      });
    }
  }, [issues]);

  if (!eventTypeData) {
    return <div>Loading Event Type Analysis...</div>;
  }

  return (
    <div className="event-type-container">
      {eventTypeData && <Line data={eventTypeData} />}
    </div>
  );
}

export default EventTypeAnalysis;
