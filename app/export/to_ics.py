# Built-in imports
from sys import argv
from os.path import realpath, dirname, join
from json import load

# Package imports
from dateutil import parser
from ics import Calendar, Event

# Local imports
from repo import update_repo

def events_to_ics(events, output_dir):
    output_dir = realpath(output_dir)
    ics_all = join(output_dir, "all.ics")

    calendar = Calendar()
    for raw_event in events:
        event = Event()
        event.name = raw_event["name"]
        event.begin = parser.parse(raw_event["datetime"])
        event.location = raw_event["location"]
        event.url = raw_event["url"]

        calendar.events.add(event)
        

    with open(ics_all, "w") as file:
        file.writelines(calendar.serialize_iter())


# For testing:
# - python to_ics.py path/to/events.json
if __name__ == "__main__":
    events_json = realpath(argv[1])
    dir = dirname(events_json)

    with open(events_json, "r") as file:
        events = load(file)
    
    events_to_ics(events)

    update_repo(dir)
