document.addEventListener("DOMContentLoaded", () => {
    fetchSpotNames();
    fadeInElements();
});

function fadeInElements() {
    const elements = document.querySelectorAll('.fade-in');
    elements.forEach((element, index) => {
        setTimeout(() => {
            element.classList.add('visible');
        }, index * 100); // Stagger the fade-in effect
    });
}

function fetchShellyAI() {
    const myHeaders = new Headers();
    myHeaders.append("Content-Type", "application/json");

    const baseUrl = `${window.location.protocol}//${window.location.hostname}${window.location.port ? ':' + window.location.port : ''}`;
    const apiUrl = `${baseUrl}/ShellyAI/ask`;

    const spots = fetchSpotIds();

    const question = document.getElementById("chat-input").value.trim();

    const raw = JSON.stringify({
        "question": question,
        "chat_history": "ShellyAI: Sup, my name is ShellyAI and I'm here to help you with any surf question you need",
        "spots": spots  
    });

    const requestOptions = {
        method: "POST",
        headers: myHeaders,
        body: raw,
        redirect: "follow"
    };

    fetch(apiUrl, requestOptions)
    .then((response) => response.text())
    .then((result) => console.log(result))
    .catch((error) => console.error(error));
}

function fetchSpotIds() {
    const myHeaders = new Headers();
    myHeaders.append("Cookie", "access_token_cookie=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTczMzk4Mjg4MSwianRpIjoiMjRmMTgzMGMtZDNkNS00NDUyLWFkNTctNmE5YzZkMjU3MGI1IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6MSwibmJmIjoxNzMzOTgyODgxLCJleHAiOjE3MzM5ODM3ODF9.MZ-jhwgEQoNnZD8RLGdqKuQjXj34dE5nCZ2UOl1gMBw");

    const baseUrl = `${window.location.protocol}//${window.location.hostname}${window.location.port ? ':' + window.location.port : ''}`;
    const apiUrl = `${baseUrl}/auth/get_spot_ids`;

    const requestOptions = {
        method: "GET",
        headers: myHeaders,
        redirect: "follow"
    };

    fetch(apiUrl, requestOptions)
    .then((response) => response.text())
    .then((result) => {
        return JSON.parse(result);
    })
    .catch((error) => console.error(error));
}

function fetchSpotNames() {
    const myHeaders = new Headers();
    myHeaders.append("Cookie", "access_token_cookie=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTczMzk4Mjg4MSwianRpIjoiMjRmMTgzMGMtZDNkNS00NDUyLWFkNTctNmE5YzZkMjU3MGI1IiwidHlwZSI6ImFjY2VzcyIsInN1YiIsMSwibmJmIjoxNzMzOTgyODgxLCJleHAiOjE3MzM5ODM3ODF9.MZ-jhwgEQoNnZD8RLGdqKuQjXj34dE5nCZ2UOl1gMBw");

    const baseUrl = `${window.location.protocol}//${window.location.hostname}${window.location.port ? ':' + window.location.port : ''}`;
    const apiUrl = `${baseUrl}/auth/get_spot_names`;

    const requestOptions = {
        method: "GET",
        headers: myHeaders,
        redirect: "follow"
    };

    fetch(apiUrl, requestOptions)
    .then((response) => response.json())  // Parse the response as JSON
    .then((result) => {
        const div = document.getElementById("sidebar");
        for (let i = 0; i < result.length; i++) {
            let spot = document.createElement("button");
            spot.classList.add("w-full", "py-2", "text-center", "bg-gray-700", "bg-opacity-80", "text-white", "rounded-lg", "hover:bg-gray-600");
            spot.textContent = result[i];

            div.appendChild(spot);
        }
    })
    .catch((error) => console.error(error));
}

function sendMessage() {
    // THings need to happen
    let sendBtn = document.getElementById("send-btn");
    let chatInput = document.getElementById("chat-input");

    // Disable the ability to click send
    sendBtn.disabled = true;
    sendBtn.classList.add("cursor-not-allowed");

    // Clear the input field
    let message = chatInput.value.trim();
    chatInput.value = "";

    let userMessage = `
        <div class="flex justify-end">
            <div class="btn-cool text-white px-4 py-2 rounded-lg max-w-xs bg-gray-900 bg-opacity-80 shadow-md">
                ${message}
            </div>
        </div>
    `;

    // Append the message to the chat window
    let chatMessages = document.getElementById("chat-messages");
    chatMessages.innerHTML += userMessage;

    // Fetch the response from the server
    // TODO: Fetch the response from the server

    // Append the response to the chat window
    response = "TODO: implement the response"

    let shellyMessage = `
        <div class="flex justify-start">
            <div class="btn-chat text-white px-4 py-2 rounded-lg max-w-xs bg-gray-900 bg-opacity-80 shadow-md">
                ${response}
            </div>
        </div>
    `;

    chatMessages.innerHTML += shellyMessage;
    

    // Enable the ability to click send again
    sendBtn.disabled = false;
    sendBtn.classList.remove("cursor-not-allowed");

}