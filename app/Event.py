# Built-in imports
from copy import deepcopy
from json import load, dump

# Package imports
from datetime import timedelta
from dateutil import parser

# Local imports
from scrape_and_parse.locale import facebook_locale_to_www

class Event(object):
    """
    name = str
    datetime = date
    url = str
    """


    def __init__(self, name, datetime, location, url=""):
        self.name = name
        # Replacement due to bug ? https://github.com/dateutil/dateutil/issues/70#issuecomment-945080282
        self.datetime = parser.parse(datetime.replace("UTC", ""))
        self.location = location
        self.url = url
    
    # Thanks to https://stackoverflow.com/a/682545 & https://www.programiz.com/python-programming/methods/built-in/classmethod
    @classmethod
    def from_dict(cls, dict):
        return cls(
            name=dict["name"], 
            datetime=dict["datetime"],
            location=dict["location"],
            url=dict["url"]
            )
    
    def to_json(self):
        serializable_event = deepcopy(self)
        serializable_event.datetime = self.datetime.isoformat()
        return serializable_event.__dict__
    
    def clean_url(self):
        url = facebook_locale_to_www(self.url)
        url = url[:url.index("?")]
        return url
    
    # See Add To Calendar Button documentation: https://github.com/add2cal/add-to-calendar-button#typical-structure
    def endTime(self):
        return self.datetime + timedelta(hours=2)

def load_events_from_json(json_path):
    events = []
    with open(json_path, "r") as file:
        raw_events = load(file)
        for raw_event in raw_events:
            event = Event.from_dict(raw_event)
            events.append(event)
    return events

def events_to_json(events, json_path):
    serializable_events = []
    for event in events:
        serializable_events.append(event.to_json())
    
    with open(json_path, "w") as file:
        dump(serializable_events, file)
