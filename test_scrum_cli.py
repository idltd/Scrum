import os
import sys
import shutil
import io
from contextlib import redirect_stdout, redirect_stderr
import importlib
import subprocess

# Helper functions
import io
from contextlib import redirect_stdout, redirect_stderr
import importlib
import shlex

def run_command(command):
    print(f"Command: {' '.join(map(shlex.quote, command))}")
    
    stdout = io.StringIO()
    stderr = io.StringIO()
    
    with redirect_stdout(stdout), redirect_stderr(stderr):
        try:
            if 'scrum' in sys.modules:
                importlib.reload(sys.modules['scrum'])
            else:
                importlib.import_module('scrum')
            
            scrum = sys.modules['scrum']
            scrum.main(command)
        except SystemExit:
            pass
        except Exception as e:
            print(f"Error: {str(e)}", file=stderr)
    
    print(f"Output: {stdout.getvalue().strip()}")
    print(f"Error: {stderr.getvalue().strip()}")
    print("---")

def run_git_command(command):
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        print(f"Command: {' '.join(command)}")
        print(f"Output: {result.stdout.strip()}")
        print(f"Error: {result.stderr.strip()}")
    except subprocess.CalledProcessError as e:
        print(f"Command: {' '.join(command)}")
        print(f"Error: {e.stderr.strip()}")
    except FileNotFoundError:
        print(f"Command: {' '.join(command)}")
        print("Error: Git command not found. Make sure Git is installed and in your PATH.")
    print("---")

# Test script
def run_tests():
    # Setup
    test_dir = "scrum_test_project"
    os.makedirs(test_dir, exist_ok=True)
    os.chdir(test_dir)

    # Test 1: Try to use commands before git init and scrum init
    print("Test 1: Commands before initialization")
    run_command(["scrum", "info"])
    run_command(["backlog", "add", "Task 1"])

    # Test 2: Initialize scrum project
    print("Test 3: Initialize scrum project")
    run_command(["scrum", "init", "Test Project"])

    # Test 3: Initialize git
    print("Test 2: Initialize git")
    run_git_command(["git", "init"])
    run_git_command(["git", "commit","-am","initial commit"])

    # Test 4: Check project info
    print("Test 4: Check project info")
    run_command(["scrum", "info"])

    # Test 5: Add backlog items
    print("Test 5: Add backlog items")
    run_command(["backlog", "add", "Task 1"])
    run_command(["backlog", "add", "Task 2"])
    run_command(["backlog", "add", "Task 3"])

    # Test 6: List backlog
    print("Test 6: List backlog")
    run_command(["backlog", "list"])

    # Test 7: Create a sprint
    print("Test 7: Create a sprint")
    run_command(["sprint", "create", "Sprint 1"])

    # Test 8: Add items to sprint
    print("Test 8: Add items to sprint")
    run_command(["sprint", "add_item", "1", "1"])
    run_command(["sprint", "add_item", "1", "2"])

    # Test 9: Start sprint
    print("Test 9: Start sprint")
    run_command(["sprint", "start", "1"])

    # Test 10: Update item status
    print("Test 10: Update item status")
    run_command(["backlog", "update", "1", "--status", "In Progress"])

    # Test 11: Show sprint details
    print("Test 11: Show sprint details")
    run_command(["sprint", "show", "1"])

    # Test 12: End sprint
    print("Test 12: End sprint")
    run_command(["sprint", "end", "1"])

    # Test 13: Create and abandon sprint
    print("Test 13: Create and abandon sprint")
    run_command(["sprint", "create", "Sprint 2"])
    run_command(["sprint", "start", "2"])
    run_command(["sprint", "abandon", "2"])

    # Test 14: Final project info
    print("Test 14: Final project info")
    run_command(["scrum", "info"])

    # Cleanup
    os.chdir("..")
    shutil.rmtree(test_dir)

if __name__ == "__main__":
    run_tests()