import unittest
from analysis_open_issue_by_creator import AnalyzeOpenIssuesByCreator

class TestAnalyzeOpenIssuesByCreator(unittest.TestCase):
    def setUp(self):
        self.analyzer = AnalyzeOpenIssuesByCreator()

    def test_count_open_issues_by_creator(self):
        issues = [
            {"state": "open", "creator": "vishal"},
            {"state": "closed", "creator": "aless"},
            {"state": "open", "creator": "vishal"},
            {"state": "open", "creator": "aless"},
            {"state": "open"},
        ]
        result = self.analyzer.count_open_issues_by_creator(issues)
        self.assertEqual(result, {"vishal": 2, "aless": 1})

