from os.path import exists, realpath
from pathlib import Path
from datetime import datetime

from src.facebook_event_aggregator.repo import _normalize_path, _get_repo_path, _generate_commit_message, clone_or_pull_repo, update_repo

from git import Repo, FetchInfo
from git.util import IterableList
from git.exc import GitCommandError

class TestRepo():    
    """Test helper funcs"""
    def test_normalize_path(self):
        assert _normalize_path("../") == realpath("../")
    
    def test_get_repo_path(self, tmp_path: Path):
        assert str(tmp_path.joinpath("test")) == _get_repo_path(tmp_path, "test")

    def test_generate_commit_message(self):
        assert _generate_commit_message() == f'Update from {datetime.now().strftime("%d %m %Y")}'


    def clone_or_pull_shortcut(self, tmp_path: Path):
        return clone_or_pull_repo(tmp_path, "test", "https://github.com/github/dev.git")

    def test_clone_or_pull(self, tmp_path: Path):
        repo_dir = _get_repo_path(tmp_path, "test")

        assert not exists(repo_dir)
        
        assert type(self.clone_or_pull_shortcut(tmp_path)) == Repo
        assert exists(repo_dir)

        assert type(self.clone_or_pull_shortcut(tmp_path)) == IterableList
        
        
    def test_update_repo(self, tmp_path: Path):
        repo_dir = _get_repo_path(tmp_path, "test")

        assert not exists(repo_dir)
        
        repo = self.clone_or_pull_shortcut(tmp_path)
        
        try:
            generated_commit_msg = _generate_commit_message()  # Do this before so there's less chance of bad timing failing the test
            update_repo(tmp_path, "test", commit_msg=None)
        except GitCommandError:
            pass  # This will return 403, which is normal
        finally:
            assert repo.commit(repo.branches[0]).message == generated_commit_msg
        
        try:
            update_repo(tmp_path, "test", commit_msg="Test succeeded!")
        except GitCommandError:
            pass  # This will return 403, which is normal
        finally:
            assert repo.commit(repo.branches[0]).message == "Test succeeded!"
