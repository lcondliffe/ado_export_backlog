# Azure DevOps Backlog Exporter

This script exports all open features, user stories, and tasks from an Azure DevOps board to JSON files.

## Prerequisites

- Python 3.6+
- An Azure DevOps Personal Access Token (PAT) with "Work Items - Read" permissions.

## Installation

1.  Clone this repository.
2.  Install the required Python packages:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

1.  Set the following environment variables:

    - `ADO_ORGANIZATION`: Your Azure DevOps organization name.
    - `ADO_PROJECT`: Your Azure DevOps project name.
    - `ADO_PAT`: Your Azure DevOps Personal Access Token.
    - `ADO_AREA_PATH`: The area path to filter by (e.g., "MyProject\MyTeam").

2.  Run the script:

    ```bash
    python ado_export.py
    ```

3.  The exported data will be saved in the `output` directory in the following files:

    - `features.json`
    - `user_stories.json`
    - `tasks.json`

