import requests
import json
import time


# GitHub repository issues API endpoint
repo_url = "https://api.github.com/repos/python-poetry/poetry/issues"

access_token = ""
headers = {
    "Authorization": f"token {access_token}"
}

big_issues = []

def fetch_all_issues(repo_url, headers):
    issues = []
    page = 1
    while True:
        # Add pagination parameters
        response = requests.get(repo_url, headers=headers, params={"per_page": 1000, "page": page})
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

def fetch_issue_timeline(url, count): 
    res = []
    if url != "":
        page = 1
        print(count)
        while True:
            response = requests.get(url, headers=headers, params={"per_page": 1000, "page": page})
            time.sleep(1)
            print(f"Fetching page {page}...")
            if response.status_code != 200:
                print(f"Failed to fetch issues. Status code: {response.status_code}")
                break
            page_issues = response.json()
            if not page_issues:  # Stop if no more issues are returned
                break
            for val in page_issues:
                res.append({
                    "event_type": val.get("event", "N/A"),  # Use .get() to avoid KeyError
                    "author": (val.get("actor") or {}).get("login", "N/A"),  # Ensure actor is a dictionary
                    "event_date": val.get("created_at", "N/A"),
                    "comment": val.get("body", "")
                })
            page += 1
    return res

# Fetch all issues
issues = fetch_all_issues(repo_url, headers)

count = 0
for issue in issues: 
    count += 1
    if issue is not None: 
        big_issues.append({
            "url": issue.get("url"),
            "creator": issue.get("user", {}).get("login", "N/A"),  # Safely access the "login" key
            "labels": [label["name"] for label in issue.get("labels", [])],
            "state": issue.get("state", ""),
            "assigness": [assignee["login"] for assignee in issue.get("assignees", "")],
            "title": issue.get("title", ""),
            "text": issue.get("body", ""),
            "number": issue.get("number", ""),
            "created_date": issue.get("created_at", ""),
            "updated_date": issue.get("updated_at", ""),
            "closed_date": issue.get("closed_at", ""),
            "timeline_url": issue.get('timeline_url', ""),
            "events": fetch_issue_timeline(issue.get('timeline_url', []), count),
            "response_count": issue.get("comments", 0)  # Add the number of comments
        })
# Save the extracted issues to a JSON file
with open('github_issues.json', 'w') as json_file:
    json.dump(big_issues, json_file, indent=4)