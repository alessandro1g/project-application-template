import unittest
from analysis_issue_per_event import AnalyzeIssuePerEvent

class TestAnalyzeIssuePerEvent(unittest.TestCase):
    def setUp(self):
        self.analyzer = AnalyzeIssuePerEvent()

    def test_extract_event_counts(self):
        issues = [
            {"events": [1, 2, 3]},
            {"events": []},
            {"events": [1]},
            {},
        ]
        result = self.analyzer.extract_event_counts(issues)
        self.assertEqual(result, [3, 0, 1, 0])

    def test_categorize_event_counts(self):
        event_counts = [0, 1, 2, 6, 12, 17, 22]
        result = self.analyzer.categorize_event_counts(event_counts)
        expected = {"0": 1, "1-5": 2, "6-10": 1, "11-15": 1, "16-20": 1, "21+": 1}
        self.assertEqual(result, expected)

