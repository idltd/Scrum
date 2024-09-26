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
        print(f"{item['id']}: {item['description']} - {item['status']}")

def backlog_update(item_id, status=None, estimate=None):
    """
    Update a backlog item's status or estimate.

    Usage: scrum backlog update <item_id> [--status <new_status>] [--estimate <new_estimate>]
    """
    data = read_data()
    for item in data['backlog']:
        if item['id'] == int(item_id):
            if status:
                item['status'] = status
            if estimate:
                item['estimate'] = int(estimate)
            write_data(data)
            print(f"Updated item {item_id}")
            return
    print(f"Item {item_id} not found")

# Add more backlog commands as needed