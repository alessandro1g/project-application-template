import unittest
from analysis_issue_count_by_label import AnalyzeIssueCountByLabel

class TestAnalyzeIssueCountByLabel(unittest.TestCase):
    def setUp(self):
        self.analyzer = AnalyzeIssueCountByLabel()

    def test_count_issue_labels(self):
        issues = [
            {"labels": [{"name": "error"}, {"name": "feature"}]},
            {"labels": ["error", "suggestion"]},
            {"labels": []},
            {},
        ]
        result = self.analyzer.count_issue_labels(issues)
        self.assertEqual(result, {"error": 2, "feature": 1, "suggestion": 1})

    def test_count_issue_labels_empty(self):
        result = self.analyzer.count_issue_labels([])
        self.assertEqual(result, {})

