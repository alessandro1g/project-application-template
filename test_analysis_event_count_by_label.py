import unittest
from analysis_event_count_by_label import Analyze_Event_Count_By_Label

class TestAnalyzeEventCountByLabel(unittest.TestCase):
    def setUp(self):
        self.analyzer = Analyze_Event_Count_By_Label()

    def test_count_labels_mixed_types(self):
        issues = [
            {"labels": [{"name": "error"}, {"name": "feature"}]},
            {"labels": ["error", "suggestion"]},
            {"labels": []},
            {},
        ]
        result = self.analyzer.count_labels(issues)
        self.assertEqual(result, {"error": 2, "feature": 1, "suggestion": 1})

    def test_count_labels_empty(self):
        issues = []
        result = self.analyzer.count_labels(issues)
        self.assertEqual(result, {})

