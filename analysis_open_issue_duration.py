from typing import List
from datetime import datetime, timezone
import matplotlib.pyplot as plt
from data_loader import DataLoader


class AnalyzeOpenIssueDurationMonths:
    # Getting the Issues Data
    def __init__(self):
        self.issues = DataLoader().get_issues()

    def run(self):
        issues = self.fetch_issues()
        if not issues:
            return

        durations = self.get_open_issue_durations_months(issues)
        if not durations:
            print("No open issues found.")
            return

        window_centers, counts = self.calculate_distribution(durations)
        self.plot_distribution(window_centers, counts)

    # Count duration for which each issue has been open
    def get_open_issue_durations_months(self, issues: List[dict]) -> List[float]:
        durations = []
        now = datetime.now(timezone.utc)
        for issue in issues:
            if issue.get("state") == "open":
                created_str = issue.get("created_date")
                if created_str:
                    try:
                        created_date = datetime.fromisoformat(created_str.replace('Z', '+00:00'))
                        months_open = (now - created_date).days / 30.44
                        durations.append(months_open)
                    except ValueError as e:
                        print(f"Invalid date format: {created_str}, error: {e}")
        return durations

    # Calculate the distribution of the data based on the maximum duration and minimum duration
    def calculate_distribution(self, durations: List[float]) -> tuple:
        min_dur = min(durations)
        max_dur = max(durations)
        window_size = (max_dur - min_dur) / 10
        windows = [min_dur + i * window_size for i in range(11)]

        counts = [0] * 10
        for duration in durations:
            for i in range(10):
                if windows[i] <= duration < windows[i + 1]:
                    counts[i] += 1
                    break

        centers = [(windows[i] + windows[i + 1]) / 2 for i in range(10)]
        return centers, counts

    # Create a plot for open issues and duration distribution
    def plot_distribution(self, window_centers: List[float], issue_counts: List[int]):
        plt.figure(figsize=(14, 7))
        plt.plot(window_centers, issue_counts, marker='o', linestyle='-')
        plt.xlabel('Open Issue Duration (Months)')
        plt.ylabel('Number of Issues')
        plt.title('Distribution of Open Issue Durations (Months)')
        plt.grid(True)
        plt.tight_layout()
        plt.show()


if __name__ == '__main__':
    # Invoke run method when running this module directly
    AnalyzeOpenIssueDurationMonths().run()
