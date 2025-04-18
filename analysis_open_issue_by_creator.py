from typing import List
from collections import Counter
import matplotlib.pyplot as plt
from random import random
from data_loader import DataLoader


class AnalyzeOpenIssuesByCreator:
    # Getting the Issues Data
    def __init__(self):
        self.issues = DataLoader().get_issues()

    def run(self):
        issues = self.fetch_issues()
        if not issues:
            return

        creator_counts = self.count_open_issues_by_creator(issues)
        if not creator_counts:
            print("No open issues found.")
            return

        self.plot_pie_chart(creator_counts)

    # Count the issues for each creator using dictionary
    def count_open_issues_by_creator(self, issues: List[dict]) -> Counter:
        counter = Counter()
        for issue in issues:
            if issue.get("state") == "open" and issue.get("creator"):
                counter[issue["creator"]] += 1
        return counter

    # Create a pie chart for top 10 authors of issues
    def plot_pie_chart(self, creator_counts: Counter):
        top_creators = creator_counts.most_common(self.top_n)
        creators = [creator for creator, _ in top_creators]
        counts = [count for _, count in top_creators]
        colors = [f'#{hex(int(random() * 16777215))[2:].zfill(6)}' for _ in range(len(creators))]

        plt.figure(figsize=(10, 10))
        plt.pie(counts, labels=creators, autopct='%1.1f%%', startangle=140, colors=colors)
        plt.title(f'Distribution of Open Issues by Creator (Top {self.top_n})')
        plt.axis('equal')
        plt.tight_layout()
        plt.style.use('seaborn-v0_8-pastel')
        plt.show()


if __name__ == "__main__":
    # Invoke run method when running this module directly
    AnalyzeOpenIssuesByCreator().run()
