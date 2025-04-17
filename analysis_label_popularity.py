# analysis3_label_popularity.py

import matplotlib.pyplot as plt
import pandas as pd
from data_loader import DataLoader
from model import Issue


class LabelPopularityOverTime:
    def __init__(self):
        self.issues = DataLoader().get_issues()

    def run(self):
        records = []

        for issue in self.issues:
            if issue.created_date and issue.labels:
                month = issue.created_date.strftime('%Y-%m')
                for label in issue.labels:
                    records.append({"month": month, "label": label})

        if not records:
            print("No labels found.")
            return

        df = pd.DataFrame(records)
        df["month"] = pd.to_datetime(df["month"])

        top_labels = df["label"].value_counts().nlargest(5).index
        df_top = df[df["label"].isin(top_labels)]

        label_trend = df_top.groupby(["month", "label"]).size().reset_index(name="count")
        pivot = label_trend.pivot(index="month", columns="label", values="count").fillna(0)

        pivot.plot(marker="o", figsize=(14, 7))
        plt.title("Label Popularity Over Time (Top 5 Labels)")
        plt.xlabel("Month")
        plt.ylabel("Label Usage Count")
        plt.grid(True)
        plt.tight_layout()
        plt.xticks(rotation=45)
        plt.show()
