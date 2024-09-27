import os
import json

SCRUM_FILE = 'scrum.json'

def check_scrum_file():
    if not os.path.exists(SCRUM_FILE):
        print(f"Error: {SCRUM_FILE} not found. Please initialize the project first.")
        print("Run 'scrum init' to initialize the project.")
        return False
    return True

def read_data():
    if not check_scrum_file():
        return None
    with open(SCRUM_FILE, 'r') as f:
        return json.load(f)

def write_data(data):
    with open(SCRUM_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def init_project(project_name):
    if os.path.exists(SCRUM_FILE):
        print(f"Error: {SCRUM_FILE} already exists. Project is already initialized.")
        return False

    initial_data = {
        "project_name": project_name,
        "backlog": [],
        "sprints": [],
        "current_sprint_id": None,
        "next_item_id": 1,
        "next_sprint_id": 1
    }

    write_data(initial_data)
    print(f"Initialized Scrum project '{project_name}' and created {SCRUM_FILE}")
    return True

def get_project_name():
    data = read_data()
    return data['project_name'] if data else None