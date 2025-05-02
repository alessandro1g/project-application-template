import unittest
from unittest.mock import patch
from analysis_issue_creation_over_years import AnalyzeIssueCreationOverYears

class TestAnalyzeIssueCreationOverYears(unittest.TestCase):
    def setUp(self):
        self.analyzer = AnalyzeIssueCreationOverYears()

    def test_count_issues_by_year_various(self):
        issues = [
            {"created_date": "2022-01-01T12:00:00Z"},
            {"created_date": "2023-05-10T15:00:00Z"},
            {"created_date": "not-a-date"},
            {"created_date": None},
            {},
        ]
        result = self.analyzer.count_issues_by_year(issues)
        self.assertEqual(result, {2022: 1, 2023: 1})

    @patch("analysis_issue_creation_over_years.plt.show")
    def test_plot_yearly_trend(self, mock_show):
        yearly_counts = {2022: 5, 2023: 10}
        self.analyzer.plot_yearly_trend(yearly_counts)
        mock_show.assert_called_once()

    def test_run_uses_self_issues(self):
        self.analyzer.issues = [{"created_date": "2022-01-01T12:00:00Z"}]
        with patch.object(self.analyzer, "plot_yearly_trend") as mock_plot:
            self.analyzer.run()
            mock_plot.assert_called_once()

    def test_run_with_none_issues(self):
        self.analyzer.issues = None
        with patch.object(self.analyzer, "plot_yearly_trend") as mock_plot:
            self.analyzer.run()
            mock_plot.assert_not_called()

if __name__ == "__main__":
    unittest.main()
