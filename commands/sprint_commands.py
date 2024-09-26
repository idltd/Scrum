import os
import json
import subprocess
from datetime import datetime, timedelta

DATA_FILE = 'scrum_data.json'

__module_description__ = "Manage sprints"
__module_importance__ = 2

def check_scrum_file():
    if not os.path.exists(DATA_FILE):
        print("Error: The scrum_data.json file does not exist. Please ensure you are in the correct project directory.")
        return False
    return True

def read_data():
    if not check_scrum_file():
        return None
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

def write_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def git_command(command):
    try:
        subprocess.run(command, check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        print(f"Git command failed: {e.stderr}")
        return False
    return True

def sprint_create(name, duration=14):
    """
    Create a new sprint.

    Usage: scrum sprint create <name> [duration]
    duration: Sprint duration in days (default: 14)
    """
    data = read_data()
    if not data:
        return
    
    start_date = datetime.now().strftime("%Y-%m-%d")
    end_date = (datetime.now() + timedelta(days=int(duration))).strftime("%Y-%m-%d")
    
    new_sprint = {
        'id': data['next_sprint_id'],
        'name': name,
        'start_date': start_date,
        'end_date': end_date,
        'status': 'Planned',
        'items': []
    }
    
    data['sprints'].append(new_sprint)
    data['next_sprint_id'] += 1
    write_data(data)
    print(f"Created new sprint: {name} (ID: {new_sprint['id']})")

def sprint_start(sprint_id):
    """
    Start a sprint and create a Git branch for it.

    Usage: scrum sprint start <sprint_id>
    """
    data = read_data()
    if not data:
        return
    
    sprint = next((s for s in data['sprints'] if s['id'] == int(sprint_id)), None)
    if not sprint:
        print(f"Sprint {sprint_id} not found.")
        return
    
    if data['current_sprint_id']:
        print("Cannot start a new sprint while another is in progress.")
        return
    
    branch_name = f"sprint_{sprint['id']}"
    if not git_command(['git', 'checkout', '-b', branch_name]):
        return
    
    sprint['status'] = 'In Progress'
    data['current_sprint_id'] = sprint['id']
    write_data(data)
    print(f"Started sprint: {sprint['name']} (ID: {sprint['id']}) and created branch: {branch_name}")

def sprint_end(sprint_id):
    """
    End a sprint and merge its Git branch.

    Usage: scrum sprint end <sprint_id>
    """
    data = read_data()
    if not data:
        return
    
    sprint = next((s for s in data['sprints'] if s['id'] == int(sprint_id)), None)
    if not sprint:
        print(f"Sprint {sprint_id} not found.")
        return
    
    if data['current_sprint_id'] != sprint['id']:
        print("Can only end the current active sprint.")
        return
    
    branch_name = f"sprint_{sprint['id']}"
    if not git_command(['git', 'checkout', 'main']) or \
       not git_command(['git', 'merge', branch_name]):
        return
    
    sprint['status'] = 'Completed'
    data['current_sprint_id'] = None
    write_data(data)
    print(f"Ended sprint: {sprint['name']} (ID: {sprint['id']}) and merged branch: {branch_name}")

def sprint_abandon(sprint_id):
    """
    Abandon a sprint and delete its Git branch.

    Usage: scrum sprint abandon <sprint_id>
    """
    data = read_data()
    if not data:
        return
    
    sprint = next((s for s in data['sprints'] if s['id'] == int(sprint_id)), None)
    if not sprint:
        print(f"Sprint {sprint_id} not found.")
        return
    
    if data['current_sprint_id'] != sprint['id']:
        print("Can only abandon the current active sprint.")
        return
    
    branch_name = f"sprint_{sprint['id']}"
    if not git_command(['git', 'checkout', 'main']) or \
       not git_command(['git', 'branch', '-D', branch_name]):
        return
    
    sprint['status'] = 'Abandoned'
    data['current_sprint_id'] = None
    write_data(data)
    print(f"Abandoned sprint: {sprint['name']} (ID: {sprint['id']}) and deleted branch: {branch_name}")

def sprint_list():
    """
    List all sprints.

    Usage: scrum sprint list
    """
    data = read_data()
    if not data:
        return
    
    if not data['sprints']:
        print("No sprints found.")
        return
    
    for sprint in data['sprints']:
        status = "CURRENT" if sprint['id'] == data['current_sprint_id'] else sprint['status']
        print(f"[{sprint['id']}] {sprint['name']} ({status})")
        print(f"    Start: {sprint['start_date']}, End: {sprint['end_date']}")
        print(f"    Items: {len(sprint['items'])}")
        print()

# ... (other sprint-related functions remain the same)