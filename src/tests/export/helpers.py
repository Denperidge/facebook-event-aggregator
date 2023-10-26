from pathlib import Path
from datetime import datetime

from src.facebook_event_aggregator.Event import Event

test_event_one = Event(
    name="Underscores - Botanique",
    datetime_param=str(datetime.now()),
    source="Botanique",
    location="Brussels",
    url="https://www.facebook.com/events/3483289855332151"
)

test_event_two = Event(
    name="Chase Petra - Trix",
    datetime_param=str(datetime.now()),
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


def check_event_contents_in(event: Event, haystack):
    for property in [event.name, event.description, event.location, event.clean_url]:
        assert property in haystack

def write_test_ics(path):
    with open(path.joinpath(str(path)), "w", encoding="UTF-8") as file:
        file.write(
            """
BEGIN:VCALENDAR
VERSION:2.0
PRODID:ics.py - http://git.io/RANDOM
BEGIN:VEVENT
CREATED:20151219T021727Z
DTEND;TZID=America/Toronto:20170515T110000
DTSTAMP:20151219T021727Z
DTSTART;TZID=America/Toronto:20170515T100000
LAST-MODIFIED:20151219T021727Z
RRULE:FREQ=DAILY;UNTIL=20170519T035959Z
SEQUENCE:0
SUMMARY:Meeting
TRANSP:OPAQUE
UID:21B97459-D97B-4B23-AF2A-E2759745C299
END:VEVENT
END:VCALENDAR
""")
        
        