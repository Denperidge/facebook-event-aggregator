from json import loads, dumps

from dateutil import parser


from src.facebook_event_aggregator.Event import Event

class TestEventClass():
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

    def test_to_json(self):
        self.compare_to_original(Event.from_dict(self.event.to_json()))
    
