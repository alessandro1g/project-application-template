import unittest
from unittest.mock import patch, MagicMock
from analysis_issue_count_by_label import AnalyzeIssueCountByLabel


class TestAnalyzeIssueCountByLabel(unittest.TestCase):

    @patch('analysis2.DataLoader')
    def test_init_loads_issues(self, mock_data_loader):
        mock_data_loader.return_value.get_issues.return_value = [{'labels': []}]
        analyzer = AnalyzeIssueCountByLabel()
        self.assertEqual(analyzer.issues, [{'labels': []}])

    def test_count_issue_labels_with_dict_and_str(self):
        issues = [
            {"labels": [{"name": "bug"}, {"name": "enhancement"}]},
            {"labels": ["question", {"name": "bug"}]},
            {"labels": []},
        ]
        analyzer = AnalyzeIssueCountByLabel()
        result = analyzer.count_issue_labels(issues)
        expected = {"bug": 2, "enhancement": 1, "question": 1}
        self.assertEqual(result, expected)

    @patch('analysis2.plt')
    def test_plot_label_counts_executes_plot(self, mock_plt):
        analyzer = AnalyzeIssueCountByLabel()
        label_counts = {"bug": 5, "feature": 3}
        analyzer.plot_label_counts(label_counts)

        mock_plt.figure.assert_called_once()
        mock_plt.bar.assert_called_once()
        mock_plt.xlabel.assert_called_with('Labels')
        mock_plt.ylabel.assert_called_with('Number of Issues')
        mock_plt.title.assert_called_with('GitHub Issue Count by Label')
        mock_plt.show.assert_called_once()

    @patch.object(AnalyzeIssueCountByLabel, 'count_issue_labels')
    @patch.object(AnalyzeIssueCountByLabel, 'plot_label_counts')
    @patch('analysis2.DataLoader')
    def test_run_with_valid_issues(self, mock_data_loader, mock_plot, mock_count):
        mock_data_loader.return_value.get_issues.return_value = [{'labels': [{'name': 'bug'}]}]
        mock_count.return_value = {'bug': 1}

        analyzer = AnalyzeIssueCountByLabel()
        analyzer.run()

        mock_count.assert_called_once_with([{'labels': [{'name': 'bug'}]}])
        mock_plot.assert_called_once_with({'bug': 1})

    @patch('analysis2.DataLoader')
    def test_run_with_none_issues(self, mock_data_loader):
        mock_data_loader.return_value.get_issues.return_value = None
        analyzer = AnalyzeIssueCountByLabel()
        result = analyzer.run()
        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()
