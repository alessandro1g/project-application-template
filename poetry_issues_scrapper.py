import requests
import json

# GitHub repository issues API endpoint
repo_url = "https://api.github.com/repos/python-poetry/poetry/issues"

access_token = "Access_Token"
headers = {
    "Authorization": f"token {access_token}"
}

big_issues = []
# Fetch issues
response = requests.get(repo_url, headers=headers)

def fetch_issue_timeline(url): 
    response = requests.get(url)
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


# Check if the request was successful
if response.status_code == 200:
    issues = response.json()
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
            "timeline_url": f"https://api.github.com/repos/python-poetry/poetry/issues/{issue['number']}/timeline",
            "events": fetch_issue_timeline(f"https://api.github.com/repos/python-poetry/poetry/issues/{issue['number']}/timeline")
        })

else:
    print(f"Failed to fetch issues. Status code: {response.status_code}")
    
    # Save the extracted issues to a JSON file
with open('github_issues.json', 'w') as json_file:
    json.dump(big_issues, json_file, indent=4)
