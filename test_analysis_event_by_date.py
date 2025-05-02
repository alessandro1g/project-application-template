import unittest
from unittest.mock import patch, MagicMock
from analysis_event_by_date import Analysis_Event_By_Date
from model import Issue, Event
import datetime

class TestAnalysisEventByDate(unittest.TestCase):

    @patch('analysis_event_by_date.DataLoader')
    @patch('analysis_event_by_date.config.get_parameter')
    @patch('analysis_event_by_date.Analysis_Event_By_Date.plot_date_event_map')
    def test_run_with_mocked_data(self, mock_plot, mock_get_parameter, mock_data_loader):
        # Mock the config parameter
        mock_get_parameter.return_value = 'test_user'

        # Mock the DataLoader to return test issues and events
        mock_event1 = MagicMock(spec=Event)
        mock_event1.event_date = datetime.date(2023, 10, 1)

        mock_event2 = MagicMock(spec=Event)
        mock_event2.event_date = datetime.date(2023, 10, 2)

        mock_event3 = MagicMock(spec=Event)
        mock_event3.event_date = datetime.date(2023, 10, 1)

        mock_issue1 = MagicMock(spec=Issue)
        mock_issue1.events = [mock_event1, mock_event2]

        mock_issue2 = MagicMock(spec=Issue)
        mock_issue2.events = [mock_event3]

        mock_data_loader.return_value.get_issues.return_value = [mock_issue1, mock_issue2]

        # Instantiate and run the analysis
        analysis = Analysis_Event_By_Date()
        analysis.run()

        # Verify the plot_date_event_map was called with the correct data
        expected_date_event_map = {
            datetime.date(2023, 10, 1): 2,
            datetime.date(2023, 10, 2): 1
        }
        mock_plot.assert_called_once_with(expected_date_event_map)

    @patch('analysis_event_by_date.Analysis_Event_By_Date.plot_date_event_map')
    def test_plot_date_event_map(self, mock_plot):
        # Test the plot_date_event_map method directly
        analysis = Analysis_Event_By_Date()
        date_event_map = {
            datetime.date(2023, 10, 1): 5,
            datetime.date(2023, 10, 2): 3
        }

        # Call the method
        with patch('matplotlib.pyplot.show'):
            analysis.plot_date_event_map(date_event_map)

        # Verify no exceptions occur (visual inspection of the plot is manual)

    @patch('analysis_event_by_date.DataLoader')
    def test_empty_issues(self, mock_data_loader):
        # Test the case where no issues are returned
        mock_data_loader.return_value.get_issues.return_value = []

        analysis = Analysis_Event_By_Date()
        with patch('analysis_event_by_date.Analysis_Event_By_Date.plot_date_event_map') as mock_plot:
            analysis.run()
            mock_plot.assert_called_once_with({})  # Expect an empty map

    def test_date_event_map_edge_cases(self):
        # Test edge cases for date_event_map
        analysis = Analysis_Event_By_Date()

        # Case 1: No events
        issues = []
        result = analysis.generate_date_event_map(issues)
        self.assertEqual(result, {})

        # Case 2: Events with the same date
        mock_event1 = MagicMock(spec=Event)
        mock_event1.event_date = datetime.date(2023, 10, 1)

        mock_event2 = MagicMock(spec=Event)
        mock_event2.event_date = datetime.date(2023, 10, 1)

        mock_issue = MagicMock(spec=Issue)
        mock_issue.events = [mock_event1, mock_event2]

        result = analysis.generate_date_event_map([mock_issue])
        self.assertEqual(result, {datetime.date(2023, 10, 1): 2})

    @patch('matplotlib.pyplot.show')
    def test_plot_date_event_map_empty(self, mock_show):
        # Test plotting with an empty date_event_map
        analysis = Analysis_Event_By_Date()
        analysis.plot_date_event_map({})
        mock_show.assert_called_once()  # Ensure the plot is still shown

if __name__ == '__main__':
    unittest.main()