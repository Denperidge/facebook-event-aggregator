# Built-in imports
from os.path import realpath, dirname, join
from sys import argv
from json import load

# Package imports
from dateutil import parser
from jinja2 import FileSystemLoader, Environment

template_dir = join(realpath(dirname(__file__)), "templates")
env = Environment(
    loader=FileSystemLoader(template_dir),
    autoescape=True
)

def render_to_html(events, output_dir):
    template_index = env.get_template("index.html")
    
    output = template_index.render(events=events)

    filename_index = join(output_dir, "index.html")
    with open(filename_index, "w") as file:
        file.writelines(output)



if __name__ == "__main__":
    events_json = realpath(argv[1])
    dir = dirname(events_json)

    with open(events_json, "r") as file:
        events = load(file)
        for event in events:
            print(event)
            event["datetime"] = parser.parse(event["datetime"])

    render_to_html(events, dir)