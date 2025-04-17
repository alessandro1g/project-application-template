# analysis2_monthly_issue_trend.py

import matplotlib.pyplot as plt
import pandas as pd
from data_loader import DataLoader
from model import Issue


class MonthlyIssueTrend:
    def __init__(self):
        self.issues = DataLoader().get_issues()

    def run(self):
        dates = []
        for issue in self.issues:
            if issue.created_date:
                dates.append(issue.created_date.strftime('%Y-%m'))

        if not dates:
            print("No issue creation data found.")
            return

        df = pd.DataFrame(dates, columns=["month"])
        df["month"] = pd.to_datetime(df["month"])

        monthly_counts = df.groupby("month").size().reset_index(name="issue_count")

        plt.figure(figsize=(12, 6))
        plt.plot(monthly_counts["month"], monthly_counts["issue_count"], marker="o")
        plt.title("Monthly Issue Creation Trend")
        plt.xlabel("Month")
        plt.ylabel("Number of Issues")
        plt.grid(True)
        plt.tight_layout()
        plt.xticks(rotation=45)
        plt.show()
