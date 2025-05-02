import unittest
from unittest.mock import patch
from datetime import datetime, timezone
from analysis_open_issue_duration import AnalyzeOpenIssueDurationMonths

class TestAnalyzeOpenIssueDurationMonths(unittest.TestCase):
    def setUp(self):
        self.analyzer = AnalyzeOpenIssueDurationMonths()

    @patch("analysis_open_issue_duration.datetime")
    def test_invalid_date_format(self, mock_datetime):
        now = datetime(2025, 5, 1, tzinfo=timezone.utc)
        mock_datetime.now.return_value = now
        mock_datetime.fromisoformat.side_effect = lambda s: datetime.fromisoformat(s)
        issues = [
            {"state": "open", "created_date": "2025-04-01T00:00:00+00:00"},
            {"state": "open", "created_date": "not-a-date"},
            {"state": "open", "created_date": "2025-03-01T00:00:00+00:00"},
        ]
        durations = self.analyzer.get_open_issue_durations_months(issues)
        self.assertEqual(len(durations), 2)
        self.assertTrue(all(isinstance(d, float) for d in durations))

if __name__ == "__main__":
    unittest.main()


