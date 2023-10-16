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
