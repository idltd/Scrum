import os
import subprocess
import shutil
import json

# Helper functions
def run_command(command):
    result = subprocess.run(command, capture_output=True, text=True)
    print(f"Command: {' '.join(command)}")
    print(f"Output: {result.stdout.strip()}")
    print(f"Error: {result.stderr.strip()}")
    print("---")
    return result

def check_json_file(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
    return data

# Test script
def run_tests():
    # Setup
    test_dir = "scrum_test_project"
    os.makedirs(test_dir, exist_ok=True)
    os.chdir(test_dir)

    # Test 1: Try to use commands before git init and scrum init
    print("Test 1: Commands before initialization")
    run_command(["scrum", "info"])
    run_command(["scrum", "backlog", "add", "Task 1"])

    # Test 2: Initialize git
    print("Test 2: Initialize git")
    run_command(["git", "init"])

    # Test 3: Initialize scrum project
    print("Test 3: Initialize scrum project")
    run_command(["scrum", "init", "Test Project"])

    # Test 4: Check project info
    print("Test 4: Check project info")
    run_command(["scrum", "info"])

    # Test 5: Add backlog items
    print("Test 5: Add backlog items")
    run_command(["scrum", "backlog", "add", "Task 1"])
    run_command(["scrum", "backlog", "add", "Task 2"])
    run_command(["scrum", "backlog", "add", "Task 3"])

    # Test 6: List backlog
    print("Test 6: List backlog")
    run_command(["scrum", "backlog", "list"])

    # Test 7: Create a sprint
    print("Test 7: Create a sprint")
    run_command(["scrum", "sprint", "create", "Sprint 1"])

    # Test 8: Add items to sprint
    print("Test 8: Add items to sprint")
    run_command(["scrum", "sprint", "add-item", "1", "1"])
    run_command(["scrum", "sprint", "add-item", "1", "2"])

    # Test 9: Start sprint
    print("Test 9: Start sprint")
    run_command(["scrum", "sprint", "start", "1"])

    # Test 10: Update item status
    print("Test 10: Update item status")
    run_command(["scrum", "backlog", "update", "1", "--status", "In Progress"])

    # Test 11: Show sprint details
    print("Test 11: Show sprint details")
    run_command(["scrum", "sprint", "show", "1"])

    # Test 12: End sprint
    print("Test 12: End sprint")
    run_command(["scrum", "sprint", "end", "1"])

    # Test 13: Create and abandon sprint
    print("Test 13: Create and abandon sprint")
    run_command(["scrum", "sprint", "create", "Sprint 2"])
    run_command(["scrum", "sprint", "start", "2"])
    run_command(["scrum", "sprint", "abandon", "2"])

    # Test 14: Final project info
    print("Test 14: Final project info")
    run_command(["scrum", "info"])

    # Cleanup
    os.chdir("..")
    shutil.rmtree(test_dir)

if __name__ == "__main__":
    run_tests()