import unittest
from unittest.mock import patch
from analysis_issue_per_event import AnalyzeIssuePerEvent

class TestAnalyzeIssuePerEvent(unittest.TestCase):
    def setUp(self):
        self.analyzer = AnalyzeIssuePerEvent()

    def test_extract_event_counts_various(self):
        issues = [
            {"events": [1, 2, 3]},
            {"events": []},
            {"events": [1]},
            {},
            {"events": None},
        ]
        result = self.analyzer.extract_event_counts(issues)
        self.assertEqual(result, [3, 0, 1, 0, 0])

    def test_categorize_event_counts_all_categories(self):
        counts = [0, 1, 2, 6, 12, 17, 22]
        result = self.analyzer.categorize_event_counts(counts)
        expected = {"0": 1, "1-5": 2, "6-10": 1, "11-15": 1, "16-20": 1, "21+": 1}
        self.assertEqual(result, expected)

    @patch("analysis_issue_per_event.plt.show")
    def test_plot_event_distribution(self, mock_show):
        categorized = {"0": 1, "1-5": 2, "6-10": 1, "11-15": 1, "16-20": 1, "21+": 1}
        self.analyzer.plot_event_distribution(categorized)
        mock_show.assert_called_once()

    def test_run_with_none_or_empty(self):
        self.analyzer.issues = None
        with patch.object(self.analyzer, "plot_event_distribution") as mock_plot:
            self.analyzer.run()
            mock_plot.assert_not_called()

        self.analyzer.issues = []
        with patch.object(self.analyzer, "plot_event_distribution") as mock_plot:
            self.analyzer.run()
            mock_plot.assert_not_called()

    def test_run_valid(self):
        self.analyzer.issues = [{"events": [1, 2]}]
        with patch.object(self.analyzer, "plot_event_distribution") as mock_plot:
            self.analyzer.run()
            mock_plot.assert_called_once()

if __name__ == "__main__":
    unittest.main()

