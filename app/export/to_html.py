# Built-in imports
from os import getenv, listdir, remove
from os.path import realpath, dirname, join, isfile
from pathlib import Path
from sys import argv
from json import load

# Package imports
from dateutil import parser
from jinja2 import FileSystemLoader, Environment
from slugify import slugify

# Local imports
from Event import load_events_from_json
from scrape_and_parse.scrape_and_parse import read_pages_from_env

template_dir = join(realpath(dirname(__file__)), "templates")
env = Environment(
    loader=FileSystemLoader(template_dir),
    autoescape=True,
    trim_blocks=True,  # Thanks to https://stackoverflow.com/a/35777386
    lstrip_blocks=True,
)

def filter_slugify(value):
    return slugify(value)
env.filters["slug"] = filter_slugify


# This will remove any images in the provided directory that aren't 
def cleanup_images(upcoming_events, directory):
    upcoming_events_slugs = [event.uid for event in upcoming_events]

    files = listdir(directory)
    for filename in files:
        file = join(directory, filename)
        if isfile(file):
            filename_no_ext_or_path = Path(file).stem
            if filename_no_ext_or_path not in upcoming_events_slugs:
                remove(file)
        


def events_to_html(events, output_dir, image_dir):
    template_index = env.get_template("index.html")

    pages = [page[1] for page in read_pages_from_env(replace_locale=False)]
    sources = set([event.source for event in events])
    
    
    output = template_index.render(
        events=events, 
        image_dir=image_dir,
        title=getenv("title"),
        domain=getenv("domain"),
        timezone=getenv("tz", "UTC"),
        pages=pages,
        sources=sources)

    filename_index = join(output_dir, "index.html")
    with open(filename_index, "w") as file:
        file.writelines(output)



if __name__ == "__main__":
    events_json = realpath(argv[1])
    dir = dirname(events_json)

    events = load_events_from_json(events_json)

    events_to_html(events, dir)