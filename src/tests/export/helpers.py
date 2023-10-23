from datetime import datetime

from src.facebook_event_aggregator.Event import Event

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
