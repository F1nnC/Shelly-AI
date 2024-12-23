document.addEventListener("DOMContentLoaded", () => {
    const chatMessages = document.getElementById("chat-messages");
    const chatInput = document.getElementById("chat-input");
    const sendButton = document.getElementById("send-btn");

    sendButton.addEventListener("click", () => {
        const messageText = chatInput.value.trim();

        if (messageText !== "") {
            // Create a new message div
            const messageDiv = document.createElement("div");
            messageDiv.classList.add("flex", "justify-end", "my-2");

            const messageContent = document.createElement("div");
            messageContent.classList.add("btn-cool", "text-white", "px-4", "py-2", "rounded-lg", "max-w-xs", "bg-blue-600");
            messageContent.textContent = messageText;

            // Append the message content to the message div
            messageDiv.appendChild(messageContent);

            // Append the new message div to the chat messages container
            chatMessages.appendChild(messageDiv);

            // Scroll to the bottom of the chat messages container
            chatMessages.scrollTop = chatMessages.scrollHeight;

            // Clear the input field
            chatInput.value = "";
        }
    });

    // Allow sending messages with the Enter key
    chatInput.addEventListener("keydown", (event) => {
        if (event.key === "Enter") {
            sendButton.click();
        }
    });
});

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