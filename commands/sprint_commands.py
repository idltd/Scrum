from utils.file_handler import read_data, write_data
from utils.git_handler import create_branch, switch_to_master, merge_branch, delete_branch
from datetime import datetime, timedelta

__module_description__ = "Manage sprints"
__module_importance__ = 2

def sprint_create(name, duration=14):
    """
    Create a new sprint.

    Usage: scrum sprint create <name> [duration]
    duration: Sprint duration in days (default: 14)
    """
    data = read_data()
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

def sprint_list():
    """
    List all sprints.

    Usage: scrum sprint list
    """
    data = read_data()
    if not data['sprints']:
        print("No sprints found.")
        return
    
    for sprint in data['sprints']:
        status = "CURRENT" if sprint['id'] == data['current_sprint_id'] else sprint['status']
        print(f"[{sprint['id']}] {sprint['name']} ({status})")
        print(f"    Start: {sprint['start_date']}, End: {sprint['end_date']}")
        print(f"    Items: {len(sprint['items'])}")
        print()

def sprint_start(sprint_id):
    """
    Start a sprint and create a Git branch for it.

    Usage: scrum sprint start <sprint_id>
    """
    data = read_data()
    sprint = next((s for s in data['sprints'] if s['id'] == int(sprint_id)), None)
    if not sprint:
        print(f"Sprint {sprint_id} not found.")
        return
    
    if data['current_sprint_id']:
        print("Cannot start a new sprint while another is in progress.")
        return
    
    branch_name = f"sprint_{sprint['id']}"
    if create_branch(branch_name):
        sprint['status'] = 'In Progress'
        data['current_sprint_id'] = sprint['id']
        write_data(data)
        print(f"Started sprint: {sprint['name']} (ID: {sprint['id']})")
    else:
        print("Failed to start sprint due to Git branch creation error.")

def sprint_end(sprint_id):
    """
    End a sprint and merge its Git branch.

    Usage: scrum sprint end <sprint_id>
    """
    data = read_data()
    sprint = next((s for s in data['sprints'] if s['id'] == int(sprint_id)), None)
    if not sprint:
        print(f"Sprint {sprint_id} not found.")
        return
    
    if data['current_sprint_id'] != sprint['id']:
        print("Can only end the current active sprint.")
        return
    
    branch_name = f"sprint_{sprint['id']}"
    if switch_to_master() and merge_branch(branch_name):
        sprint['status'] = 'Completed'
        data['current_sprint_id'] = None
        write_data(data)
        print(f"Ended sprint: {sprint['name']} (ID: {sprint['id']})")
    else:
        print("Failed to end sprint due to Git merge error.")

def sprint_abandon(sprint_id):
    """
    Abandon a sprint and delete its Git branch.

    Usage: scrum sprint abandon <sprint_id>
    """
    data = read_data()
    sprint = next((s for s in data['sprints'] if s['id'] == int(sprint_id)), None)
    if not sprint:
        print(f"Sprint {sprint_id} not found.")
        return
    
    if data['current_sprint_id'] != sprint['id']:
        print("Can only abandon the current active sprint.")
        return
    
    branch_name = f"sprint_{sprint['id']}"
    if switch_to_master() and delete_branch(branch_name):
        sprint['status'] = 'Abandoned'
        data['current_sprint_id'] = None
        write_data(data)
        print(f"Abandoned sprint: {sprint['name']} (ID: {sprint['id']})")
    else:
        print("Failed to abandon sprint due to Git branch deletion error.")

def sprint_add_item(sprint_id, item_id):
    """
    Add a backlog item to a sprint.

    Usage: scrum sprint add-item <sprint_id> <item_id>
    """
    data = read_data()
    sprint = next((s for s in data['sprints'] if s['id'] == int(sprint_id)), None)
    if not sprint:
        print(f"Sprint {sprint_id} not found.")
        return
    
    item = next((i for i in data['backlog'] if i['id'] == int(item_id)), None)
    if not item:
        print(f"Backlog item {item_id} not found.")
        return
    
    if item['id'] in sprint['items']:
        print(f"Item {item_id} is already in the sprint.")
        return
    
    sprint['items'].append(item['id'])
    item['sprint_id'] = sprint['id']
    write_data(data)
    print(f"Added item {item_id} to sprint {sprint_id}")

def sprint_remove_item(sprint_id, item_id):
    """
    Remove a backlog item from a sprint.

    Usage: scrum sprint remove-item <sprint_id> <item_id>
    """
    data = read_data()
    sprint = next((s for s in data['sprints'] if s['id'] == int(sprint_id)), None)
    if not sprint:
        print(f"Sprint {sprint_id} not found.")
        return
    
    if int(item_id) not in sprint['items']:
        print(f"Item {item_id} is not in sprint {sprint_id}.")
        return
    
    sprint['items'].remove(int(item_id))
    item = next((i for i in data['backlog'] if i['id'] == int(item_id)), None)
    if item:
        item['sprint_id'] = None
    write_data(data)
    print(f"Removed item {item_id} from sprint {sprint_id}")

def sprint_show(sprint_id):
    """
    Show details of a specific sprint.

    Usage: scrum sprint show <sprint_id>
    """
    data = read_data()
    sprint = next((s for s in data['sprints'] if s['id'] == int(sprint_id)), None)
    if not sprint:
        print(f"Sprint {sprint_id} not found.")
        return
    
    print(f"Sprint: {sprint['name']} (ID: {sprint['id']})")
    print(f"Status: {sprint['status']}")
    print(f"Start Date: {sprint['start_date']}")
    print(f"End Date: {sprint['end_date']}")
    print(f"Items:")
    for item_id in sprint['items']:
        item = next((i for i in data['backlog'] if i['id'] == item_id), None)
        if item:
            print(f"  [{item['id']}] {item['description']} - {item['status']}")
        else:
            print(f"  [ERROR] Item {item_id} not found in backlog")