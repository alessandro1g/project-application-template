import unittest
from unittest.mock import patch, MagicMock
from collections import Counter
from analysis_open_issue_by_creator import AnalyzeOpenIssuesByCreator


class TestAnalyzeOpenIssuesByCreator(unittest.TestCase):

    @patch('analysis_open_issue_by_creator.DataLoader')
    def test_count_open_issues_by_creator(self, MockDataLoader):
        MockDataLoader.return_value.get_issues.return_value = []

        analyzer = AnalyzeOpenIssuesByCreator()
        sample_issues = [
            {"state": "open", "creator": "vishal"},
            {"state": "closed", "creator": "aless"},
            {"state": "open", "creator": "vishal"},
            {"state": "open", "creator": "achyut"},
            {"state": "open", "creator": None},
            {"state": "open"},  
        ]

        result = analyzer.count_open_issues_by_creator(sample_issues)
        expected = Counter({"vishal": 2, "achyut": 1})

        self.assertEqual(result, expected)

    @patch('analysis_open_issue_by_creator.AnalyzeOpenIssuesByCreator.plot_pie_chart')
    @patch('analysis_open_issue_by_creator.DataLoader')
    def test_run_with_valid_open_issues(self, MockDataLoader, mock_plot):
        MockDataLoader.return_value.get_issues.return_value = [
            {"state": "open", "creator": "vishal"},
            {"state": "closed", "creator": "aless"},
            {"state": "open", "creator": "aless"},
        ]

        analyzer = AnalyzeOpenIssuesByCreator()
        analyzer.top_n = 2
        analyzer.fetch_issues = MagicMock(return_value=analyzer.issues)
        analyzer.run()

        expected_counter = Counter({"vishal": 1, "aless": 1})
        mock_plot.assert_called_once_with(expected_counter)

    @patch('analysis_open_issue_by_creator.DataLoader')
    def test_run_with_no_issues(self, MockDataLoader):
        MockDataLoader.return_value.get_issues.return_value = None

        analyzer = AnalyzeOpenIssuesByCreator()
        analyzer.fetch_issues = MagicMock(return_value=None)
        self.assertIsNone(analyzer.run())  

    @patch('builtins.print')
    @patch('analysis_open_issue_by_creator.DataLoader')
    def test_run_with_no_open_issues(self, MockDataLoader, mock_print):
        MockDataLoader.return_value.get_issues.return_value = [
            {"state": "closed", "creator": "x"},
            {"state": "closed", "creator": "y"},
        ]

        analyzer = AnalyzeOpenIssuesByCreator()
        analyzer.fetch_issues = MagicMock(return_value=analyzer.issues)
        analyzer.run()

        mock_print.assert_called_once_with("No open issues found.")

