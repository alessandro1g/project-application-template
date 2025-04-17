
from typing import List
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from data_loader import DataLoader
from model import Issue,Event
import config

class Analysis1:
    def __init__(self):
        # Parameter is passed in via command line (--user)
        self.USER:str = config.get_parameter('user')
    
    def run(self):
        issues:List[Issue] = DataLoader().get_issues()
        print(issues)
        
        ### BASIC STATISTICS
        # Calculate the total number of events for a specific user (if specified in command line args)
        date_event_map: dict = {}
        for issue in issues:
            # Access the correct attribute of the Event object
            for event in issue.events:
                event_date = event.event_date  # Replace 'date' with the actual attribute name for the event's date
                
                # Increment the count for the event's date
                if event_date in date_event_map:
                    date_event_map[event_date] += 1
                else:
                    date_event_map[event_date] = 1

        # Plot the date_event_map
        self.plot_date_event_map(date_event_map)

    def plot_date_event_map(self, date_event_map: dict):
        # Create a plot for date_event_map
        dates = list(date_event_map.keys())
        event_counts = list(date_event_map.values())

        plt.figure(figsize=(10, 6))
        plt.bar(dates, event_counts, color='skyblue')
        plt.xlabel('Date')
        plt.ylabel('Event Count')
        plt.title('Event Count by Date')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()


if __name__ == '__main__':
    # Invoke run method when running this module directly
    Analysis1().run()