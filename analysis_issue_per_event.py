from collections import Counter
import matplotlib.pyplot as plt
import numpy as np
from data_loader import DataLoader
from typing import Dict, List
from scipy.interpolate import make_interp_spline


class AnalyzeIssuePerEvent:
    # Getting the Issues Data
    def __init__(self):
        self.issues = DataLoader().get_issues()

    def run(self):
        issues = self.load_issues()
        if issues is None:
            return

        event_counts = self.extract_event_counts(issues)
        if not event_counts:
            print("No events found in the issues.")
            return

        categorized_counts = self.categorize_event_counts(event_counts)
        self.plot_event_distribution(categorized_counts)

    # Count Events occured in a single issue
    def extract_event_counts(self, issues: List[Dict]) -> List[int]:
        event_counts = []
        for issue in issues:
            events = issue.get("events", [])
            event_counts.append(len(events) if isinstance(events, list) else 0)
        return event_counts

    # Create a categorization of the event counts
    def categorize_event_counts(self, event_counts: List[int]) -> Dict[str, int]:
        categories = ["0", "1-5", "6-10", "11-15", "16-20", "21+"]
        categorized = Counter()
        for count in event_counts:
            if count == 0:
                categorized["0"] += 1
            elif 1 <= count <= 5:
                categorized["1-5"] += 1
            elif 6 <= count <= 10:
                categorized["6-10"] += 1
            elif 11 <= count <= 15:
                categorized["11-15"] += 1
            elif 16 <= count <= 20:
                categorized["16-20"] += 1
            else:
                categorized["21+"] += 1
        return {cat: categorized[cat] for cat in categories}

    # Create a plot for Event counts and issues as categories
    def plot_event_distribution(self, categorized_counts: Dict[str, int]):
        categories = list(categorized_counts.keys())
        counts = list(categorized_counts.values())

        x = np.arange(len(categories))
        x_smooth = np.linspace(x.min(), x.max(), 300)
        spl = make_interp_spline(x, counts, k=3)
        y_smooth = spl(x_smooth)

        plt.figure(figsize=(10, 6))
        plt.plot(x_smooth, y_smooth, '-', color='royalblue')
        plt.xlabel("Event Count Category")
        plt.ylabel("Number of Issues")
        plt.title("Number of Issues per Event Count Category")
        plt.grid(True)
        plt.tight_layout()
        plt.savefig("events_per_issue_line_graph.png")
        plt.show()


if __name__ == '__main__':
    # Invoke run method when running this module directly
    AnalyzeIssuePerEvent().run()
