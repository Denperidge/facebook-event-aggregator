from pathlib import Path

from src.facebook_event_aggregator.export.utils import cleanup_images
from src.facebook_event_aggregator.Event import Event
from .helpers import example

def assert_exist(path: Path, filenames, exist=True):
    for filename in filenames:
        assert (path.joinpath(filename)).exists() == exist

def test_cleanup_images(tmp_path: Path):
    events = example["events"]
    
    filenames = ["test.png", events[0].uid + ".png", "meow.png", events[1].uid]

    for filename in filenames:
        with open(str(tmp_path.joinpath(filename)), "w", encoding="UTF-8") as file:
            file.write("")
    
    assert_exist(tmp_path, filenames)

    for file in tmp_path.glob("*"):
        print(file)
    
    cleanup_images(events, str(tmp_path))

    for file in tmp_path.glob("*"):
        print(file)


    assert_exist(tmp_path, [filenames[0], filenames[2]], exist=False)
    assert_exist(tmp_path, [filenames[1], filenames[3]], exist=True)
    
        