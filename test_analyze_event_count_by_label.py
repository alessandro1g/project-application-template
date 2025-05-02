import unittest
from unittest.mock import patch, MagicMock
from analysis_event_count_by_label import Analyze_Event_Count_By_Label


class TestAnalyzeEventCountByLabel(unittest.TestCase):

    @patch('analysis_event_count_by_label.DataLoader')
    def test_init_loads_issues(self, mock_data_loader):
        mock_data_loader.return_value.get_issues.return_value = [{'labels': []}]
        analyzer = Analyze_Event_Count_By_Label()
        self.assertEqual(analyzer.issues, [{'labels': []}])

    def test_count_labels_with_dict_and_str_labels(self):
        issues_data = [
            {"labels": [{"name": "error"}, {"name": "feature"}]},
            {"labels": ["suggestion", {"name": "error"}]},
            {"labels": []},
        ]
        analyzer = Analyze_Event_Count_By_Label()
        result = analyzer.count_labels(issues_data)
        expected = {"error": 2, "feature": 1, "suggestion": 1}
        self.assertEqual(result, expected)

    @patch('analysis_event_count_by_label.plt')
    def test_plot_label_distribution_executes(self, mock_plt):
        analyzer = Analyze_Event_Count_By_Label()
        label_counts = {"error": 5, "feature": 3}
        analyzer.plot_label_distribution(label_counts)

        mock_plt.figure.assert_called_once()
        mock_plt.bar.assert_called_once()
        mock_plt.xlabel.assert_called_with('Labels')
        mock_plt.ylabel.assert_called_with('Number of Issues')
        mock_plt.title.assert_called_with('GitHub Issue Count by Label')
        mock_plt.show.assert_called_once()

    @patch.object(Analyze_Event_Count_By_Label, 'count_labels')
    @patch.object(Analyze_Event_Count_By_Label, 'plot_label_distribution')
    @patch('analysis_event_count_by_label.DataLoader')
    def test_run_with_valid_issues(self, mock_data_loader, mock_plot, mock_count):
        mock_data_loader.return_value.get_issues.return_value = [{'labels': [{'name': 'error'}]}]
        mock_count.return_value = {'error': 1}

        analyzer = Analyze_Event_Count_By_Label()
        analyzer.run()

        mock_count.assert_called_once_with([{'labels': [{'name': 'error'}]}])
        mock_plot.assert_called_once_with({'error': 1})

    @patch('analysis_event_count_by_label.DataLoader')
    def test_run_with_none_issues(self, mock_data_loader):
        mock_data_loader.return_value.get_issues.return_value = None
        analyzer = Analyze_Event_Count_By_Label()
        result = analyzer.run()
        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()
