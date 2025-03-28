// Function to handle the sending of messages when "Enter" is pressed
function handleKey(event) {
    if (event.key === "Enter") {
        sendMessage();
    }
}

function sendMessage() {
    let userInput = document.getElementById("user-input").value;
    if (userInput.trim() === "") {
        return;  // Don't send empty messages
    }

    // Display user input in the chat box (on the right side)
    let chatBox = document.getElementById("chat-box");
    chatBox.innerHTML += "<div class='user-message'>" + userInput + "</div>";
    document.getElementById("user-input").value = ""; // Clear the input field

    // Make the AJAX POST request to the Flask backend
    fetch("/chat", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ message: userInput })
    })
    .then(response => response.json())
    .then(data => {
        // Display the bot's response (on the left side)
        chatBox.innerHTML += "<div class='bot-message'>" + data.response + "</div>";
        chatBox.scrollTop = chatBox.scrollHeight;  // Scroll to the bottom of the chat box
    })
    .catch(error => {
        console.error("Error:", error);
    });
}
