import streamlit as st
import requests

# Load API key from Streamlit secrets
GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
MODEL_NAME = "llama-3.2-90b-vision-preview"
API_URL = f"https://api.groq.com/v1/models/{MODEL_NAME}/generate"

# Streamlit UI
st.title("LLaMA 3.2 Chatbot")
st.subheader("Powered by GROQ API")

# Initialize chat history if not already present
if "messages" not in st.session_state:
    st.session_state.messages = []

def query_groq_api(prompt):
    """Send a request to the GROQ API and return the response."""
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "prompt": prompt,
        "max_tokens": 300
    }
    try:
        response = requests.post(API_URL, json=data, headers=headers)
        response.raise_for_status()  # Raise an error for bad responses

        return response.json().get("choices", [{}])[0].get("text", "")
    except requests.exceptions.HTTPError as http_err:
        st.error(f"HTTP error: {http_err}")
    except requests.exceptions.RequestException as req_err:
        st.error(f"Request error: {req_err}")
    return "I'm having trouble connecting to the server. Please try again later."

# User input section
user_input = st.text_input("You:", key="user_input")

if st.button("Send") and user_input:
    # Send the user's input to the GROQ API
    bot_response = query_groq_api(user_input)

    # Update chat history
    st.session_state.messages.append(("User", user_input))
    st.session_state.messages.append(("Bot", bot_response))

# Display chat history
for user, message in st.session_state.messages:
    st.write(f"**{user}:** {message}")
