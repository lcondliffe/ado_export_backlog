import os
import requests
import json
import argparse

# Configuration
PAT = os.environ.get("ADO_PAT")

# API Version
API_VERSION = "7.1-preview.2"

def get_work_item_ids(organization, project, pat, area_path):
    """
    Get all work item IDs in the project.
    """
    url = f"https://dev.azure.com/{organization}/{project}/_apis/wit/wiql?api-version={API_VERSION}"
    headers = {
        "Content-Type": "application/json",
    }
    auth = ("", pat)
    # In Azure DevOps, the area path in queries should be prefixed with the project name.
    full_area_path = f"{project}\\{area_path}"
    query = {
        "query": f"SELECT [System.Id] FROM workitems WHERE [System.TeamProject] = '{project}' AND [System.AreaPath] = '{full_area_path}' AND [System.State] <> 'Closed' AND [System.State] <> 'Removed'"
    }

    response = requests.post(url, headers=headers, auth=auth, data=json.dumps(query))
    response.raise_for_status()
    work_items = response.json()["workItems"]
    return [item["id"] for item in work_items]

def get_work_item_details(organization, project, pat, ids):
    """
    Get the details for a list of work item IDs.
    """
    url = f"https://dev.azure.com/{organization}/{project}/_apis/wit/workitems?ids={','.join(map(str, ids))}&api-version={API_VERSION}"
    headers = {
        "Content-Type": "application/json",
    }
    auth = ("", pat)

    response = requests.get(url, headers=headers, auth=auth)
    response.raise_for_status()
    return response.json()["value"]

def main():
    """
    Main function.
    """
    parser = argparse.ArgumentParser(description="Export Azure DevOps work items.")
    parser.add_argument("--organization", required=True, help="Azure DevOps organization")
    parser.add_argument("--project", required=True, help="Azure DevOps project")
    parser.add_argument("--area-path", required=True, help="Azure DevOps area path")
    args = parser.parse_args()

    if not PAT:
        print("Please set the ADO_PAT environment variable.")
        return

    print("Fetching work item IDs...")
    work_item_ids = get_work_item_ids(args.organization, args.project, PAT, args.area_path)
    print(f"Found {len(work_item_ids)} work items.")

    if not work_item_ids:
        print("No work items found.")
        return

    print("Fetching work item details...")
    work_item_details = []
    batch_size = 100
    for i in range(0, len(work_item_ids), batch_size):
        batch_ids = work_item_ids[i:i + batch_size]
        details = get_work_item_details(args.organization, args.project, PAT, batch_ids)
        work_item_details.extend(details)
        print(f"Fetched details for {len(work_item_details)} of {len(work_item_ids)} work items.")

    print(f"Fetched details for {len(work_item_details)} work items.")

    # Filter for open features, user stories, and tasks
    features = []
    user_stories = []
    tasks = []

    for item in work_item_details:
        item_type = item["fields"]["System.WorkItemType"]
        if item_type == "Feature":
            features.append(item)
        elif item_type == "User Story":
            user_stories.append(item)
        elif item_type == "Task":
            tasks.append(item)

    # Create output directory
    if not os.path.exists("output"):
        os.makedirs("output")

    # Write results to JSON files
    with open("output/features.json", "w") as f:
        json.dump(features, f, indent=4)
    with open("output/user_stories.json", "w") as f:
        json.dump(user_stories, f, indent=4)
    with open("output/tasks.json", "w") as f:
        json.dump(tasks, f, indent=4)

    print("Export complete.")
    print(f"  - Features: {len(features)}")
    print(f"  - User Stories: {len(user_stories)}")
    print(f"  - Tasks: {len(tasks)}")


if __name__ == "__main__":
    main()