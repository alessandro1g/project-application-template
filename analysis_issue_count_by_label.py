from collections import Counter
import matplotlib.pyplot as plt
from typing import Dict, List
from data_loader import DataLoader


class AnalyzeIssueCountByLabel:
    # Getting the Issues Data
    def __init__(self):
        self.issues = DataLoader().get_issues()

    def run(self):
        issues = self.load_issues_from_url(self.json_url)
        if issues is None:
            return

        label_counts = self.count_issue_labels(issues)
        self.plot_label_counts(label_counts)

    # Count Issue Labels and increment its count if its already present in the dictionary
    def count_issue_labels(self, issues: List[Dict]) -> Dict[str, int]:
        label_counter = Counter()
        for issue in issues:
            labels = issue.get("labels", [])
            for label in labels:
                if isinstance(label, dict):
                    label_counter[label["name"]] += 1
                elif isinstance(label, str):
                    label_counter[label] += 1
        return dict(label_counter)

    # Create a plot for label and Issues Count
    def plot_label_counts(self, label_counts: Dict[str, int]):
        labels = list(label_counts.keys())
        counts = list(label_counts.values())

        plt.figure(figsize=(12, 6))
        plt.bar(labels, counts, color='skyblue')
        plt.xlabel('Labels')
        plt.ylabel('Number of Issues')
        plt.title('GitHub Issue Count by Label')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.show()


if __name__ == '__main__':
    # Invoke run method when running this module directly
    AnalyzeIssueCountByLabel().run()
