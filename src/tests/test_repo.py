from os.path import exists, realpath
from pathlib import Path

from src.facebook_event_aggregator.repo import _normalize_path, clone_or_pull_repo, update_repo, pull_update_if_needed

from git import Repo, FetchInfo
from git.util import IterableList

class TestRepo():
    def repo_dest(self, tmp_path: Path):
        return tmp_path.joinpath("test")
    
    def clone_or_pull_shortcut(self, tmp_path: Path):
        return clone_or_pull_repo(str(self.repo_dest(tmp_path)), "test", "https://github.com/github/dev.git")

    def test_normalize_path(self):
        assert _normalize_path("../") == realpath("../")
    
    def clone_repo_if_not_exists(self, tmp_path: Path):
        assert not self.repo_dest(tmp_path).exists()
        
        assert type(self.clone_or_pull_shortcut(tmp_path)) == Repo
        assert self.repo_dest.exists()

        assert type(self.clone_or_pull_shortcut(tmp_path)) == IterableList[FetchInfo]
        
    def test_update_repo(self, tmp_path: Path):
        assert not self.repo_dest(tmp_path).exists()
        
        repo = self.clone_or_pull_shortcut(tmp_path)
        
