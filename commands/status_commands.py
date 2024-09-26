from utils.file_handler import read_data

__module_description__ = "Get an overview of the current system status"
__module_importance__ = 1

def status_overview():
    """
    Display an overview of the current project status.

    Usage: scrum status overview
    """
    data = read_data()
    print(f"Project: {data['project_name']}")
    print(f"\nBacklog:")
    print(f"  Total items: {len(data['backlog'])}")
    statuses = {}
    for item in data['backlog']:
        statuses[item['status']] = statuses.get(item['status'], 0) + 1
    for status, count in statuses.items():
        print(f"  {status}: {count}")
    
    print(f"\nSprints:")
    print(f"  Total sprints: {len(data['sprints'])}")
    current_sprint = next((s for s in data['sprints'] if s['id'] == data['current_sprint_id']), None)
    if current_sprint:
        print(f"  Current sprint: {current_sprint['name']} (ID: {current_sprint['id']})")
        print(f"    Start date: {current_sprint['start_date']}")
        print(f"    End date: {current_sprint['end_date']}")
        sprint_items = [item for item in data['backlog'] if item['sprint_id'] == current_sprint['id']]
        print(f"    Items: {len(sprint_items)}")
    else:
        print("  No active sprint")

def status_sprint(sprint_id=None):
    """
    Display detailed status of a specific sprint or the current sprint.

    Usage: scrum status sprint [sprint_id]
    """
    data = read_data()
    if not sprint_id:
        sprint_id = data['current_sprint_id']
    
    sprint = next((s for s in data['sprints'] if s['id'] == int(sprint_id)), None)
    if not sprint:
        print(f"Sprint {sprint_id} not found")
        return
    
    print(f"Sprint: {sprint['name']} (ID: {sprint['id']})")
    print(f"Status: {sprint['status']}")
    print(f"Start date: {sprint['start_date']}")
    print(f"End date: {sprint['end_date']}")
    
    sprint_items = [item for item in data['backlog'] if item['sprint_id'] == sprint['id']]
    print(f"\nItems ({len(sprint_items)}):")
    for item in sprint_items:
        print(f"  [{item['id']}] {item['description']} - {item['status']}")

# Add more status commands as needed