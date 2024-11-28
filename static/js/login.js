// Decet Button Click Event
document.getElementById("submit").addEventListener("click", login);

// Detect Enter Key Press Event
document.getElementById("submit").addEventListener('keypress', function (e) {
    if (e.key === 'Enter') {
      login();
    }
});

async function login() {
    event.preventDefault(); // Prevent form submission
    let username = document.getElementById("username").value;
    let password = document.getElementById("password").value;

    const myHeaders = new Headers();
    myHeaders.append("Content-Type", "application/json");

    const raw = JSON.stringify({
        "username": username,
        "password": password
    });

    const requestOptions = {
        method: "POST",
        headers: myHeaders,
        body: raw,
        redirect: "follow"
    };

    // Dynamically determine the base URL
    const baseUrl = `${window.location.protocol}//${window.location.hostname}${window.location.port ? ':' + window.location.port : ''}`;
    const apiUrl = `${baseUrl}/auth/login`;

    fetch(apiUrl, requestOptions)
        .then((response) => {
            if (response.ok) { // If the response status is 200-299
                window.location.href = `${baseUrl}/spots`; // Redirect to /spots
            } else if (response.status === 401) { // If the response status is 401
                document.getElementById("error").innerText = "Invalid username or password"; // Display error message
                document.getElementById("error").style.display = "inline-block"; // Display the error message
            } else {
                document.getElementById("error").innerText = "Sever Error"; // Display error message
                document.getElementById("error").style.display = "inline-block"; // Display the error message
            }
        })
        .then((result) => {
            if (!response.ok) {
                console.error(result); // Log the error message if the response is not ok
            }
        })
        .catch((error) => console.error(error));
}


