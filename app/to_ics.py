from ics import Calendar, Event
from json import load
from os import makedirs
from os.path import abspath, join, realpath, dirname
from dotenv import load_dotenv
from dateutil import parser
from repo import update_repo


root_dir = abspath(join(realpath(dirname(__file__)), "../"))
env_file = join(root_dir, ".env")
public_dir = join(root_dir, "public/")
events_json = join(public_dir, "events.json")
all_ics = join(public_dir, "all.ics")
makedirs(public_dir, exist_ok=True)
load_dotenv(env_file)

with open(events_json, "r") as file:
    events = load(file)

calendar = Calendar()
for raw_event in events:
    event = Event()
    event.name = raw_event["name"]
    event.begin = parser.parse(raw_event["datetime"])
    event.location = raw_event["location"]
    event.url = raw_event["url"]

    calendar.events.add(event)

with open(all_ics, "w") as file:
    file.writelines(calendar.serialize_iter())

update_repo(public_dir)
