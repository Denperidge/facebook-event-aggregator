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
def init_repo_if_not_exists(dir):
    dir = normalize_path(dir)

    dotgit = join(dir, ".git/")
    if not isdir(dotgit):
        git_command(dir, "init")

        repo_url = input("Git repo URL: ")
        git_command(dir, "clone {} .".format(repo_url))

        
    
def update_repo(dir, commit_msg=None):
    dir = normalize_path(dir)
    if commit_msg is None:
        current_date = datetime.now().strftime("%d %m %Y")
        commit_msg = "Update from {}".format(current_date)
    
    print(commit_msg)

    git_command(dir, 
        "add .", 
        "commit -m \"{}\"".format(commit_msg),
        "push origin main"
        )


