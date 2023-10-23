from pathlib import Path

from src.facebook_event_aggregator.export.to_ics import events_to_ics

from .helpers import example

def test_events_to_ics(tmp_path: Path):
    events_to_ics(example["events"], str(tmp_path))

    with open(str(tmp_path.joinpath("ical/")))