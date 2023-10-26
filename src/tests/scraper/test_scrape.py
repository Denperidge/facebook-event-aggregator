from os.path import join, abspath, dirname

from pathlib import Path

from dateutil import parser

from src.facebook_event_aggregator.scraper.driver import setup_driver
from src.facebook_event_aggregator.scraper.scrape_event_page import scrape_event_page
from src.facebook_event_aggregator.scraper.scrape_events_page import scrape_events_page


def test_scrape_event_page():
    return
    location, image_url = scrape_event_page("file://" + abspath(join(dirname(__file__).replace("\\", "/"), "event_page.htm")))
    assert location == "Le Botanique"
    assert image_url == "https://scontent-bru2-1.xx.fbcdn.net/v/t39.30808-6/384365949_704986814996124_1745966508573235950_n.jpg?stp=dst-jpg_s960x960&_nc_cat=106&ccb=1-7&_nc_sid=5f2048&_nc_ohc=YrHGPpoEZssAX8FBBH7&_nc_oc=AQkB4iDsJKhbaZq2oCPLR0ui77bF_fqimfD7hV3pTDczYXSTcO1tqLKSYFY4YbV-q0I&_nc_ht=scontent-bru2-1.xx&oh=00_AfA6LQP9omvSzhV9fQH8_NVYL8pT2d7rkxnBlOGt87251A&oe=653DDCD4"

def test_scrape_events_page(tmp_path: Path):
    events_page = "file://" + abspath(join(dirname(__file__).replace("\\", "/"), "events_page.htm"))
    events = scrape_events_page(setup_driver(), events_page, str(tmp_path))
    
    things_to_find = [
        {
            # TODO finish datetime tests
            "name": "Business As Usual #2 Money Talks pt 2 in AMOR",
            #"datetime": parser.parse("25 oct 08:00 +2")



        },
        {
            "name": "Coach Party / Trix - HiFive Concert - UITVERKOCHT!"
        },
        {
            "name": "Eric Steckel / Trix"
        },
        {
            "name": "Brass Against / Trix"
        },
        {
            "name": "It It Anita + Godcaster / Trix"
        },
        {
            "name": "Birds in Row + Walfang + Quentin Sauvé / Trix"
        },
        {
            "name": "Vrijdag Vrijdag met Fabulae Dramatis + C I M E + Wendung"
        },
        {
            "name": "Protomartyr + Es + dust / Trix"
        }
    ]

    for event in events:

        assert event.source == "Trix"
        to_find = things_to_find.pop(0)
        assert event.name == to_find["name"]
        assert event.location == "Trix"
        #assert event.location == "Trix"  # TODO: location is not consistent
        print(event.name)
        print(event.source)
        print(event.datetime)
        
        print(event.location)
        print("---")
    