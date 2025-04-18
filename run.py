

"""
Starting point of the application. This module is invoked from
the command line to run the analyses.
"""

import argparse

import config
from example_analysis import ExampleAnalysis

from analysis_event_by_date import Analysis_Event_By_Date
from analysis_contributor_vs_labelheatmap import ContributorVsLabelHeatmap
from analysis_monthly_issue_trend import MonthlyIssueTrend
from analysis_label_popularity import LabelPopularityOverTime
from analysis_type_of_events import Analysis_Type_Of_Events
from analysis_event_count_by_label import Analyze_Event_Count_By_Label
from analysis_issue_count_by_label import AnalyzeIssueCountByLabel
from analysis_issue_creation_over_years import AnalyzeIssueCreationOverYears
from analysis_issue_per_event import AnalyzeIssuePerEvent
from analysis_open_issue_by_creator import AnalyzeOpenIssuesByCreator
from analysis_open_issue_duration import AnalyzeOpenIssueDurationMonths


def parse_args():
    """
    Parses the command line arguments that were provided along
    with the python command. The --feature flag must be provided as
    that determines what analysis to run. Optionally, you can pass in
    a user and/or a label to run analysis focusing on specific issues.
    
    You can also add more command line arguments following the pattern
    below.
    """
    ap = argparse.ArgumentParser("run.py")
    
    # Required parameter specifying what analysis to run
    ap.add_argument('--feature', '-f', type=int, required=True,
                    help='Which of the three features to run')
    
    # Optional parameter for analyses focusing on a specific user (i.e., contributor)
    ap.add_argument('--user', '-u', type=str, required=False,
                    help='Optional parameter for analyses focusing on a specific user')
    
    # Optional parameter for analyses focusing on a specific label
    ap.add_argument('--label', '-l', type=str, required=False,
                    help='Optional parameter for analyses focusing on a specific label')
    
    return ap.parse_args()



# Parse feature to call from command line arguments
args = parse_args()
# Add arguments to config so that they can be accessed in other parts of the application
config.overwrite_from_args(args)
    
# Run the feature specified in the --feature flag
if args.feature == 0:
    ExampleAnalysis().run()
elif args.feature == 1:
    Analysis_Event_By_Date().run()
elif args.feature == 2:
    ContributorVsLabelHeatmap().run()
elif args.feature == 3:
    MonthlyIssueTrend().run()
elif args.feature == 4:
    LabelPopularityOverTime().run()
elif args.feature == 5:
    Analysis_Type_Of_Events().run()
elif args.feature == 6:
    Analyze_Event_Count_By_Label().run()
elif args.feature == 7:
    AnalyzeIssueCountByLabel().run()
elif args.feature == 8:
    AnalyzeIssueCreationOverYears().run()
elif args.feature == 9:
    AnalyzeIssuePerEvent().run()
elif args.feature == 10:
    AnalyzeOpenIssuesByCreator().run()
elif args.feature == 11:
    AnalyzeOpenIssueDurationMonths().run()
else:
    print('Need to specify which feature to run with --feature flag.')
