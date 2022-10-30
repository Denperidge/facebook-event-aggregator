# Sociaalisme

A Facebook event scraper & aggregator, that displays multiple groups' events in a website and .ics file. Without needing a back-end!

## Structure
For more in depth or WIP notes, see [dev-notes](dev-notes.md)

1. `step-1.py` Scrapes the information from Facebook and turns that data into JSON.
2. `step-2.js` Turns the JSON data into...
    1. A static website
    2. A .ical link
3. 

## Maintaining
This application is made to be as platform-agnostic as possible. However, the weak link is in the Facebook scraping. The parse_* functions in [step-1.py](app/step-1.py) are most likely to need changes. So if the application doesn't find any events, look there first.


## Installing
```bash
pip install -r requirements.txt

```

## Configuring
- If run locally, set the pages you want to scrape in .env. An example file is provided in [.env.example]!
- If run on GitHub Actions, set a secret called "pages" in the repositories secrets, with for the rest the same value as you'd do in the local .env

## Contributing

Make sure to run `pipreqs` following command if any modules get added to a python file.
(Note: pipreqs seems to have some issues with the match statement. If that's still the case, comment those lines out before running)
