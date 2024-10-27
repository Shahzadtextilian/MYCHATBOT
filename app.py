import os
import streamlit as st
from groq import Groq

# Set up the Streamlit app configuration
st.set_page_config(page_title="AI Chatbot", layout="wide")

# Initialize the Groq client
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    st.error("API key not found. Make sure it's set as 'GROQ_API_KEY' in the environment variables.")
    st.stop()

client = Groq(api_key=api_key)

# Available Groq models
GROQ_MODELS = ["llama3-8b-8192", "llama2-7b-4096", "gpt-j-6b", "opt-13b"]

# Initialize chat history and selected model if not already set
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "selected_model" not in st.session_state:
    st.session_state.selected_model = "llama3-8b-8192"  # Default model

# Function to get chatbot response from Groq API
def chat_with_groq(messages, model):
    api_messages = [{"role": msg["role"], "content": msg["content"]} for msg in messages]

    try:
        response = client.chat.completions.create(
            messages=api_messages,
            model=model,
        )
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return "Sorry, I couldn't process your request."

# Function to display chat history with formatting
def display_chat_history():
    for message in st.session_state.chat_history:
        role = "User" if message["role"] == "user" else "Assistant"
        color = "#4CAF50" if role == "User" else "#FF5733"

        st.markdown(
            f"""
            <div style='text-align: left; margin-bottom: 10px;'>
                <span style='color: {color}; font-weight: bold; font-size: 18px;'>{role}:</span>
                <div style='font-size: 16px; font-family: Arial, sans-serif;'>{message["content"].replace("\n", "<br>")}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

# Function to handle user input and get response
def handle_user_input():
    user_message = st.session_state.get("user_input", "").strip()
    if user_message:
        st.session_state.chat_history.append({"role": "user", "content": user_message})

        # Get response from the selected model
        response = chat_with_groq(st.session_state.chat_history, st.session_state.selected_model)
        st.session_state.chat_history.append({"role": "assistant", "content": response})

        # Reset input field
        st.session_state["user_input"] = ""

# Streamlit UI layout
st.title("AI Chatbot")
st.subheader("Chat with an intelligent assistant")

# Model selection dropdown
st.selectbox(
    "Select Model",
    GROQ_MODELS,
    index=GROQ_MODELS.index(st.session_state.selected_model),
    key="selected_model",
)

# Form to handle user input
with st.form(key="chat_form", clear_on_submit=True):
    st.text_input("You:", key="user_input")
    submit_button = st.form_submit_button(label="Submit")

# If submit button is pressed, handle the input
if submit_button:
    handle_user_input()

# Display chat history
st.write("---")
st.subheader("Chat History")
display_chat_history()

# Footer at the bottom
st.markdown(
    """
    <hr style="border: none; border-top: 1px solid #eee; margin-top: 20px;" />
    <div style="text-align: center; font-size: 14px; color: #888;">
        Chatbot Developed by <b>Shahzad Mahmood</b>
    </div>
    """,
    unsafe_allow_html=True
)
