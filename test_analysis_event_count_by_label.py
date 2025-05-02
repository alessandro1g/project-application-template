import unittest
from unittest.mock import patch
from analysis_event_count_by_label import Analyze_Event_Count_By_Label

class TestAnalyzeEventCountByLabel(unittest.TestCase):
    def setUp(self):
        self.analyzer = Analyze_Event_Count_By_Label()

    def test_count_labels_various(self):
        issues = [
            {"labels": [{"name": "error"}, {"name": "feature"}]},
            {"labels": ["error", "suggestion"]},
            {"labels": []},
            {},
            {"labels": [{"name": "error"}]},
        ]
        result = self.analyzer.count_labels(issues)
        self.assertEqual(result, {"error": 3, "feature": 1, "suggestion": 1})

    def test_count_labels_empty(self):
        self.assertEqual(self.analyzer.count_labels([]), {})

    @patch("analysis_event_count_by_label.plt.show")
    def test_plot_label_distribution(self, mock_show):
        label_counts = {"error": 5, "feature": 3}
        self.analyzer.plot_label_distribution(label_counts)
        mock_show.assert_called_once()

    @patch("analysis_event_count_by_label.DataLoader")
    @patch("analysis_event_count_by_label.Analyze_Event_Count_By_Label.plot_label_distribution")
    def test_run_none(self, mock_plot, mock_loader):
        self.analyzer.issues = None
        self.analyzer.run()
        mock_plot.assert_not_called()

    @patch("analysis_event_count_by_label.DataLoader")
    @patch("analysis_event_count_by_label.Analyze_Event_Count_By_Label.plot_label_distribution")
    def test_run_valid(self, mock_plot, mock_loader):
        self.analyzer.issues = [{"labels": ["error"]}]
        self.analyzer.run()
        mock_plot.assert_called_once()

if __name__ == "__main__":
    unittest.main()
