# Built-in imports
from subprocess import run
from os.path import realpath, isdir, join
from datetime import datetime

"""
This module handles Git repo initialisating


GitPython is not used because:
- It still requires an active Git installation
- Currently in maintenance mode
- The git commands needed in this are very basic
"""

# Commands meant for internal use
def git_command(dir, *commands):
    for command in commands:
        run("git {}".format(command), cwd=dir, shell=True)

def normalize_path(dir):
    return realpath(dir)

# Commands meant for external use
def clone_repo_if_not_exists(parent_dir, dest_dirname):
    dest_dirname = normalize_path(join(parent_dir, dest_dirname))

    if not isdir(dest_dirname):
        repo_url = input("Git repo URL: ")
        git_command(parent_dir, "clone {0} {1}".format(repo_url, dest_dirname))

        
    
def update_repo(dir, commit_msg=None):
    dir = normalize_path(dir)
    if commit_msg is None:
        current_date = datetime.now().strftime("%d %m %Y")
        commit_msg = "Update from {}".format(current_date)
    
    print(commit_msg)

    git_command(dir,
        "pull",
        "add .", 
        "commit -m \"{}\"".format(commit_msg),
        "push origin main"
        )


# Thanks to https://stackoverflow.com/questions/3258243/check-if-pull-needed-in-git#comment20583319_12791408
# & https://stackoverflow.com/a/17938274
def pull_update_if_needed(dir):
    git_command(dir, "fetch")
    fetch = int(run("git rev-list HEAD...@{u} --count", cwd=dir, encoding="UTF-8", capture_output=True, shell=True).stdout)
    if fetch == 0:
        return False
    else:
        git_command(dir, "pull")
        return True
        
