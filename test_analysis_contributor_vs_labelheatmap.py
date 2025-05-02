import unittest
from unittest.mock import patch, MagicMock
from analysis_contributor_vs_labelheatmap import ContributorVsLabelHeatmap
from model import Issue
import matplotlib.pyplot as plt


class TestContributorVsLabelHeatmap(unittest.TestCase):

    @patch('analysis_contributor_vs_labelheatmap.plt.show')
    @patch('analysis_contributor_vs_labelheatmap.DataLoader')
    def test_run_with_mock_data(self, mock_loader, mock_show):
        mock_issue = MagicMock(spec=Issue)
        mock_issue.creator = "alice"
        mock_issue.labels = ["bug", "enhancement"]

        mock_loader.return_value.get_issues.return_value = [mock_issue]

        analysis = ContributorVsLabelHeatmap()
        analysis.run()

        self.assertEqual(len(analysis.issues), 1)
        self.assertEqual(analysis.issues[0].creator, "alice")
        mock_show.assert_called_once()

    @patch('analysis_contributor_vs_labelheatmap.plt.show')
    @patch('analysis_contributor_vs_labelheatmap.DataLoader')
    def test_run_with_empty_issues(self, mock_loader, mock_show):
        mock_loader.return_value.get_issues.return_value = []
        analysis = ContributorVsLabelHeatmap()
        analysis.run()
        mock_show.assert_not_called()


if __name__ == '__main__':
    unittest.main()
