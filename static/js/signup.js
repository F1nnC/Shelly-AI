

function registerUser() {
    event.preventDefault(); 
    const username = document.getElementById("username").value;
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    const email2 = document.getElementById("email2").value;
    const password2 = document.getElementById("password2").value;

    if (email !== email2) {
        document.getElementById("error").innerText = "Emails do not match";
        document.getElementById("error").style.display = "inline-block";
        return;
    }

    if (password !== password2) {
        document.getElementById("error").innerText = "Passwords do not match";
        document.getElementById("error").style.display = "inline-block";
        return;
    }

    const myHeaders = new Headers();
    myHeaders.append("Content-Type", "application/json");

    const raw = JSON.stringify({
    "username": username,
    "email": email,
    "password": password
    });

    const requestOptions = {
    method: "POST",
    headers: myHeaders,
    body: raw,
    redirect: "follow"
    };

    
    const baseUrl = `${window.location.protocol}//${window.location.hostname}${window.location.port ? ':' + window.location.port : ''}`;
    const apiUrl = `${baseUrl}/auth/login`;

    fetch(apiUrl, requestOptions)
        .then((response) => {
            if (response.ok) { // If the response status is 200-299
                window.location.href = `${baseUrl}/login`; // Redirect to /login
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