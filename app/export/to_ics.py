# Built-in imports
from sys import argv
from os.path import realpath, dirname, join
from json import load

# Package imports
from dateutil import parser
from ics import Calendar, Event as IcsEvent

# Local imports
from repo import update_repo
from Event import load_events_from_json

def events_to_ics(events, output_dir):
    output_dir = realpath(output_dir)
    ics_all = join(output_dir, "all.ics")

    calendar = Calendar()
    for event in events:
        ics_event = IcsEvent()
        ics_event.name = event.name
        ics_event.begin = event.datetime
        ics_event.location = event.location
        ics_event.url = event.url

        calendar.events.add(ics_event)
        

    with open(ics_all, "w") as file:
        file.writelines(calendar.serialize_iter())


# For testing:
# - python to_ics.py path/to/events.json
if __name__ == "__main__":
    events_json = realpath(argv[1])
    dir = dirname(events_json)

    events = load_events_from_json(events_json)


    events_to_ics(events, dir)

    update_repo(dir)
