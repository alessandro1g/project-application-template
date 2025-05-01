import unittest
from unittest.mock import patch
from analysis_issue_per_event import AnalyzeIssuePerEvent


class TestAnalyzeIssuePerEvent(unittest.TestCase):

    @patch('analysis4.DataLoader')
    def test_extract_event_counts(self, MockDataLoader):
        MockDataLoader.return_value.get_issues.return_value = [
            {"events": [1, 2, 3]},
            {"events": []},
            {"events": [1]},
            {"events": None},
            {"events": "not-a-list"}
        ]

        analyzer = AnalyzeIssuePerEvent()
        counts = analyzer.extract_event_counts(analyzer.issues)
        self.assertEqual(counts, [3, 0, 1, 0, 0, 0])

    def test_categorize_event_counts(self):
        analyzer = AnalyzeIssuePerEvent()

        sample_counts = [0, 3, 7, 13, 18, 25, 0, 1, 21]
        result = analyzer.categorize_event_counts(sample_counts)

        expected = {
            "0": 2,
            "1-5": 2,
            "6-10": 1,
            "11-15": 1,
            "16-20": 1,
            "21+": 2
        }
        self.assertEqual(result, expected)

    @patch('analysis4.AnalyzeIssuePerEvent.plot_event_distribution')
    @patch('analysis4.DataLoader')
    def test_run_with_valid_issues(self, MockDataLoader, mock_plot):
        MockDataLoader.return_value.get_issues.return_value = [
            {"events": [1, 2]},
            {"events": []},
            {"events": [1] * 10},
            {"events": [1] * 30},
        ]

        analyzer = AnalyzeIssuePerEvent()
        analyzer.run()

        expected_counts = {
            "0": 1,
            "1-5": 1,
            "6-10": 1,
            "11-15": 0,
            "16-20": 0,
            "21+": 1
        }

        mock_plot.assert_called_once_with(expected_counts)

    @patch('analysis4.DataLoader')
    def test_run_with_no_issues(self, MockDataLoader):
        MockDataLoader.return_value.get_issues.return_value = None

        analyzer = AnalyzeIssuePerEvent()
        self.assertIsNone(analyzer.run())  # run exits early

    @patch('analysis4.DataLoader')
    @patch('builtins.print')
    def test_run_with_no_event_data(self, mock_print, MockDataLoader):
        MockDataLoader.return_value.get_issues.return_value = [
            {"events": []},
            {"events": None},
            {},
        ]

        analyzer = AnalyzeIssuePerEvent()
        analyzer.run()
        mock_print.assert_called_once_with("No events found in the issues.")
