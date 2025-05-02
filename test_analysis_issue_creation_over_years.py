import unittest
from unittest.mock import patch
from analysis_issue_creation_over_years import AnalyzeIssueCreationOverYears

class TestAnalyzeIssueCreationOverYears(unittest.TestCase):
    def setUp(self):
        self.analyzer = AnalyzeIssueCreationOverYears()

    def test_count_issues_by_year_valid_dates(self):
        issues = [
            {"created_date": "2022-01-01T12:00:00Z"},
            {"created_date": "2022-05-10T15:00:00Z"},
            {"created_date": "2023-03-15T09:00:00Z"},
        ]
        result = self.analyzer.count_issues_by_year(issues)
        self.assertEqual(result, {2022: 2, 2023: 1})

    def test_count_issues_by_year_invalid_date(self):
        issues = [
            {"created_date": "not-a-date"},
            {"created_date": "2022-01-01T12:00:00Z"},
        ]
        
        result = self.analyzer.count_issues_by_year(issues)
        self.assertEqual(result, {2022: 1})

    def test_count_issues_by_year_missing_date(self):
        issues = [
            {},
            {"created_date": None},
            {"created_date": "2021-12-31T23:59:59Z"},
        ]
        result = self.analyzer.count_issues_by_year(issues)
        self.assertEqual(result, {2021: 1})

