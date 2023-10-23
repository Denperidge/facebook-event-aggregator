from pathlib import Path

from ics import Calendar

from src.facebook_event_aggregator.export.to_ics import events_to_ics, _read_ics_if_exists

from .helpers import example, check_event_contents_in, write_test_ics

def test_read_ics_if_exists(tmp_path: Path):

    test_path = tmp_path.joinpath("test.ics")
    
    assert not test_path.exists()
    read_when_not_exist = _read_ics_if_exists(str(test_path))

    assert read_when_not_exist == Calendar()  # Empty calendar
    assert len(read_when_not_exist.events) == 0

    write_test_ics(test_path)
    read_when_exists = _read_ics_if_exists(str(test_path))
    
    assert test_path.exists()
    assert read_when_exists != Calendar()
    assert len(read_when_exists.events) > 0
    



def test_events_to_ics(tmp_path: Path):
    events_to_ics(example["events"], str(tmp_path))

    ical_dir = tmp_path.joinpath("ical/")

    all_filepath = ical_dir.joinpath("all.ics")

    assert ical_dir.joinpath("all.ics").exists()
    with open(str(all_filepath), "r", encoding="utf-8") as all_file:
        all_content = all_file.read()

    for event in example["events"]:
        check_event_contents_in(event, all_content)

        source_filepath = ical_dir.joinpath(event.source.lower() + ".ics")
        assert source_filepath.exists()
        with open(str(source_filepath), "r", encoding="UTF-8") as source_file:
            source_contents = source_file.read()
            check_event_contents_in(event, source_contents)
        
