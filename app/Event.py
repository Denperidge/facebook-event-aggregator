# Built-in imports
from copy import deepcopy
from json import load, dump
from os.path import join, basename
from glob import glob

# Package imports
from datetime import timedelta
from dateutil import parser
from slugify import slugify

# Local imports
from scrape_and_parse.locale import facebook_locale_to_www

class Event(object):
    """
    name = str
    datetime = date
    url = str
    """


    def __init__(self, name, datetime, source, location, url):
        self.name = name
        # Replacement due to bug ? https://github.com/dateutil/dateutil/issues/70#issuecomment-945080282
        self.datetime = parser.parse(datetime.replace("UTC", ""))
        self.location = location
        self.url = url
        self.source = source
    
    # Thanks to https://stackoverflow.com/a/682545 & https://www.programiz.com/python-programming/methods/built-in/classmethod
    @classmethod
    def from_dict(cls, dict):
        return cls(
            name=dict["name"], 
            datetime=dict["datetime"],
            source=dict["source"],
            location=dict["location"],
            url=dict["url"]
            )
    
    
    def to_json(self):
        serializable_event = deepcopy(self)
        serializable_event.datetime = self.datetime.isoformat()
        return serializable_event.__dict__
    
    @property
    def description(self):
        return "Organized by {0}. See {1} for more info".format(self.source, self.clean_url)
    
    @property
    def clean_url(self):
        url = facebook_locale_to_www(self.url)
        if "?" in url:
            url = url[:url.index("?")]
        return url
    
    # Thanks to https://www.geeksforgeeks.org/getter-and-setter-in-python/
    @property
    def uid(self):
        # Facebook allows double entries of the same event, but in different times.
        # So the URL + datetime should be unique
        return slugify(self.clean_url) + slugify(self.datetime.isoformat())
    
    # See Add To Calendar Button documentation: https://github.com/add2cal/add-to-calendar-button#typical-structure
    @property
    def endTime(self):
        return self.datetime + timedelta(hours=2)
    
    """
    Okay so this is a doozy.
    - Glob is being used to future proof, in case of png or jpg or jpeg. That's good.
    - But it requires a local path to find the image
    - But that path cannot be relative. Originally this was passed img_dir=public/img,
      which then got public/ removed to img/filename.png.
      That works when running from the project dir! When run in C:/ProjectDir, it will
      look in C:/ProjectDir/public/img, find the thing, and replace as said above

      But the glob will fail when run from a different folder
      Cause then it will look for the file in C:/Differentdir/public/img and return None

    So this function got redesigned to not return ANY path, and instead just a filename.
    With optionally a relative path added as a paremeter

   
    """
    def get_image(self, image_dir, return_with_path=None):
        try:
            image_glob_str = join(image_dir, self.uid + "*")
            filename_no_path = basename(glob(image_glob_str)[0])

            if not return_with_path:
                filename = filename_no_path
            else:
                filename = join(return_with_path, filename_no_path)

            return filename

        except IndexError:
            print("No image found for " + self.uid)
            return None
        
        

def load_events_from_json(json_path):
    events = []
    with open(json_path, "r") as file:
        raw_events = load(file)
        for raw_event in raw_events:
            event = Event.from_dict(raw_event)
            events.append(event)
    return events

def events_to_json(events, json_path):
    serializable_events = []
    for event in events:
        serializable_events.append(event.to_json())
    
    with open(json_path, "w") as file:
        dump(serializable_events, file)
