import React, { useState, useEffect } from "react";
import axios from "axios";
import "./App.css";
import EventAnalysis from "./components/EventAnalysis";
import LabelPopularity from "./components/LabelPopularity";
import MonthlyIssueTrendComponent from "./components/MonthlyIssueTrendComponent";
import EventTypeAnalysis from "./components/EventTypeAnalysis";
// import ContributorLabelHeatmap from "./components/ContributorLabelHeatmap";
import IssueCountByLabel from "./components/IssueCountByLabel";
import IssueCreationTrendYears from "./components/IssueCreationTrendYears";
import OpenIssueDurationMonths from "./components/OpenIssueDurationMonths";
import OpenIssuesByCreator from "./components/OpenIssuesByCreator";
import IssuesPerEventAnalysis from "./components/IssuesPerEventAnalysis"

const ChartItem = ({ children, title }) => {
  return (
    <div
      className={`chart-item`}
    >
      <h2 className="chart-title">{title}</h2>
      <div style={{ width: "100%", height: "100%" }}>{children}</div>
    </div>
  );
};

function App() {
  const [githubIssues, setGithubIssues] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get(
          "https://raw.githubusercontent.com/alessandro1g/project-application-template/refs/heads/main/github_issues.json"
        );
        setGithubIssues(response.data);
        setLoading(false);
      } catch (err) {
        setError(err);
        setLoading(false);
        console.error("Error fetching data:", err);
      }
    };

    fetchData();
  }, []);

  if (loading) {
    return <div className="loading-message">Loading GitHub Issues...</div>;
  }

  if (error) {
    return (
      <div className="error-message">
        Error loading GitHub Issues: {error.message}
      </div>
    );
  }

  return (
    <div className="app-container">
      <header className="header-bar">
        <div className="header-bar-left">
          <img
            src="logo_icon.png"
            alt="Reployzer Logo"
            className="header-bar-logo"
          />
          <span className="header-bar-name">Reployzer</span>
        </div>
        <div className="header-bar-right">
          <a
            href="https://github.com/alessandro1g/project-application-template/blob/main/README.md"
            target="_blank"
            rel="noopener noreferrer"
          >
            About
          </a>
        </div>
      </header>

      <div className="chart-grid-container">
        <div className="chart-grid">
          <ChartItem title="Event Analysis">
            <EventAnalysis issues={githubIssues} />
          </ChartItem>
          <ChartItem title="Label Popularity">
            <LabelPopularity issues={githubIssues} />
          </ChartItem>
          <ChartItem title="Monthly Issue Trend">
            <MonthlyIssueTrendComponent issues={githubIssues} />
          </ChartItem>
          <ChartItem title="Event Type Analysis">
            <EventTypeAnalysis issues={githubIssues} />
          </ChartItem>
          {/* <ChartItem title="Contributor Label Heatmap" >
            <ContributorLabelHeatmap issues={githubIssues} />
          </ChartItem> */}
          <ChartItem title="Issue Count By Label">
            <IssueCountByLabel issues={githubIssues} />
          </ChartItem>
          <ChartItem title="Issue Creation Trend (Years)">
            <IssueCreationTrendYears issues={githubIssues} />
          </ChartItem>
          <ChartItem title="Open Issue Duration (Months)">
            <OpenIssueDurationMonths issues={githubIssues} />
          </ChartItem>
          <ChartItem title="Open Issues by Creator">
            <OpenIssuesByCreator issues={githubIssues} />
          </ChartItem>
          <ChartItem title="Number of Issues per Event">
            <IssuesPerEventAnalysis issues={githubIssues} />
          </ChartItem>
        </div>
      </div>

      <footer className="footer-bar">
        <div className="footer-left">
          <span className="footer-right">
            Authors:{" "}
            <a
              href="https://github.com/VishalPatil18"
              target="_blank"
              rel="noopener noreferrer"
            >
              Vishal
            </a>
            ,{" "}
            <a
              href="https://github.com/Achuth07"
              target="_blank"
              rel="noopener noreferrer"
            >
              Achuth
            </a>{" "}
            &{" "}
            <a
              href="https://github.com/alessandro1g"
              target="_blank"
              rel="noopener noreferrer"
            >
              Alessandro
            </a>
          </span>
        </div>
        <div className="footer-right">
          <a
            href="https://github.com/alessandro1g/project-application-template/tree/main"
            target="_blank"
            rel="noopener noreferrer"
          >
            Repolizer Codebase
          </a>
        </div>
      </footer>
    </div>
  );
}

export default App;
