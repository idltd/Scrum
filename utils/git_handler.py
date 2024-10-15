import subprocess

def git_command(command):
    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        return False, e.stderr

def is_git_repository():
    success, _ = git_command(['git', 'rev-parse', '--is-inside-work-tree'])
    return success

def create_branch(branch_name):
    success, output = git_command(['git', 'checkout', '-b', branch_name])
    if success:
        print(f"Created and switched to new branch: {branch_name}")
    else:
        print(f"Failed to create branch: {output}")
    return success

def switch_to_master():
    success, output = git_command(['git', 'checkout', 'master'])
    if success:
        print("Switched to master branch")
    else:
        print(f"Failed to switch to master branch: {output}")
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