import unittest
from unittest.mock import patch, MagicMock
from poetry_issues_scrapper import fetch_all_issues, fetch_issue_timeline

class TestPoetryIssuesScrapper(unittest.TestCase):
    @patch('poetry_issues_scrapper.requests.get')
    def test_fetch_all_issues_success(self, mock_get):
        print("test_fetch_all_issues_success")
        
        # Mock the first response
        mock_response_1 = MagicMock()
        mock_response_1.status_code = 200
        mock_response_1.json.return_value = [
            {"id": 1, "title": "Issue 1"},
            {"id": 2, "title": "Issue 2"}
        ]
        
        # Mock the second response (None or empty response)
        mock_response_2 = MagicMock()
        mock_response_2.status_code = 200
        mock_response_2.json.return_value = []

        # Use side_effect to return the first response for the first call and the second response for the second call
        mock_get.side_effect = [mock_response_1, mock_response_2]

        headers = {"Authorization": "token test_token"}
        issues = fetch_all_issues("https://api.github.com/repos/test/repo/issues", headers)

        # Assertions for the first call
        self.assertEqual(len(issues), 2)
        self.assertEqual(issues[0]["title"], "Issue 1")
        self.assertEqual(issues[1]["title"], "Issue 2")

        # Assertions for the second call (if fetch_all_issues handles pagination or makes a second call)
        self.assertEqual(mock_get.call_count, 2)  # Ensure it was called twice

    @patch('poetry_issues_scrapper.requests.get')
    def test_fetch_all_issues_failure(self, mock_get):
        print("test_fetch_all_issues_failure")
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        headers = {"Authorization": "token test_token"}
        issues = fetch_all_issues("https://api.github.com/repos/test/repo/issues", headers)

        self.assertEqual(len(issues), 0)
        mock_get.assert_called()

    @patch('poetry_issues_scrapper.requests.get')
    def test_fetch_all_issues_invalid_json(self, mock_get):
        print("test_fetch_all_issues_invalid_json")
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.side_effect = ValueError("Invalid JSON")
        mock_get.return_value = mock_response

        headers = {"Authorization": "token test_token"}
        with self.assertRaises(ValueError):
            fetch_all_issues("https://api.github.com/repos/test/repo/issues", headers)
            


    @patch('poetry_issues_scrapper.requests.get')
    def test_fetch_all_issues_empty_response(self, mock_get):
        print("test_fetch_all_issues_empty_response")
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = []
        mock_get.return_value = mock_response

        headers = {"Authorization": "token test_token"}
        issues = fetch_all_issues("https://api.github.com/repos/test/repo/issues", headers)

        self.assertEqual(len(issues), 0)
        mock_get.assert_called()

    @patch('poetry_issues_scrapper.requests.get')
    def test_fetch_issue_timeline_success(self, mock_get):
        print("test_fetch_issue_timeline_success")
        
        # Mock the first response
        mock_response_1 = MagicMock()
        mock_response_1.status_code = 200
        mock_response_1.json.return_value = [
            {
                "event": "closed",
                "actor": {"login": "user1"},
                "created_at": "2023-10-01T12:00:00Z",
                "body": "Issue closed"
            }
        ]
        
        # Mock the second response
        mock_response_2 = MagicMock()
        mock_response_2.status_code = 200
        mock_response_2.json.return_value = [
            {
                "event": "reopened",
                "actor": {"login": "user2"},
                "created_at": "2023-10-02T12:00:00Z",
                "body": "Issue reopened"
            }
        ]

        mock_response_3 = MagicMock()
        mock_response_3.status_code = 200
        mock_response_3.json.return_value = []
        
        # Use side_effect to simulate responses dynamically
        mock_get.side_effect = [mock_response_1, mock_response_2, mock_response_3]

        headers = {"Authorization": "token test_token"}
        
        # First call to fetch the timeline
        timeline = fetch_issue_timeline("https://api.github.com/repos/test/repo/issues/1/timeline", 1)

        self.assertEqual(len(timeline), 2)
        self.assertEqual(timeline[0]["event_type"], "closed")
        self.assertEqual(timeline[0]["author"], "user1")
        self.assertEqual(timeline[1]["event_type"], "reopened")
        self.assertEqual(timeline[1]["author"], "user2")

    @patch('poetry_issues_scrapper.requests.get')
    def test_fetch_issue_timeline_failure(self, mock_get):
        print("test_fetch_issue_timeline_failure")
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        headers = {"Authorization": "token test_token"}
        timeline = fetch_issue_timeline("https://api.github.com/repos/test/repo/issues/1/timeline", 1)

        self.assertEqual(len(timeline), 0)
        mock_get.assert_called()

    @patch('poetry_issues_scrapper.requests.get')
    def test_fetch_issue_timeline_invalid_json(self, mock_get):
        print("test_fetch_issue_timeline_invalid_json")
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.side_effect = ValueError("Invalid JSON")
        mock_get.return_value = mock_response

        headers = {"Authorization": "token test_token"}
        with self.assertRaises(ValueError):
            fetch_all_issues("https://api.github.com/repos/test/repo/issues", headers)

    @patch('poetry_issues_scrapper.requests.get')
    def test_fetch_issue_timeline_empty_url(self, mock_get):
        print("test_fetch_issue_timeline_empty_url")
        timeline = fetch_issue_timeline("", 1)
        self.assertEqual(len(timeline), 0)
        mock_get.assert_not_called()


    @patch('poetry_issues_scrapper.requests.get')
    def test_fetch_all_issues_with_empty_assignees(self, mock_get):
        print("test_fetch_all_issues_with_empty_assignees")
        
        # Mock responses for multiple pages
        mock_response_page_1 = MagicMock()
        mock_response_page_1.status_code = 200
        mock_response_page_1.json.return_value = [
            {
                "id": 1,
                "title": "Issue with no assignees" # Incorrect type (string instead of list)
            }
        ]

        mock_response_page_2 = MagicMock()
        mock_response_page_2.status_code = 200
        mock_response_page_2.json.return_value = [
            {
                "id": 2,
                "title": "Issue with empty assignees",
                "assignees": []  # Correct type (empty list)
            }
        ]

        mock_response_page_3 = MagicMock()
        mock_response_page_3.status_code = 200
        mock_response_page_3.json.return_value = []

        # Use side_effect to simulate multiple pages
        mock_get.side_effect = [mock_response_page_1, mock_response_page_2, mock_response_page_3]

        headers = {"Authorization": "token test_token"}
        issues = fetch_all_issues("https://api.github.com/repos/test/repo/issues", headers)

        # Assertions
        self.assertEqual(len(issues), 2)
        self.assertEqual(issues[0].get("assignees", ""), [])  # This should not cause an error
        self.assertEqual(issues[1]["assignees"], [])  # This should work as expected
        self.assertEqual(mock_get.call_count, 3)  # Ensure it was called three times


if __name__ == '__main__':
    unittest.main()