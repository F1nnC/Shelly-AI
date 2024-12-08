document.addEventListener('DOMContentLoaded', () => {
    getAccountInfo();
});

function getAccountInfo() {
    const requestOptions = {
        method: "GET",
        redirect: "follow"
    };

    const baseUrl = `${window.location.protocol}//${window.location.hostname}${window.location.port ? ':' + window.location.port : ''}`;
    let apiUrl = `${baseUrl}/auth/user`;

    let favorite_spots = [];

    fetch(apiUrl, requestOptions)
        .then((response) => {
            if (!response.ok) {
                throw new Error("HTTP error, status = " + response.status);
            }
            return response.json();
        })
        .then((result) => {
            favorite_spots = result.favorite_spots;
            updatePage(result.username, result.email, result.favorite_spots);
            console.log(favorite_spots);
        })
        .catch((error) => console.error(error));

    apiUrl = `${baseUrl}/spot/get_all_spots`;

    fetch(apiUrl, requestOptions)
        .then((response) => {
            if (!response.ok) {
                throw new Error("HTTP error, status = " + response.status);
            }
            return response.json();
        })
        .then((result) => {
            for (let i = 0; i < result.length; i++) {
                updateSpots(result[i].name, result[i].spot_id, favorite_spots);
            }
        })
        .catch((error) => console.error(error));
}

function addSpot() {
    let spot = document.getElementById("spots");
    let spotName = spot.options[spot.selectedIndex].text;
    let spotId = spot.options[spot.selectedIndex].value;

    const requestOptions = {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        redirect: "follow",
        body: JSON.stringify({ spot_id: spotId, name: spotName })
    };

    const baseUrl = `${window.location.protocol}//${window.location.hostname}${window.location.port ? ':' + window.location.port : ''}`;
    let apiUrl = `${baseUrl}/auth/add_spot`;

    fetch(apiUrl, requestOptions)
        .then((response) => {
            if (!response.ok) {
                throw new Error("HTTP error, status = " + response.status);
            }
            return response.json();
        })
        .then((result) => {
            console.log(result);
            // Dynamically add the spot to the favorite spots list
            addFavoriteSpotToUI(spotName, spotId);
            // Remove the spot from the dropdown
            removeSpotFromDropdown(spotId);
            // Re-add to the dropdown in case user wants to add it again
        })
        .catch((error) => console.error(error));
}

function deleteSpot(spotId) {
    const requestOptions = {
        method: "DELETE",
        headers: { "Content-Type": "application/json" },
        redirect: "follow",
        body: JSON.stringify({ spot_id: spotId })
    };

    const baseUrl = `${window.location.protocol}//${window.location.hostname}${window.location.port ? ':' + window.location.port : ''}`;
    let apiUrl = `${baseUrl}/auth/remove_spot`;

    fetch(apiUrl, requestOptions)
        .then((response) => {
            if (!response.ok) {
                throw new Error("HTTP error, status = " + response.status);
            }
            return response.json();
        })
        .then((result) => {
            console.log(result);
            // Remove the spot from the favorite spots list
            document.getElementById(spotId).remove();
            // Update the dropdown by removing the deleted spot's option
            addDropdown(result.name, spotId);
        })
        .catch((error) => console.error(error));
}

function updatePage(username, email, favorite_spots) {
    document.getElementById("welcome").innerHTML = `Welcome, ${username}`;
    document.getElementById("username").innerHTML = `<strong>Username:</strong> ${username}`;
    document.getElementById("email").innerHTML = `<strong>Email:</strong> ${email}`;
    let fav_spot_element = document.getElementById("favorite-spots");

    if (favorite_spots.length === 0) {
        return;
    }

    fav_spot_element.style = "display: block";

    for (let i = 0; i < favorite_spots.length; i++) {
        addFavoriteSpotToUI(favorite_spots[i].name, favorite_spots[i].spot_id);
    }
}

function updateSpots(name, spotId, favorite_spots) {
    let spotDropdown = document.getElementById("spots");

    // Check if the spot is already in the favorite_spots array
    if (favorite_spots.some(spot => spot.spot_id === spotId)) {
        return;
    }

    // Append a new option to the spot select element
    let option = document.createElement("option");
    option.text = name;
    option.value = spotId;

    spotDropdown.add(option);
}

function addDropdown(name, spotId) {
    let spotDropdown = document.getElementById("spots");

    // Check if the spot is not already in the dropdown
    if (![...spotDropdown.options].some(option => option.value === spotId)) {
        // Append a new option to the dropdown
        let option = document.createElement("option");
        option.text = name;
        option.value = spotId;

        spotDropdown.add(option);
    }
}

function addFavoriteSpotToUI(name, spotId) {
    let fav_spot_element = document.getElementById("favorite-spots");

    // Create a div for the favorite spot
    let spotDiv = document.createElement("div");
    spotDiv.className = "flex items-center justify-between bg-blue-600 text-white px-4 py-2 rounded-lg shadow-md";
    spotDiv.id = spotId;

    // Add the spot name
    let spotName = document.createElement("span");
    spotName.textContent = name;

    // Add the delete button
    let deleteButton = document.createElement("button");
    deleteButton.className = "bg-red-500 hover:bg-red-700 text-white font-bold px-2 py-1 rounded-lg transition";
    deleteButton.textContent = "X";
    deleteButton.setAttribute("aria-label", "Delete Spot");
    deleteButton.onclick = function () {
        deleteSpot(spotId);
    };

    // Append the name and button to the div
    spotDiv.appendChild(spotName);
    spotDiv.appendChild(deleteButton);

    // Append the div to the favorite spots container
    fav_spot_element.appendChild(spotDiv);
}

function removeSpotFromDropdown(spotId) {
    let spotDropdown = document.getElementById("spots");
    for (let i = 0; i < spotDropdown.options.length; i++) {
        if (spotDropdown.options[i].value === spotId) {
            spotDropdown.remove(i);
            break;
        }
    }
}
