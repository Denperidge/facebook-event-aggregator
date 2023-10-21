from os.path import exists, realpath
from pathlib import Path

from src.facebook_event_aggregator.repo import _git_command, _normalize_path, clone_repo_if_not_exists, update_repo, pull_update_if_needed


class TestRepo():

    def test_git_command(self, tmp_path: Path):
        dotgit = tmp_path.joinpath(".git")

        assert not exists(dotgit)

        # TODO: a second command that can be tested
        _git_command(tmp_path, "init", "add .")
        
        assert exists(dotgit)


    def test_normalize_path(self):
        assert _normalize_path("../") == realpath("../")
    

    def clone_repo_if_not_exists(self, tmp_path: Path):
        dest_dirname = "test"
        dest_dirpath = tmp_path.joinpath(dest_dirname)
        assert not dest_dirpath.exists()
        clone_repo_if_not_exists(str(tmp_path), dest_dirname, "https://github.com/github/dev.git")
        
        assert dest_dirpath.exists()

        clone_repo_if_not_exists(str(tmp_path), dest_dirname, "https://github.com/github/dev.git")
        

    def test_update_repo(self, tmp_path: Path):
        dest_dirname = "test"
        dest_dirpath = tmp_path.joinpath(dest_dirname)
        clone_repo_if_not_exists(str(tmp_path), dest_dirname, "https://github.com/github/dev.git")
        