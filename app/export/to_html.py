# Built-in imports
from os.path import realpath, dirname, join
from sys import argv
from json import load

# Package imports
from dateutil import parser
from jinja2 import FileSystemLoader, Environment

# Local imports
from Event import load_events_from_json

template_dir = join(realpath(dirname(__file__)), "templates")
env = Environment(
    loader=FileSystemLoader(template_dir),
    autoescape=True
)

def events_to_html(events, output_dir):
    template_index = env.get_template("index.html")
    
    output = template_index.render(events=events)

    filename_index = join(output_dir, "index.html")
    with open(filename_index, "w") as file:
        file.writelines(output)



if __name__ == "__main__":
    events_json = realpath(argv[1])
    dir = dirname(events_json)

    events = load_events_from_json(events_json)

    events_to_html(events, dir)