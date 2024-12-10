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