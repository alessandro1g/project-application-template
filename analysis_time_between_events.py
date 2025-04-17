
from typing import List
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from datetime import datetime
from data_loader import DataLoader
from model import Issue,Event
import config


class Analysis2:
    def __init__(self):
        # Parameter is passed in via command line (--user)
        self.USER:str = config.get_parameter('user')
    
    def run(self):
        issues: List[Issue] = DataLoader().get_issues()
        
        # Prepare data for plotting
        issue_event_data = []
        issue_dict = {}
        for issue in issues:
            issue_dict[issue.title] = {}
            for event in issue.events:
                event_time = event.event_date  
                # Convert the event time to a datetime object
                if event_time is not None: 
                    if event_time.month not in issue_dict[issue.title]:
                        issue_dict[issue.title][event_time.month] = 1
                    else: 
                        issue_dict[issue.title][event_time.month] += 1


        plt.figure(figsize=(10, 6))  # Move this outside the loop to create a single plot

        for issue_title, months in issue_dict.items():
            # Sort the months dictionary by month (key)
            sorted_months = sorted(months.items())  # Returns a list of tuples [(month, count), ...]
            x = [month for month, _ in sorted_months]  # Extract months (x-axis)
            y = [count for _, count in sorted_months]  # Extract counts (y-axis)

            # Plot each issue's data as a separate line
            plt.plot(x, y, label=issue_title)

        # Adding labels, title, and legend
        plt.xlabel("Month")
        plt.ylabel("Event Count")
        plt.title("Event Counts by Month for Each Issue")
        plt.legend()
        plt.grid(True)
        plt.show()

if __name__ == '__main__':
    # Invoke run method when running this module directly
    Analysis2().run()