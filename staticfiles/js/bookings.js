function toggleDisplayOnChange() {
    console.log("Change detected")
    let divToChange = document.getElementById("div-booking-selections")
    if (divToChange.classList.contains("hide-component")) {
        // Nothing to change
    } else {
        divToChange.classList.add("hide-component");
    };
}

function toggleDisplayOnClick() {
    console.log("Click detected")
    let divToChange = document.getElementById("div-booking-selections")
    if (divToChange.classList.contains("hide-component")) {
        divToChange.classList.remove("hide-component");
    }; 

}
