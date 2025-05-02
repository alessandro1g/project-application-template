import unittest
from unittest.mock import patch
from collections import Counter
from analysis_open_issue_by_creator import AnalyzeOpenIssuesByCreator

class TestAnalyzeOpenIssuesByCreator(unittest.TestCase):
    def setUp(self):
        self.analyzer = AnalyzeOpenIssuesByCreator()
        self.analyzer.top_n = 10

    def test_count_open_issues_by_creator_various(self):
        issues = [
            {"state": "open", "creator": "vishal"},
            {"state": "closed", "creator": "aless"},
            {"state": "open", "creator": "vishal"},
            {"state": "open", "creator": "aless"},
            {"state": "open"},
        ]
        result = self.analyzer.count_open_issues_by_creator(issues)
        self.assertEqual(result, {"vishal": 2, "aless": 1})

    @patch("analysis_open_issue_by_creator.plt.show")
    @patch("matplotlib.pyplot.style.use")
    def test_plot_pie_chart(self, mock_style, mock_show):
        counts = Counter({"vishal": 2, "aless": 1})
        self.analyzer.plot_pie_chart(counts)
        mock_style.assert_called_once()
        mock_show.assert_called_once()

    def test_run_with_none_issues(self):
        self.analyzer.issues = None
        with patch.object(self.analyzer, "plot_pie_chart") as mock_plot:
            self.analyzer.run()
            mock_plot.assert_not_called()

    def test_run_with_no_open_issues(self):
        self.analyzer.issues = [{"state": "closed", "creator": "aless"}]
        with patch("builtins.print") as mock_print:
            self.analyzer.run()
            mock_print.assert_any_call("No open issues found.")

    def test_run_with_open_issues(self):
        self.analyzer.issues = [{"state": "open", "creator": "vishal"}]
        with patch.object(self.analyzer, "plot_pie_chart") as mock_plot:
            self.analyzer.run()
            mock_plot.assert_called_once()

if __name__ == "__main__":
    unittest.main()

