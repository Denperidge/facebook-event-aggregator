
from datetime import datetime
from pathlib import Path

from src.facebook_event_aggregator.Event import Event
from src.facebook_event_aggregator.export.to_html import events_to_html

test_event_one = Event(
    name="Underscores - Botanique",
    datetime=str(datetime.now()),
    source="Botanique",
    location="Brussels",
    url="https://www.facebook.com/events/3483289855332151"
)

test_event_two = Event(
    name="Chase Petra - Trix",
    datetime=str(datetime.now()),
    source="Trix",
    location="Antwerp",
    url="https://www.facebook.com/events/956264055785138/"
)

example = {
    "events": [test_event_one, test_event_two],
    "title": "Concerts",
    "host_domain": "https://concerts.example.com",
    
    "page_urls": ["https://www.facebook.com/botaniquebxl", "https://www.facebook.com/trixonline"],
    "timezone": "Europe/Brussels"
}


def test_events_to_html(tmp_path: Path):
    events_to_html(
        events=example["events"],
        absolute_img_dir=tmp_path.joinpath("images"),
        relative_from_html_img_dir="images/",
        page_urls=example["page_urls"],
        output_dir=tmp_path,
        title=example["title"],
        host_domain=example["host_domain"],
        timezone=example["timezone"]
    )

    with open(tmp_path.joinpath("index.html"), encoding="UTF-8") as file:
        data = file.read()
        for item in example.values():
            if type(item) == list:
                for value in item:
                    if not isinstance(value, Event):
                        assert value in data
                    else:
                        for property in [value.name, value.description, value.location, value.clean_url]:
                            assert property in data
                        
            
            else:
                assert item in data
