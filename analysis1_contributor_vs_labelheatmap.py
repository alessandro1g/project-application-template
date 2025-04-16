# analysis1_contributor_vs_labelheatmap.py

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from data_loader import DataLoader
from model import Issue
from collections import Counter

class ContributorVsLabelHeatmap:
    def __init__(self):
        self.issues = DataLoader().get_issues()

    def run(self):
        creator_label_pairs = []
        for issue in self.issues:
            creator = issue.creator
            labels = issue.labels
            for label in labels:
                creator_label_pairs.append((creator, label))

        if not creator_label_pairs:
            print("No contributor-label data found.")
            return

        df = pd.DataFrame(creator_label_pairs, columns=["creator", "label"])
        top_contributors = df['creator'].value_counts().nlargest(10).index
        df_top = df[df['creator'].isin(top_contributors)]

        heatmap_data = df_top.pivot_table(index="creator", columns="label", aggfunc="size", fill_value=0)

        plt.figure(figsize=(12, 6))
        sns.heatmap(heatmap_data, cmap="YlGnBu", linewidths=.5, annot=True, fmt='d')
        plt.title("Top 10 Contributors vs Labels Heatmap")
        plt.ylabel("Contributor")
        plt.xlabel("Label")
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()
        plt.show()
