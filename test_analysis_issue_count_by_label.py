import unittest
from unittest.mock import patch
from analysis_issue_count_by_label import AnalyzeIssueCountByLabel

class TestAnalyzeIssueCountByLabel(unittest.TestCase):
    def setUp(self):
        self.analyzer = AnalyzeIssueCountByLabel()
        self.analyzer.json_url = "dummy_url" 

    def test_count_issue_labels_various(self):
        issues = [
            {"labels": [{"name": "error"}, {"name": "feature"}]},
            {"labels": ["error", "suggestion"]},
            {"labels": []},
            {},
            {"labels": [{"name": "error"}]},
        ]
        result = self.analyzer.count_issue_labels(issues)
        self.assertEqual(result, {"error": 3, "feature": 1, "suggestion": 1})

    def test_count_issue_labels_empty(self):
        self.assertEqual(self.analyzer.count_issue_labels([]), {})

    @patch("analysis_issue_count_by_label.plt.show")
    def test_plot_label_counts(self, mock_show):
        label_counts = {"error": 5, "feature": 3}
        self.analyzer.plot_label_counts(label_counts)
        mock_show.assert_called_once()


if __name__ == "__main__":
    unittest.main()
