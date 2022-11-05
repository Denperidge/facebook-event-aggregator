# Built-in imports
from json import load

# Package imports
from dateutil import parser

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

def load_events_from_json(json_path):
    events = []
    with open(json_path, "r") as file:
        raw_events = load(file)
        for raw_event in raw_events:
            event = Event.from_dict(raw_event)
            events.append(event)
    return events
