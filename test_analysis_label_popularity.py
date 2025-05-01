import unittest
from unittest.mock import patch, MagicMock
from analysis_label_popularity import LabelPopularityOverTime
from model import Issue
from datetime import datetime


class TestLabelPopularityOverTime(unittest.TestCase):

    @patch('analysis_label_popularity.plt.show')
    @patch('analysis_label_popularity.DataLoader')
    def test_run_with_mock_labels(self, mock_loader, mock_show):
        mock_issue = MagicMock(spec=Issue)
        mock_issue.created_date = datetime(2025, 1, 20)
        mock_issue.labels = ["bug", "feature"]

        mock_loader.return_value.get_issues.return_value = [mock_issue]

        analysis = LabelPopularityOverTime()
        analysis.run()

        self.assertIn("bug", mock_issue.labels)
        mock_show.assert_called_once()

    @patch('analysis_label_popularity.plt.show')
    @patch('analysis_label_popularity.DataLoader')
    def test_run_with_empty_data(self, mock_loader, mock_show):
        mock_loader.return_value.get_issues.return_value = []
        analysis = LabelPopularityOverTime()
        analysis.run()
        mock_show.assert_not_called()


if __name__ == '__main__':
    unittest.main()
