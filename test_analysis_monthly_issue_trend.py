import unittest
from unittest.mock import patch, MagicMock
from analysis_monthly_issue_trend import MonthlyIssueTrend
from model import Issue
from datetime import datetime


class TestMonthlyIssueTrend(unittest.TestCase):

    @patch('analysis_monthly_issue_trend.plt.show')
    @patch('analysis_monthly_issue_trend.DataLoader')
    def test_run_with_mock_issues(self, mock_loader, mock_show):
        mock_issue = MagicMock(spec=Issue)
        mock_issue.created_date = datetime(2025, 3, 1)

        mock_loader.return_value.get_issues.return_value = [mock_issue]

        analysis = MonthlyIssueTrend()
        analysis.run()

        self.assertEqual(analysis.issues[0].created_date.month, 3)
        mock_show.assert_called_once()

    @patch('analysis_monthly_issue_trend.plt.show')
    @patch('analysis_monthly_issue_trend.DataLoader')
    def test_run_with_no_data(self, mock_loader, mock_show):
        mock_loader.return_value.get_issues.return_value = []
        analysis = MonthlyIssueTrend()
        analysis.run()
        mock_show.assert_not_called()


if __name__ == '__main__':
    unittest.main()
