import unittest
from unittest.mock import patch
from analysis_issue_creation_over_years import AnalyzeIssueCreationOverYears


class TestAnalyzeIssueCreationOverYears(unittest.TestCase):

    @patch('analysis3.DataLoader')
    def test_count_issues_by_year(self, MockDataLoader):
        MockDataLoader.return_value.get_issues.return_value = [
            {"created_date": "2020-01-01T10:00:00Z"},
            {"created_date": "2021-02-15T12:00:00Z"},
            {"created_date": "2020-05-20T09:30:00Z"},
            {"created_date": "invalid-date"},   
            {},                                 
        ]

        analyzer = AnalyzeIssueCreationOverYears()
        result = analyzer.count_issues_by_year(analyzer.issues)

        expected = {2020: 2, 2021: 1}
        self.assertEqual(result, expected)

    @patch('analysis3.AnalyzeIssueCreationOverYears.plot_yearly_trend')
    @patch('analysis3.DataLoader')
    def test_run_with_valid_and_invalid_dates(self, MockDataLoader, mock_plot):
        MockDataLoader.return_value.get_issues.return_value = [
            {"created_date": "2019-12-31T23:59:59Z"},
            {"created_date": "not-a-date"},
            {},
        ]

        analyzer = AnalyzeIssueCreationOverYears()
        analyzer.run()

        mock_plot.assert_called_once_with({2019: 1})

    @patch('analysis3.DataLoader')
    def test_run_with_no_issues(self, MockDataLoader):
        MockDataLoader.return_value.get_issues.return_value = None

        analyzer = AnalyzeIssueCreationOverYears()
        self.assertIsNone(analyzer.run())  

