# Sociaalisme

# How should the app be built & designed?

## Step 1: data source (most important)

### Option A: Link the Facebook app with groups (group-centric)

[Events - Graph API - Documentation - Facebook for Developers](https://developers.facebook.com/docs/graph-api/reference/v15.0/group/events)

+ Would allow for relatively easy addition of other groups, or data sources, if designed right

? Would the groups in question be okay with this? (Alleviating factor is open-sourcing the application, but still)

+ There can be a check for visiibility of the events

Is there a non-group bound event endpoint?

### Option C: Scraping

Lets go bayby

### Option B: Login with Facebook (person-centric)

[Guides - Groups API - Documentation - Facebook for Developers](https://developers.facebook.com/docs/groups-api/guides#getting-groups-for-a-user)

+ Allows people to use it with any groups

- Higher bar of entry, would require a server

+ Would however, probably not require a link to a group

- But this is pretty much just the “your events” ical link?

- this would introduce a very heavy facebook lock-in though

## Step 2: moving the API data from the source to the website

[Webhooks - Documentation - Facebook for Developers](https://developers.facebook.com/docs/graph-api/webhooks/)

Perhaps a webhook → github action? It *looks* like Facebook allows the sending of webhooks

Alternatively chronning it?

There should also be a manual invocation. Perhaps protected by a password? Or by using a pug env variable to make an obscurely named html page that triggers it. Either way, manual refreshing should be a thing.

## Step 3: turning that API data into useable data

### Agnosticism

Important note: this should be platform-agnostic. This application is designed for use with Facebook groups, but it should allow for easy addition of any other sources. Normalize the data here somewhat

### ID-generation to allow for data changes

Event changes: dates and times change. There should be unique id’s for an event, that are the following:

- Replicable: if the ID generated is 100% unique to any past and future iterations, it won’t allow for automatic changes
- Not based on date/time: this is the most likely factor to change. But this should still not rely on location.

There’s a good chance Facebook events will have an ID assigned to them. Is this good enough? Perhaps it can be spun to a more platform-agnostic form (for example, source platform & source id?)

### Future additions

Perhaps a distinction of types? Meeting/protest/etc…

## Step 4: serving the data

### 4A: Website

With PUG & Node.JS a full static website would be possible. Generate one HTML file and one .ical file. Betere performance & less api calls!

[socialisme.denperidge.com](http://socialisme.denperidge.com/) ? If I could get a subdomain of the [socialisme.be](http://socialisme.be) people that’d be cool though

### 4B: Calendar

[GitHub - sebbo2002/ical-generator: ical-generator is a small piece of code which generates ical calendar files](https://github.com/sebbo2002/ical-generator)

Node.JS

[GitHub - spatie/icalendar-generator: Generate calendars in the iCalendar format](https://github.com/spatie/icalendar-generator)

PHP

Host ICS file --> automatic pulls? Test dit met google !!

Filtering within ICS? Is there a built in query system?

## Step 5:

# Service/filenaming structure

## Setup

Attach facebook webhook to the application

## Post-setup

Facebook webhook —> GitHub webhook —> GitHub actions —> app/index.js generates public/data.json —> app/website.pug uses this to create public/index.html, app/calendar.js uses this to create public/index.ics

# Sociaalisme - Notes

/me/events met een page access token geeft de page events

een page access token heeft geen expiry date, en heeft dus mogelijk geen long-lived UAT nodig

pages_show_list & **pages_read_engagement**

This requires the person logging in to be an adiminstrator though, is that worth it ? Will I get permissions for that?

---

Scraping: note the difference between groups, pages, and communities (ugh)

Page: [https://www.facebook.com/LSPPSL.LinkseSocialistischePartij/upcoming_hosted_events](https://www.facebook.com/LSPPSL.LinkseSocialistischePartij/upcoming_hosted_events)