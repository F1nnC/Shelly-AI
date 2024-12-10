document.getElementById("send-btn").addEventListener("click", () => {
    const chatInput = document.getElementById("chat-input");
    const messageText = chatInput.value.trim();

    if (messageText) {
        const chatMessages = document.getElementById("chat-messages");

        // Create a new message bubble for user input
        const userMessage = document.createElement("div");
        userMessage.className = "flex justify-end";
        userMessage.innerHTML = `
            <div class="bg-gray-700 text-white px-4 py-2 rounded-lg max-w-xs">
                ${messageText}
            </div>
        `;
        chatMessages.appendChild(userMessage);

        // Clear input
        chatInput.value = "";

        // Scroll to the bottom
        chatMessages.scrollTop = chatMessages.scrollHeight;

        // Simulate bot response (replace with your backend logic)
        setTimeout(() => {
            const botMessage = document.createElement("div");
            botMessage.className = "flex";
            botMessage.innerHTML = `
                <div class="bg-blue-600 text-white px-4 py-2 rounded-lg max-w-xs">
                    This is a placeholder response from Shelly AI.
                </div>
            `;
            chatMessages.appendChild(botMessage);
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }, 1000);
    }
});
