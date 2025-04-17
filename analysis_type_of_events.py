
from typing import List
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from datetime import datetime
from data_loader import DataLoader
from model import Issue,Event
import config


class Analysis_Type_Of_Events:
    def __init__(self):
        # Parameter is passed in via command line (--user)
        self.USER:str = config.get_parameter('user')
    
    def run(self):
        issues: List[Issue] = DataLoader().get_issues()
        
        # Prepare data for plotting
        issue_dict = {}
        for issue in issues:
            for event in issue.events:
                event_time = event.event_date  
                # Convert the event time to a datetime object
                if event_time is not None: 
                    if str(event_time.month) + "-" + str(event_time.year) not in issue_dict:
                        issue_dict[str(event_time.month) + "-" + str(event_time.year)] = {}

                    if event.event_type not in issue_dict[str(event_time.month) + "-" + str(event_time.year)]:
                        issue_dict[str(event_time.month) + "-" + str(event_time.year)][event.event_type] = 1
                    else:
                        issue_dict[str(event_time.month) + "-" + str(event_time.year)][event.event_type] += 1

        # Plot the data
        self.plot_data(issue_dict)

    def plot_data(self, issue_dict):
        # Aggregate data for plotting
        months = sorted(issue_dict.keys())
        event_types = set(
            event_type for month in issue_dict.values() for event_type in month.keys()
        )
        
        for event_type in event_types:
            counts = [
                issue_dict[month].get(event_type, 0) for month in months
            ]
            plt.plot(months, counts, label=event_type)
        
        # Customize the plot
        plt.title("Event Counts by Month")
        plt.xlabel("Month")
        plt.ylabel("Count")
        plt.legend(loc='best', bbox_to_anchor=(1.05, 1))  # Move legend to the side
        plt.grid(True)
        plt.tight_layout()  # Adjust layout to fit the legend
        plt.show()

if __name__ == '__main__':
    # Invoke run method when running this module directly
    Analysis_Type_Of_Events().run()