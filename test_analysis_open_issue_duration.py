import unittest
from unittest.mock import patch
from datetime import datetime, timezone
from analysis_open_issue_duration import AnalyzeOpenIssueDurationMonths

class TestAnalyzeOpenIssueDurationMonths(unittest.TestCase):
    def setUp(self):
        self.analyzer = AnalyzeOpenIssueDurationMonths()

    @patch("analysis_open_issue_duration.datetime")
    def test_get_open_issue_durations_months_various(self, mock_datetime):
        now = datetime(2025, 5, 1, tzinfo=timezone.utc)
        mock_datetime.now.return_value = now
        mock_datetime.fromisoformat.side_effect = lambda s: datetime.fromisoformat(s)
        issues = [
            {"state": "open", "created_date": "2025-04-01T00:00:00+00:00"},
            {"state": "open", "created_date": "not-a-date"},
            {"state": "open", "created_date": "2025-03-01T00:00:00+00:00"},
            {"state": "closed", "created_date": "2025-02-01T00:00:00+00:00"},
            {},
        ]
        durations = self.analyzer.get_open_issue_durations_months(issues)
        self.assertEqual(len(durations), 2)
        self.assertTrue(all(isinstance(d, float) for d in durations))

    def test_calculate_distribution_basic(self):
        durations = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        centers, counts = self.analyzer.calculate_distribution(durations)
        self.assertEqual(len(centers), 10)
        self.assertEqual(sum(counts), 10)

    @patch("analysis_open_issue_duration.plt.show")
    def test_plot_distribution(self, mock_show):
        self.analyzer.plot_distribution([1, 2, 3], [4, 5, 6])
        mock_show.assert_called_once()

    def test_run_with_none_or_no_open(self):
        self.analyzer.issues = None
        with patch.object(self.analyzer, "plot_distribution") as mock_plot:
            self.analyzer.run()
            mock_plot.assert_not_called()

        self.analyzer.issues = [{"state": "closed", "created_date": "2025-02-01T00:00:00+00:00"}]
        with patch("builtins.print") as mock_print:
            self.analyzer.run()
            mock_print.assert_any_call("No open issues found.")

    @patch("analysis_open_issue_duration.datetime")
    def test_run_with_open_issues(self, mock_datetime):
        now = datetime(2025, 5, 1, tzinfo=timezone.utc)
        mock_datetime.now.return_value = now
        mock_datetime.fromisoformat.side_effect = lambda s: datetime.fromisoformat(s)
        self.analyzer.issues = [{"state": "open", "created_date": "2025-04-01T00:00:00+00:00"}]
        with patch.object(self.analyzer, "plot_distribution") as mock_plot:
            self.analyzer.run()
            mock_plot.assert_called_once()

if __name__ == "__main__":
    unittest.main()

