import json
import os

DATA_FILE = 'scrum_data.json'

def read_data():
    if not os.path.exists(DATA_FILE):
        return {"project_name": "", "backlog": [], "sprints": [], "current_sprint_id": None, "next_item_id": 1, "next_sprint_id": 1}
    
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

def write_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)