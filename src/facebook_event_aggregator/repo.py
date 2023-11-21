# Built-in imports
from subprocess import run
from os.path import realpath, isdir, join, exists
from datetime import datetime

from git import Repo 

"""This module handles Git repo stuff"""

def _normalize_path(dir) -> str:
    return realpath(dir)

def _get_repo_path(parent_dir_path, repo_path) -> str:
    repo_path = _normalize_path(join(str(parent_dir_path), str(repo_path)))
    return repo_path

def _generate_commit_message():
    current_date = datetime.now().strftime("%d %m %Y")
    commit_msg = "Update from {}".format(current_date)
    return commit_msg


def clone_or_pull_repo(parent_dir_path, clone_dirname, repo_url: str):
    repo_path = _get_repo_path(parent_dir_path, clone_dirname)

    if not exists(repo_path):
        return Repo.clone_from(repo_url, repo_path)
    else:
        return Repo(repo_path).remote("origin").pull()

    
def update_repo(parent_dir_path, clone_dirname, commit_msg=None):
    repo_path = _get_repo_path(parent_dir_path, clone_dirname)
    
    if commit_msg is None:
        commit_msg = _generate_commit_message()
    
    repo = Repo(repo_path)
    
    repo.index.add("-A")
    repo.index.commit(commit_msg)
    repo.remote("origin").push()
