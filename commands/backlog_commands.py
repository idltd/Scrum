from utils.file_handler import read_data, write_data

__module_description__ = "Manage the project backlog"
__module_importance__ = 1

def backlog_add(description):
    """
    Add a new item to the backlog.

    Usage: scrum backlog add <description>
    """
    data = read_data()
    new_id = data['next_item_id']
    data['backlog'].append({
        'id': new_id,
        'description': description,
        'status': 'Not Started',
        'estimate': None,
        'sprint_id': None
    })
    data['next_item_id'] += 1
    write_data(data)
    print(f"Added backlog item {new_id}: {description}")

def backlog_list(filter='all'):
    """
    List items in the backlog.

    Usage: scrum backlog list [filter]
    Filters: all, unassigned, in-progress, complete
    """
    data = read_data()
    items = data['backlog']
    if filter != 'all':
        items = [item for item in items if item['status'].lower() == filter.lower()]
    for item in items:
        print(f"{item['id']}: {item['description']} - {item['status']} ({item['extimate']})")

def backlog_update(item_id, status=None, estimate=None, **kwargs):
    """
    Update a backlog item's status or estimate.

    Usage: 
    scrum backlog update <item_id> <status> [estimate]
    scrum backlog update <item_id> --status <status> [--estimate <estimate>]
    """
    data = read_data()
    item = next((item for item in data['backlog'] if item['id'] == int(item_id)), None)
    
    if not item:
        print(f"Item {item_id} not found")
        return

    # Handle positional arguments
    if status is not None:
        item['status'] = status
    if estimate is not None:
        item['estimate'] = int(estimate)
    
    # Handle named arguments (overrides positional if both are provided)
    if 'status' in kwargs:
        item['status'] = kwargs['status']
    if 'estimate' in kwargs:
        item['estimate'] = int(kwargs['estimate'])

    write_data(data)
    print(f"Updated item {item_id}")
    print(f"Status: {item['status']}")
    print(f"Estimate: {item['estimate']}")

# Add more backlog commands as needed