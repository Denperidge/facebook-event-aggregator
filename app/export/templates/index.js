
sourceFilters = document.querySelectorAll("nav a");
for (let i = 0; i < sourceFilters.length; i++) {
    sourceFilter = sourceFilters[i];
    events = document.querySelectorAll("events section")
    sourceFilter.addEventListener("click", (e) => {
        let target = e.target;
        let role = e.target.getAttribute("role");

        // If not pressed before
        console.log(target.role)
        if (role != "button") {
            e.target.setAttribute("role", "button");
        } else {
            
        }

        let selectedId = e.target.id;
        
    });
}
