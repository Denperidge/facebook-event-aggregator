# TODO stop using this
templates = {
    "base.css": """
body {
    width: 80%;
    margin: auto;
}
    """,
    "base.html": """
<!DOCTYPE html>
<html lang="{% block lang %}en{% endblock lang %}">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <!-- https://picocss.com/ -->
    <link rel="stylesheet" href="https://unpkg.com/@picocss/pico@latest/css/pico.min.css">

    <style>
        {% include "base.css" %}
    </style>

    <title>{{ title|default("Facebook Event Aggregator") }}</title>

    {% block head %}
    {% endblock head %}
</head>
<body>
    {% block body %}
    {% endblock %}
</body>
</html>
    """,
    "index.html": """
{% extends "base.html" %}

{% block head %}
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/add-to-calendar-button@1/assets/css/atcb.min.css">
{% endblock head %}

{% block body %}
<main>
    <h1>{{ title }}</h1>
    <section>
        <h2>Upcoming Events</h2>

        <nav>
            <ul id="sources">
                <li>Filter:</li>
                {% for source in sources %}
                <li><a href="#" id="{{ source|slug }}">{{ source }}</a></li>
                {% endfor %}
            </ul>
        </nav>

        <div id="events" class="grid">
            {% for event in events %}
            <article class="{{ event.source|slug }}">

                <img src="{{ event.get_image_filename(image_dir, img_path_relative_to_index) }}"/>
                
                <h3>{{ event.name }}</h3>
    
                <p>{{ event.datetime.strftime("%H:%M - %A %d %b %Y") }}</p>
                {% if event.location %}
                <p>@ {{ event.location }}</p>
                {% endif %}
                {% if event.source %}
                <p>Organised by {{ event.source }}</p>
                {% endif %}
                {% if event.url %}
                <a href="{{ event.url }}" target="_blank">View on Facebook</a>
                {% endif %}
                
                <br><br>

                <div class="atcb" style="display: none;">
                    {# As of writing, icsFile only has affect on direct ics downloads. Manual setting is either way required, and thus preferred #}
                    {
                        {# Event info #}
                        "name": "{{ event.name }}",
                        "startDate": "{{ event.datetime.strftime("%Y-%m-%d") }}",
                        "startTime": "{{ event.datetime.strftime("%H:%M") }}",
                        "endTime": "{{ event.endTime.strftime("%H:%M") }}",
                        {#
                            Requires name|email
                        "organizer": "{{ event.organizer }}", 
                        #}
                        "location": "{{ event.location }}",
                        "description": "{{ event.description|escape }}",
                        "timeZone": "{{ timezone }}",
                        "uid": "{{ event.uid }}",

                        {# atcb configuration #}
                        "label": "Add {{ event.name|truncate(12, killwords=False)|escape }} to your Calendar",
                        "iCalFileName": "{{ event.uid }}",

                        "options": ["Apple", "Google|Google Calendar", "Microsoft365", "Outlook.com", "Yahoo", "iCal|iCal (.ics file)"],
                        "trigger": "click",
                        "listStyle": "overlay",
                        "lightMode": "system"
                    }
                </div>
            </article>
            {% endfor %}
        </div>
    </section>

    {% if domain %}
    <section>
        <h2>Calendar feeds</h2>
        <p>If you want to, you can also subscribe to an ical/.ics feed (sometimes called public url).<br>This will automatically add any events added here to your own calendar.</p>
        <ul class="grid">
            <li>Subscribe to all pages & communities listed here: <input type="url" value="{{ domain }}/ical/all.ics" readonly></li>
            {% for source in sources %}
                <li>
                    <label>Subscribe to {{ source }}: </label>
                    <input type="url" readonly value="{{ domain }}/ical/{{ source|slug }}.ics">
                </li>
            {% endfor %}
        </ul>
    </section>
    {% endif %}

    <section id="pages">
        <h2>Pages & communities</h2>
        <p>Check out the pages and communities that organise these events!</p>
        <ul>
            {% for page in pages %}
            <li><a href="{{ page }}" target="_blank">{{ page }}</a></li>
            {% endfor %}
        </ul>
        <p>(Note: this page is not made by the owners of the pages/communities listed above)</p>
    </section>
</main>

<footer class="grid">
    <span>
        Events collected & page generated using
        <a href="https://github.com/Denperidge/facebook-event-aggregator">Facebook Event Aggregator</a>.
    </span>
    <span>CSS Stylesheet by <a href="https://picocss.com/" target="_blank">Pico.css</a></span>
    <span>Calendar buttons by <a href="https://add-to-calendar-button.com/" target="_blank">ATCB</a></span>
    <span id="last-update">Last update: <span id="{{ now.isoformat() }}">{{ now.strftime("%H:%M, %D") }}</span></span>
</footer>

<script src="https://cdn.jsdelivr.net/npm/jquery@3.6.1/dist/jquery.min.js"></script>
<!-- https://github.com/add2cal/add-to-calendar-button -->
<script src="https://cdn.jsdelivr.net/npm/add-to-calendar-button@1" async defer></script>
<script>{% include "index.js" %}</script>
{% endblock body %}
    """,
    "index.js": """
$(document).ready(function() {
    sourceFilters = $("nav a");
    eventSelector = "#events article";
    events = $(eventSelector);

    sourceFilters.on("click", function(e) {
        sourceFilter = $(e.target);
        console.log(sourceFilter.attr("id"))

        // If not pressed before,
        if (sourceFilter.attr("role") != "button") {
            sourceFilters.attr("role", "");  // Disable any other active buttons
            sourceFilter.attr("role", "button");  // Activate the current

            let selectedEvents = $(`${eventSelector}.${sourceFilter.attr("id")}`);

            events.not(selectedEvents).hide(400);  // Hide all events
            // Besides of the selected source
            selectedEvents.show(400);
        } else {
            sourceFilter.attr("role", "");
            events.show(400);
        }
    });

    lastUpdateElement = $("#last-update span").first();
    lastUpdate = Date.parse(lastUpdateElement.attr("id"));
    // Thanks to https://stackoverflow.com/a/5511376
    let yesterday = new Date();
    yesterday.setDate(yesterday.getDate() - 1);

    if (lastUpdate < yesterday) {
        lastUpdateElement.css("color", "red");
    }

    
});

    """
}