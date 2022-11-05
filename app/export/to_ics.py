# Built-in imports
from sys import argv
from os import makedirs
from os.path import realpath, dirname, join
from json import load

# Package imports
from dateutil import parser
from ics import Calendar, Event as IcsEvent

# Local imports
from repo import update_repo
from Event import load_events_from_json
from export.to_html import slugify

def events_to_ics(events, output_dir):
    output_dir = join(realpath(output_dir), "ical/")
    makedirs(output_dir, exist_ok=True)
    ics_all = join(output_dir, "all.ics")

    all_calendar = Calendar()
    source_calendars = dict()

    sources = set([event.source for event in events])
    for source in sources:
        source_calendars[source] = Calendar()
    

    for event in events:
        ics_event = IcsEvent()
        ics_event.name = event.name
        ics_event.begin = event.datetime
        # organizer also requires email
        #ics_event.organizer = event.organizer
        ics_event.location = event.location
        ics_event.url = event.url

        ics_event.description = event.description

        all_calendar.events.add(ics_event)
        source_calendars[event.source].events.add(ics_event)
        

    with open(ics_all, "w") as file:
        file.writelines(all_calendar.serialize_iter())
    
    for source in source_calendars:
        dest = join(output_dir, slugify(source) + ".ics")
        calendar = source_calendars[source]

        with open(dest, "w") as file:
            file.writelines(calendar.serialize_iter())


# For testing:
# - python to_ics.py path/to/events.json
if __name__ == "__main__":
    events_json = realpath(argv[1])
    dir = dirname(events_json)

    events = load_events_from_json(events_json)


    events_to_ics(events, dir)

    update_repo(dir)
