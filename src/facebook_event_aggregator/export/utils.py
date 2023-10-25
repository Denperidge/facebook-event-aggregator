from os import getenv, listdir, remove
from os.path import realpath, dirname, join, isfile
from pathlib import Path

# This will remove any images in the provided directory that aren't from provided events
def cleanup_images(still_upcoming_events: list, directory: str):
    upcoming_events_slugs = [event.uid for event in still_upcoming_events]

    files = listdir(directory)
    for filename in files:
        file = join(directory, filename)
        if isfile(file):
            filename_no_ext_or_path = Path(file).stem
            if filename_no_ext_or_path not in upcoming_events_slugs:
                remove(file)
