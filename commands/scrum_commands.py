from utils.file_handler import init_project, read_data
from utils.git_handler import is_git_repository

__module_description__ = "Manage the overall Scrum project"
__module_importance__ = 0  # Highest importance

def scrum_init(project_name):
    """
    Initialize a new Scrum project.

    Usage: scrum init <project_name>
    """
    if not is_git_repository():
        print("Error: Current directory is not a Git repository.")
        print("Please initialize a Git repository before running 'scrum init'.")
        return

    if init_project(project_name):
        print(f"Scrum project '{project_name}' has been initialized.")

def scrum_info():
    """
    Display information about the current Scrum project.

    Usage: scrum info
    """
    data = read_data()
    if not data:
        print("No Scrum project found. Please initialize the project first.")
        return

    print(f"Scrum Project: {data['project_name']}")
    print("\nBacklog:")
    print(f"  Total items: {len(data['backlog'])}")
    
    statuses = {}
    for item in data['backlog']:
        status = item['status']
        statuses[status] = statuses.get(status, 0) + 1
    
    for status, count in statuses.items():
        print(f"  {status}: {count}")

    print("\nSprints:")
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

    completed_sprints = [s for s in data['sprints'] if s['status'] == 'Completed']
    print(f"  Completed sprints: {len(completed_sprints)}")

    planned_sprints = [s for s in data['sprints'] if s['status'] == 'Planned']
    print(f"  Planned sprints: {len(planned_sprints)}")

def scrum_version():
    """
    Display the version of the Scrum CLI tool.

    Usage: scrum version
    """
    print("Scrum CLI version 1.0.0")  # Update this version number as needed

# Add more scrum-level commands as needed