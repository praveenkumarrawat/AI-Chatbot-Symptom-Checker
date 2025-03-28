// Function to open the chatbot when the user clicks the chatbot icon
function openChatbot() {
    const chatbotContainer = document.getElementById("chatbot-container");
    chatbotContainer.style.display = "block"; // Show the chatbot
}

// Function to close the chatbot when the user clicks the close button
function closeChatbot() {
    const chatbotContainer = document.getElementById("chatbot-container");
    chatbotContainer.style.display = "none"; // Hide the chatbot
}

// Function to handle the user pressing the Enter key in the input field
function handleKey(event) {
    if (event.key === "Enter") {
        sendMessage(); // Trigger the send message function on Enter key
    }
}

// Function to send the user input to the backend and display the response
async function sendMessage() {
    const userInput = document.getElementById("user-input").value;
    if (!userInput.trim()) return;  // Don't send empty messages

    // Add user message to the chatbox
    addMessageToChatbox('You: ' + userInput);

    try {
        // Send the message to the Flask backend
        const response = await fetch("http://127.0.0.1:5000/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ message: userInput })
        });

        // Check if the response is successful
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        // Get the response from Flask backend
        const data = await response.json();
        const botResponse = data.response;

        // Add bot response to chatbox
        addMessageToChatbox('Bot: ' + botResponse);
        document.getElementById("user-input").value = '';  // Clear input field
    } catch (error) {
        console.error('Error:', error);
        addMessageToChatbox('Bot: Sorry, there was an issue connecting to the chatbot.');
    }
}

// Function to add a message to the chatbox
function addMessageToChatbox(message) {
    const chatBox = document.getElementById("chat-box");

    // Create a new div element for the message
    const messageElement = document.createElement("div");
    messageElement.classList.add("chat-message");
    messageElement.textContent = message;

    // Append the new message to the chatbox
    chatBox.appendChild(messageElement);

    // Scroll to the bottom of the chatbox to show the latest message
    chatBox.scrollTop = chatBox.scrollHeight;
}
