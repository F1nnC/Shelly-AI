const email = "";
const favorite_spots = [];
const username = "";

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

    fetch(apiUrl, requestOptions)
        .then((response) => {
            if (!response.ok) {
                throw new Error("HTTP error, status = " + response.status);
            }
            return response.json();
        })
        .then((result) => {
            updatePage(result.username, result.email, result.favorite_spots);
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
            // for every spot in the result, update the spots
            for (let i = 0; i < result.length; i++) {
                updateSpots(result[i].name, result[i].spotId);
            }
        })
        .catch((error) => console.error(error));
}

function updatePage(username, email, favorite_spots) {
    document.getElementById("welcome").innerHTML = `Welcome, ${username}`;
    document.getElementById("username").innerHTML = `<strong>Username:</strong> ${username}`;
    document.getElementById("email").innerHTML = `<strong>Email:</strong> ${email}`;
    document.getElementById("favorite-spots").innerHTML = `<strong>Favorite Spots:</strong> ${favorite_spots}`;
}

function updateSpots(name, spotId) {
    let spot = document.getElementById("spots");

    // Appened a new option to the spot select element
    let option = document.createElement("option");
    option.text = name;
    option.value = spotId;

    spot.add(option);
    
}