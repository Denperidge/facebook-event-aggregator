""" CLASS """
class Event(object):
    """
    name = str
    datetime = date
    url = str
    """


    def __init__(self, name, datetime, location, url=""):
        self.name = name
        # Replacement due to bug ? https://github.com/dateutil/dateutil/issues/70#issuecomment-945080282
        self.datetime = parser.parse(datetime.replace("UTC", "")).isoformat()
        self.location = location
        self.url = url

