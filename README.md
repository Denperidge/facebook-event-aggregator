# Sociaalisme

A Facebook event scraper & aggregator, that displays multiple groups' events in a website and .ics file. Without needing a back-end!

## Structure
For more in depth or WIP notes, see [dev-notes](dev-notes.md)

1. Scrape the information from Facebook.
2. Parse that data into JSON.
3. Run a script that turns the JSON data into...
    1. A static website
    2. A .ical link
4. 

## Maintaining
This application is made to be as platform-agnostic as possible. However, the weak link is in the Facebook scraping. The parse_* functions in [step-1.py](app/step-1.py) are most likely to need changes. So if the application doesn't find any events, look there first.


## Installing
```bash
pip install -r requirements.txt

```

## Contributing

Make sure to run `pipreqs` following command if any modules get added to a python file.
(Note: pipreqs seems to have some issues with the match statement. If that's still the case, comment those lines out before running)
