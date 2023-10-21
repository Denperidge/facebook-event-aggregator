from json import loads, dumps
from pathlib import Path

from dateutil import parser
from datetime import datetime


from src.facebook_event_aggregator.Event import Event
from src.facebook_event_aggregator.utils.url_converter import facebook_locale_to_www, facebook_www_to_locale

class TestEventClass():
    """Test helpers"""
    event = Event(
        name="Test",
        datetime="20 Nov 2023 18:00 UTC+1",
        source="Organisation",
        location="Belgium",
        url="https://en-gb.facebook.com/test"
    )

    def compare_to_original(self, event):
        assert event.name == "Test"
        assert event.datetime == parser.parse("20/11/2023 18:00+1")
        assert event.source == "Organisation"
        assert event.location == "Belgium"
        assert event.url == "https://en-gb.facebook.com/test"


    """Init tests"""
    def test_init(self):
        self.compare_to_original(self.event)

    def test_init_from_dict(self):
        event = Event.from_dict({
            "name":"Test",
            "datetime": "20 Nov 2023 18:00 UTC+1",
            "source": "Organisation",
            "location": "Belgium",
            "url": "https://en-gb.facebook.com/test"
        })
        assert event.to_json() == self.event.to_json()

    """Property tests"""
    def test_clean_url(self):
        assert self.event.clean_url == facebook_locale_to_www(self.event.url)
        assert self.event.clean_url != facebook_www_to_locale(self.event.url)

    def test_description(self):
        assert type(self.event.description) == str
        assert self.event.source in self.event.description
        assert self.event.clean_url in self.event.description
    
    def test_uid(self):
        assert type(self.event.uid) == str
    
    def test_endTime(self):
        assert type(self.event.endTime) == datetime

    # TODO get_image

    """Method tests"""
    def test_to_json(self):
        self.compare_to_original(Event.from_dict(self.event.to_json()))
    
    
    #def test_events_from_json(self, tmp_path: Path):
     #   with open(tmp_path.joinpath("data.json"), "w", encoding="UTF-8") as file:
      #      file.write(f"{"",}")
