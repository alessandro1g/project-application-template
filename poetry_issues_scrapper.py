import requests
import json
import time


# GitHub repository issues API endpoint
repo_url = "https://api.github.com/repos/python-poetry/poetry/issues"

access_token = "nope"
headers = {
    "Authorization": f"token {access_token}"
}

big_issues = []

def fetch_all_issues(repo_url, headers):
    issues = []
    page = 1
    while True:
        # Add pagination parameters
        response = requests.get(repo_url, headers=headers, params={"per_page": 100, "page": page})
        time.sleep(1)
        print(f"Fetching page {page}...")
        if response.status_code != 200:
            print(f"Failed to fetch issues. Status code: {response.status_code}")
            break
        page_issues = response.json()
        if not page_issues:  # Stop if no more issues are returned
            break
        issues.extend(page_issues)
        page += 1
    print(f"Fetched {len(issues)} issues.")
    return issues

def fetch_issue_timeline(url): 
    page = 1
    while True:
        response = requests.get(repo_url, headers=headers, params={"per_page": 50, "page": 1})
        time.sleep(1)
        print(f"Fetching page {page}...")
        if response.status_code != 200:
            print(f"Failed to fetch issues. Status code: {response.status_code}")
            break
        page_issues = response.json()
        if not page_issues:  # Stop if no more issues are returned
            break
        issues.extend(page_issues)
        page += 1
    res = []
    if response.status_code == 200:
        for val in response.json():
            res.append({
                "event_type": val.get("event", "N/A"),  # Use .get() to avoid KeyError
                "author": val.get("actor", {}).get("login", "N/A"),  # Safely access nested keys
                "event_date": val.get("created_at", "N/A"),
                "comment": val.get("body", "")
            })
        return res
    else:
        print(f"Failed to fetch issue timeline. Status code: {response.status_code}")
        return []

# Fetch all issues
issues = fetch_all_issues(repo_url, headers)

for issue in issues: 

    big_issues.append({
        "url": issue["url"],
        "creator": issue["user"]["login"],
        "labels": [label["name"] for label in issue["labels"]],
        "state": issue["state"],
        "assigness": [assignee["login"] for assignee in issue["assignees"]],
        "title": issue["title"],
        "text": issue.get("body", "").replace("\r\n", " ").replace("\r", " "),
        "number": issue["number"],
        "created_date": issue["created_at"],
        "updated_date": issue["updated_at"],
        "timeline_url": issue['timeline_url'],
        "events": fetch_issue_timeline(issue['timeline_url']),
        "response_count": issue.get("comments", 0)  # Add the number of comments
    })

# Save the extracted issues to a JSON file
with open('github_issues.json', 'w') as json_file:
    json.dump(big_issues, json_file, indent=4)