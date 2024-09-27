import subprocess

def git_command(command):
    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        return False, e.stderr

def create_branch(branch_name):
    success, output = git_command(['git', 'checkout', '-b', branch_name])
    if success:
        print(f"Created and switched to new branch: {branch_name}")
    else:
        print(f"Failed to create branch: {output}")
    return success

def switch_to_main():
    success, output = git_command(['git', 'checkout', 'main'])
    if success:
        print("Switched to main branch")
    else:
        print(f"Failed to switch to main branch: {output}")
    return success

def merge_branch(branch_name):
    success, output = git_command(['git', 'merge', branch_name])
    if success:
        print(f"Merged branch {branch_name} into current branch")
    else:
        print(f"Failed to merge branch: {output}")
    return success

def delete_branch(branch_name):
    success, output = git_command(['git', 'branch', '-D', branch_name])
    if success:
        print(f"Deleted branch: {branch_name}")
    else:
        print(f"Failed to delete branch: {output}")
    return success