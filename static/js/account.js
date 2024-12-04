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
    const apiUrl = `${baseUrl}/auth/user`;

    fetch(apiUrl, requestOptions)
        .then((response) => {
            if (!response.ok) {
                throw new Error("HTTP error, status = " + response.status);
            }
            updatePage(response.username, response.email, response.favorite_spots);
            return response.json();
        })
        .then((result) => console.log(result))
        .catch((error) => console.error(error));


}

function updatePage(username, email, favorite_spots) {
    document.getElementById("welcome").innerHTML = `Welcome, ${username}`;
    document.getElementById("username").innerHTML = `<strong>Username:</strong> ${username}`;
    document.getElementById("email").innerHTML = `<strong>Email:</strong> ${email}`;
    document.getElementById("favorite-spots").innerHTML = `<strong>Favorite Spots:</strong> ${favorite_spots}`;
}