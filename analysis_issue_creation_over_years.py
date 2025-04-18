from collections import defaultdict
import matplotlib.pyplot as plt
from typing import Dict, List
from datetime import datetime
from data_loader import DataLoader


class AnalyzeIssueCreationOverYears:
    # Getting the Issues Data
    def __init__(self):
        self.issues = DataLoader().get_issues()

    def run(self):
        issues = self.load_issues()
        if issues is None:
            return

        yearly_counts = self.count_issues_by_year(issues)
        self.plot_yearly_trend(yearly_counts)

    # Count Issues by year with the help of created_date attribute
    def count_issues_by_year(self, issues: List[Dict]) -> Dict[int, int]:
        yearly_counts = defaultdict(int)

        for issue in issues:
            created_date = issue.get("created_date")
            if created_date:
                try:
                    date_obj = datetime.fromisoformat(created_date.replace('Z', '+00:00'))
                    yearly_counts[date_obj.year] += 1
                except ValueError as e:
                    print(f"Invalid date format: {created_date}, error: {e}")
        return dict(yearly_counts)

    # Create a plot for Yearly Issues Count
    def plot_yearly_trend(self, yearly_counts: Dict[int, int]):
        years = sorted(yearly_counts.keys())
        counts = [yearly_counts[year] for year in years]

        plt.figure(figsize=(14, 7))
        plt.plot(years, counts, marker='o', linestyle='-')
        plt.xlabel('Year')
        plt.ylabel('Number of Issues Opened (Yearly)')
        plt.title('GitHub Issue Creation Trend Over Years')
        plt.grid(True)
        plt.tight_layout()
        plt.show()


if __name__ == '__main__':
    # Invoke run method when running this module directly
    AnalyzeIssueCreationOverYears().run()
