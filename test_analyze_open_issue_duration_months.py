import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta, timezone
from analysis_open_issue_duration import AnalyzeOpenIssueDurationMonths


class TestAnalyzeOpenIssueDurationMonths(unittest.TestCase):

    @patch('analysis_open_issue_duration.DataLoader')
    def test_get_open_issue_durations_months_valid(self, MockDataLoader):
        now = datetime.now(timezone.utc)
        thirty_days_ago = (now - timedelta(days=30)).isoformat()

        MockDataLoader.return_value.get_issues.return_value = []
        analyzer = AnalyzeOpenIssueDurationMonths()
        issues = [
            {"state": "open", "created_date": thirty_days_ago},
            {"state": "closed", "created_date": thirty_days_ago},
            {"state": "open", "created_date": "invalid-date"}
        ]

        with patch('analysis_open_issue_duration.datetime') as mock_datetime:
            mock_datetime.now.return_value = now
            mock_datetime.fromisoformat.side_effect = lambda s: datetime.fromisoformat(s)

            durations = analyzer.get_open_issue_durations_months(issues)

        self.assertEqual(len(durations), 1)
        self.assertAlmostEqual(durations[0], 30 / 30.44, places=1)

    def test_calculate_distribution(self):
        analyzer = AnalyzeOpenIssueDurationMonths()
        durations = [1, 2, 2.5, 3, 4, 5, 6, 7, 8, 9]

        centers, counts = analyzer.calculate_distribution(durations)

        self.assertEqual(len(centers), 10)
        self.assertEqual(len(counts), 10)
        self.assertEqual(sum(counts), len(durations))

    @patch('analysis_open_issue_duration.AnalyzeOpenIssueDurationMonths.plot_distribution')
    @patch('analysis_open_issue_duration.DataLoader')
    def test_run_with_valid_data(self, MockDataLoader, mock_plot):
        now = datetime.now(timezone.utc)
        MockDataLoader.return_value.get_issues.return_value = [
            {"state": "open", "created_date": (now - timedelta(days=60)).isoformat()},
            {"state": "closed", "created_date": (now - timedelta(days=10)).isoformat()}
        ]

        analyzer = AnalyzeOpenIssueDurationMonths()
        analyzer.fetch_issues = MagicMock(return_value=analyzer.issues)

        with patch('analysis_open_issue_duration.datetime') as mock_datetime:
            mock_datetime.now.return_value = now
            mock_datetime.fromisoformat.side_effect = lambda s: datetime.fromisoformat(s)

            analyzer.run()
            mock_plot.assert_called_once()

    @patch('builtins.print')
    @patch('analysis_open_issue_duration.DataLoader')
    def test_run_with_no_open_issues(self, MockDataLoader, mock_print):
        MockDataLoader.return_value.get_issues.return_value = [
            {"state": "closed", "created_date": "2022-01-01T00:00:00Z"}
        ]

        analyzer = AnalyzeOpenIssueDurationMonths()
        analyzer.fetch_issues = MagicMock(return_value=analyzer.issues)
        analyzer.run()

        mock_print.assert_called_once_with("No open issues found.")

    @patch('analysis_open_issue_duration.DataLoader')
    def test_run_with_none_issues(self, MockDataLoader):
        MockDataLoader.return_value.get_issues.return_value = None
        analyzer = AnalyzeOpenIssueDurationMonths()
        analyzer.fetch_issues = MagicMock(return_value=None)
        result = analyzer.run()
        self.assertIsNone(result)

