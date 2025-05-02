import unittest
from unittest.mock import patch, MagicMock
from analysis_type_of_events import Analysis_Type_Of_Events
from model import Issue, Event
import datetime

# filepath: /Users/alessandrogagarin/Documents/MERM BACKEND/project-application-template/test_analysis_type_of_events.py

class TestAnalysisTypeOfEvents(unittest.TestCase):

    @patch('analysis_type_of_events.config.get_parameter')
    def test_init(self, mock_get_parameter):
        # Mock the config parameter
        mock_get_parameter.return_value = 'test_user'
        analysis = Analysis_Type_Of_Events()
        self.assertEqual(analysis.USER, 'test_user')

    @patch('analysis_type_of_events.DataLoader')
    @patch('analysis_type_of_events.config.get_parameter')
    @patch('analysis_type_of_events.Analysis_Type_Of_Events.plot_data')
    def test_run_with_mocked_data(self, mock_plot_data, mock_get_parameter, mock_data_loader):
        # Mock the config parameter
        mock_get_parameter.return_value = 'test_user'

        # Mock the DataLoader to return test issues and events
        mock_event1 = MagicMock(spec=Event)
        mock_event1.event_date = datetime.date(2023, 10, 1)
        mock_event1.event_type = 'type1'

        mock_event2 = MagicMock(spec=Event)
        mock_event2.event_date = datetime.date(2023, 10, 1)
        mock_event2.event_type = 'type2'

        mock_event3 = MagicMock(spec=Event)
        mock_event3.event_date = datetime.date(2023, 11, 1)
        mock_event3.event_type = 'type1'

        mock_issue1 = MagicMock(spec=Issue)
        mock_issue1.events = [mock_event1, mock_event2]

        mock_issue2 = MagicMock(spec=Issue)
        mock_issue2.events = [mock_event3]

        mock_data_loader.return_value.get_issues.return_value = [mock_issue1, mock_issue2]

        # Instantiate and run the analysis
        analysis = Analysis_Type_Of_Events()
        analysis.run()

        # Verify the plot_data was called with the correct data
        expected_issue_dict = {
            '10-2023': {'type1': 1, 'type2': 1},
            '11-2023': {'type1': 1}
        }
        mock_plot_data.assert_called_once_with(expected_issue_dict)

    @patch('matplotlib.pyplot.show')
    def test_plot_data(self, mock_show):
        # Test the plot_data method directly
        analysis = Analysis_Type_Of_Events()
        issue_dict = {
            '10-2023': {'type1': 2, 'type2': 1},
            '11-2023': {'type1': 1}
        }

        # Call the method
        analysis.plot_data(issue_dict)

        # Verify no exceptions occur (visual inspection of the plot is manual)
        mock_show.assert_called_once()

    @patch('analysis_type_of_events.DataLoader')
    def test_run_with_empty_issues(self, mock_data_loader):
        # Test the case where no issues are returned
        mock_data_loader.return_value.get_issues.return_value = []

        analysis = Analysis_Type_Of_Events()
        with patch('analysis_type_of_events.Analysis_Type_Of_Events.plot_data') as mock_plot_data:
            analysis.run()
            mock_plot_data.assert_called_once_with({})  # Expect an empty dictionary

    @patch('matplotlib.pyplot.show')
    def test_plot_data_with_empty_dict(self, mock_show):
        # Test plotting with an empty issue_dict
        analysis = Analysis_Type_Of_Events()
        analysis.plot_data({})
        mock_show.assert_called_once()  # Ensure the plot is still shown

if __name__ == '__main__':
    unittest.main()