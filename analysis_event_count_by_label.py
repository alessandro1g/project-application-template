from collections import Counter
import matplotlib.pyplot as plt
from typing import Dict, List
from data_loader import DataLoader


class Analyze_Event_Count_By_Label:
    # Getting the Issues Data
    def __init__(self):
        self.issues = DataLoader().get_issues()

    def run(self):
        issues = self.issues
        if issues is None:
            return

        label_counts = self.count_labels(self.issues)
        self.plot_label_distribution(label_counts)

    # Count label by encapsulating then in a dictionary and a counter variable
    def count_labels(self, issues_data: List[Dict]) -> Dict[str, int]:
        label_counts = Counter()
        for issue in issues_data:
            labels = issue.get("labels", [])
            for label in labels:
                if isinstance(label, dict):
                    label_counts[label["name"]] += 1
                elif isinstance(label, str):
                    label_counts[label] += 1
        return dict(label_counts)

    # Create a plot for label distribution
    def plot_label_distribution(self, label_counts: Dict[str, int]):
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
    Analyze_Event_Count_By_Label().run()
