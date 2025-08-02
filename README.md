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

1.  Set the `ADO_PAT` environment variable:

    ```bash
    export ADO_PAT="your_personal_access_token"
    ```

2.  Run the script with the following command-line arguments:

    ```bash
    python ado_export.py \
        --organization "Your-Azure-DevOps-Organization" \
        --project "Your-Azure-DevOps-Project" \
        --area-path "Your-Area-Path"
    ```

3.  The exported data will be saved in the `output` directory in the following files:

    - `features.json`
    - `user_stories.json`
    - `tasks.json`