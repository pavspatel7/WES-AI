async function sendMessage() {
    var userInput = document.getElementById("userInput").value;
    var chatBox = document.getElementById("chatBox");
    
    // Append user message to chat box
    var userChat = document.createElement("div");
    userChat.className = "chat user-chat";
    userChat.innerHTML = '<div class="chat-message">' + userInput + '</div>';
    chatBox.appendChild(userChat);

    // Scroll to bottom of chat box
    chatBox.scrollTop = chatBox.scrollHeight;

    // Clear the user input field
    document.getElementById("userInput").value = "";

    // Send user message to Flask backend
    const response = await fetch('/ask', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ question: userInput }),
    });

    if (response.ok) {
        // Receive and display bot response
        const data = await response.json();
        var botResponse = data.answer;
        var botChat = document.createElement("div");
        botChat.className = "chat bot-chat";

        // Check if bot response contains URLs
        if (containsURL(botResponse)) {
            // Convert URLs into clickable links
            botResponse = botResponse.replace(/(https?:\/\/[^\s]+)/g, '<a href="$1" target="_blank">$1</a>');
        }

        botChat.innerHTML = '<div class="chat-message">' + botResponse + '</div>';
        chatBox.appendChild(botChat);

        // Scroll to bottom of chat box after bot response
        chatBox.scrollTop = chatBox.scrollHeight;
    } else {
        // Handle error
        console.error('Error:', response.statusText);
    }
}

// Function to check if a string contains URLs
function containsURL(str) {
    var urlRegex = /(https?:\/\/[^\s]+)/g;
    return urlRegex.test(str);
}

document.getElementById("userInput").addEventListener("keypress", function(event) {
    // Event to listen for the Enter key press
    if (event.key === "Enter") {
        event.preventDefault(); // Prevent the default action to stop form submission
        sendMessage(); // Call sendMessage when Enter is pressed
    }
});
