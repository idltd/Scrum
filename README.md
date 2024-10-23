(90% complete - a bit of tweaking needed)

# Scrum
A simple python command line app to manage a backlog and scrums - managing git branches too.  

Mostly written by AI, to my design.

Run the script (python scrum.py) for an 'interactive' mode, or put a command on the command line for simple execution.

CD into your project directory...

Usage: scrum <command> [args]

Available commands:

Scrum - Manage the overall Scrum project  
-  scrum info      -     Display information about the current Scrum project.  
-  scrum init      -     Initialize a new Scrum project.  
-  scrum version   -     Display the version of the Scrum CLI tool.  

Backlog - Manage the project backlog  
 - backlog add      -    Add a new item to the backlog.  
 - backlog list     -    List items in the backlog.  
 - backlog update   -    Update a backlog item's status or estimate.  

Status - Get an overview of the current system status  
 - status overview  -    Display an overview of the current project status.  
 - status sprint    -    Display detailed status of a specific sprint or the current sprint.

Sprint - Manage sprints  
 - sprint abandon   -    Abandon a sprint and delete its Git branch.  
 - sprint add_item  -    Add a backlog item to a sprint.  
 - sprint create    -    Create a new sprint.  
 - sprint end       -    End a sprint and merge its Git branch.  
 - sprint list      -    List all sprints.  
 - sprint remove_item -  Remove a backlog item from a sprint.  
 - sprint show      -    Show details of a specific sprint.  
 - sprint start     -    Start a sprint and create a Git branch for it.  
