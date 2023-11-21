# Built-in imports
from os import getenv, listdir, remove
from os.path import realpath, dirname, join, isfile
from pathlib import Path
from sys import argv
from json import load
from datetime import datetime

# Package imports
from dateutil import parser
from jinja2 import FileSystemLoader, Environment, PrefixLoader, PackageLoader, DictLoader
from slugify import slugify

# Local imports
from ..Event import load_events_from_json
from .templates.workaround import templates


try:
    #loader = PackageLoader("htmlexport")
    template_dir = join(realpath(dirname(__file__)), "templates")
    loader = FileSystemLoader(template_dir)
except:
    loader = DictLoader(templates)

jinja_env = Environment(
    loader=loader,
    autoescape=True,
    trim_blocks=True,  # Thanks to https://stackoverflow.com/a/35777386
    lstrip_blocks=True,
)

jinja_env.filters["slug"] = slugify


# img_dir: absolute path to look for in images
# img_path_relative_to_index: relative path from index.html to where images are stored on the host
# See Event.py
def events_to_html(
        events: list, 
        absolute_img_dir: str, 
        relative_from_html_img_dir: str,
        page_urls: list, 
        output_dir: str,
        title="Document Title",
        host_domain="https://domain.example.com",
        timezone="Europe/London"):
    """
    events: Events to export
    page_urls: 
    """
    template_index = jinja_env.get_template("index.html")

    sources = set([event.source for event in events])
    
    output = template_index.render(
        # 
        events=events,
        # Absolute image
        image_dir=absolute_img_dir,
        # Image path to be used in html to load images
        img_path_relative_to_index=relative_from_html_img_dir,
        title=title,
        domain=host_domain,
        timezone=timezone,
        pages=page_urls,
        sources=sources,
        now=datetime.now())

    filename_index = join(output_dir, "index.html")
    with open(filename_index, "w") as file:
        file.writelines(output)
    
    return output



# if __name__ == "__main__":
#     events_json = realpath(argv[1])
#     dir = dirname(events_json)

#     events = load_events_from_json(events_json)

#     events_to_html(events, dir)