from flask import Flask, render_template, request, jsonify
from langchain_ollama import OllamaLLM
import json

app = Flask(__name__)  # Fixed incorrect `_name_` to `__name__`

# Initialize OllamaLLM with the model (adjust to your use case)
ollama_model = OllamaLLM(model="llama2:latest")

# Memory to maintain the conversation's context
conversation_history = []

# Load prompts from JSON file (optional, placeholder for now)

@app.route("/")
def index():
    """
    Render the chatbot UI.
    """
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    """
    Handle user input, analyze symptoms, and generate concise responses.
    """
    global conversation_history
    user_input = request.json.get("message")
    print(f"User Input: {user_input}")  # Log user input for debugging

    if user_input:
        try:
            # Add user input to the conversation history
            conversation_history.append(f"User: {user_input}")

            # Handle greetings
            greeting_response = handle_greetings(user_input)
            if greeting_response:
                return jsonify({"response": greeting_response})

            # Handle doctor recommendation request
            doctor_response = handle_doctor_request(user_input)
            if doctor_response:
                return jsonify({"response": doctor_response})

            # Handle edge cases: ambiguous input, no symptoms mentioned, etc.
            edge_case_handling_response = handle_edge_cases(user_input)
            if edge_case_handling_response:
                return jsonify({"response": edge_case_handling_response})

            # System instructions for the model
            system_instruction = (
                "You are a medical assistant chatbot. Maintain the context of the conversation. "
                "Analyze symptoms, identify potential health conditions, and recommend actions. "
                "Ensure your response is concise, clear, and no more than 80 words."
            )

            # Create the input prompt with context
            conversation_context = "\n".join(conversation_history[-5:])  # Keep the last 5 exchanges for context
            full_input = f"{system_instruction}\n{conversation_context}\nAssistant:"

            # Generate the response using Ollama
            response = ollama_model.invoke(full_input)
            print(f"Ollama Response: {response}")

            # Truncate the response to ensure it doesn't exceed 80 words
            truncated_response = truncate_response(response, max_words=80)

            # Add the assistant's response to the conversation history
            conversation_history.append(f"Assistant: {truncated_response}")

            return jsonify({"response": truncated_response})
        except Exception as e:
            print(f"Error during model invocation: {str(e)}")
            return jsonify({"response": "Sorry, I encountered an error. Please try again."})
    else:
        return jsonify({"response": "Please describe your symptoms so I can assist."})

def handle_greetings(user_input):
    """
    Handle greeting intents based on user input.
    """
    greetings = ["hi", "hello", "hey", "good morning", "good evening", "howdy", "what's up"]
    for greeting in greetings:
        if greeting in user_input.lower() and "doctor" not in user_input.lower():
            return "Hello! How can I assist you with your health today?"
    
    # If the conversation already progressed beyond greetings, don't respond to greetings
    return None  # No greeting detected

def handle_doctor_request(user_input):
    """
    Handle doctor's recommendation based on the user's location.
    """
    if "mathura" in user_input.lower() and "doctor" in user_input.lower():
        return "Based on your location in Mathura, I suggest you visit the following doctors:\n- Dr. XYZ, Orthopedic Specialist\n- Dr. ABC, General Physician.\nYou can find their contact details online or in local directories."
    return None

def handle_edge_cases(user_input):
    """
    Handle edge cases such as vague inputs, user errors, and missing symptoms.
    """
    # Handle "thank you" with different responses based on context
    if "thank you" in user_input.lower():
        # You can differentiate between a conversational "thank you" and a goodbye
        if conversation_history and conversation_history[-1].lower().startswith("assistant:"):  # If last message is from assistant
            return "You're welcome! How else can I assist you today?"
        else:
            return "Good Bye, take care!"
    
    # Handle "bye" or similar phrases
    elif "bye" in user_input.lower() or "goodbye" in user_input.lower() or "see you" in user_input.lower():
        return "Good Bye, take care!"

    # Case 1: Check if the input is too vague or general
    elif "i don't know" in user_input.lower() or "unsure" in user_input.lower():
        return "Could you please describe the symptoms you're experiencing in more detail?"

    # Case 2: If the user doesn't provide symptoms, ask for more information
    elif "no symptoms" in user_input.lower() or "nothing" in user_input.lower():
        return "I need more details. Can you describe any symptoms you are experiencing?"

    # Case 3: If input contains spelling mistakes or gibberish
    elif not user_input.isalpha() and not any(char.isalnum() for char in user_input):
        return "It seems like there might have been a typo or an error. Could you please rephrase?"

    # Case 4: If the input is too short and lacks information, ask for clarification
    elif len(user_input.split()) < 3:
        return "Could you provide more details about your symptoms?"

    # Default fallback
    return None

def truncate_response(response, max_words):
    """
    Truncate the response to a specified number of words.
    """
    words = response.split()
    if len(words) > max_words:
        return " ".join(words[:max_words]) + "..."
    return response

if __name__ == "__main__":  # Fixed incorrect `_name_` to `__name__`
    app.run(debug=True)
