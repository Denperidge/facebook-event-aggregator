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
        events.hide(400);  // Hide all events
        // Besides of the selected source
        $(`${eventSelector}.${sourceFilter.attr("id")}`).show(400);
    } else {
        sourceFilter.attr("role", "");
        events.show(400);
    }
    
});
