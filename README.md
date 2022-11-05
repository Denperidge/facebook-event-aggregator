# Sociaalisme

A Facebook event scraper & aggregator, that displays multiple groups' events in a static website and .ics file.

## Structure
For more in depth or WIP notes, see [dev-notes](dev-notes.md)

1. `step-1.py` Scrapes the information from Facebook and turns that data into JSON.
2. `step-2.py` Turns the JSON data into...
    1. A static website
    2. A .ical link
3. `step-3.py` Uploads the data to GitHub Pages

This is all done locally, as to avoid the login sequence that Facebook asks when this is run from GitHub Actions (presumably due to rate limiting). The non-logged in Facebook interface is easier to scrape, presumably due to GraphQL (although that might be incorrect).

## Maintaining
This application is made to be as platform-agnostic as possible. However, the weak link is in the Facebook scraping. The parse_* functions in [step-1.py](app/step-1.py) are most likely to need changes. So if the application doesn't find any events, look there first.


## Installing
Prerequisites: >= py3.10, pip, git

If running on a platform without an official Chromium distrubition (e.g. Raspberry Pi 3b, Linux32...): `apt-get install chromium-chromedriver`

```bash
git clone https://github.com/Denperidge/facebook-event-aggregator.git
cd facebook-event-aggregator
pip install -r requirements.txt
echo "Run app/main.py once in case the output repo hasn't been set up yet"
echo "Command example: python3 $(pwd)/app/main.py"
echo ""
echo "Optionally, add the following line to crontab to automatically run every 24 hours (can be modified ofcourse): "
echo "0 5 * * * python3 \"$(pwd)/app/main.py\" headless update"
```
See also [crontab guru](https://crontab.guru/)!

## Configuring/usage
- Set the pages you want to scrape in .env. An example file is provided in [.env.example]!
- Run using `python3 app/main.py`. Do this at least once before automating to set up Git repo URL.

|  Startup arg   | Functionality |
| -------------- | ------------- |
| `headless` | Run Selenium in headless mode | 
| `update` | Push any changes from public/ output to the repository |
| `noscrape` | Don't scrape, and instead just load info from the existing events.json |



| .env (file) parameter | Functionality |
| --------------------- | -------------- |
| `pages`               | Which Facebook event pages have to be scraped. A JSON string of nested lists ([["page_type", "page_url"], ["page_type", "page_url]]) |
| `title` | (Recommended) The title of index.html
| `facebook_email`     | (Optional) The email of a Facebook account with which you want to scrape, in case you want to be logged in during. | 
| `facebook_password` | (Optional) The password of the Facebook account, in case you want to be logged in during. |

<details>
    <summary>Don't forget to configure Git on the device if that's not done already!</summary>
    ```bash
    git config --global user.email "you@example.com"
    git config --global user.name "Your Name"
    ``` 
</details>


## Contributing

Make sure to run `pipreqs` following command if any modules get added to a python file.
(Note: pipreqs seems to have some issues with the match statement. If that's still the case, comment those lines out before running)
