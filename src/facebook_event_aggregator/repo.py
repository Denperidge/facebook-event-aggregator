# Built-in imports
from subprocess import run
from os.path import realpath, isdir, join, exists
from datetime import datetime

from git import Repo 

"""This module handles Git repo stuff"""

def _normalize_path(dir):
    return realpath(dir)

def clone_or_pull_repo(parent_dir_path: str, dest_path: str, repo_url: str):
    dest_path = _normalize_path(join(parent_dir_path, dest_path))

    if not exists(dest_path):
        return Repo.clone_from(repo_url, dest_path)
    else:
        return Repo(dest_path).remote("origin").pull()
        
    
def update_repo(dir, commit_msg=None):
    dir = _normalize_path(dir)
    if commit_msg is None:
        current_date = datetime.now().strftime("%d %m %Y")
        commit_msg = "Update from {}".format(current_date)
    
    print(commit_msg)

    
    repo.index.add(".")
    repo.index.commit()
    repo.remote("origin").push()


# Thanks to https://stackoverflow.com/questions/3258243/check-if-pull-needed-in-git#comment20583319_12791408
# & https://stackoverflow.com/a/17938274
def pull_update_if_needed(dir):
    _git_command(dir, "fetch")
    fetch = int(run("git rev-list HEAD...@{u} --count", cwd=dir, encoding="UTF-8", capture_output=True, shell=True).stdout)
    if fetch == 0:
        return False
    else:
        _git_command(dir, "pull")
        return True
        
