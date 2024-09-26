from utils.file_handler import read_data, write_data

__module_description__ = "Manage the overall Scrum project"
__module_importance__ = 0  # Highest importance

def scrum_init(project_name):
    """
    Initialize a new Scrum project.

    Usage: scrum init <project_name>
    """
    data = {
        "project_name": project_name,
        "backlog": [],
        "sprints": [],
        "current_sprint_id": None,
        "next_item_id": 1,
        "next_sprint_id": 1
    }
    write_data(data)
    print(f"Initialized new Scrum project: {project_name}")

def scrum_info():
    """
    Display information about the current Scrum project.

    Usage: scrum info
    """
    data = read_data()
    print(f"Project: {data['project_name']}")
    print(f"Backlog items: {len(data['backlog'])}")
    print(f"Total sprints: {len(data['sprints'])}")
    print(f"Current sprint: {data['current_sprint_id'] or 'None'}")

# Add more scrum-level commands as needed