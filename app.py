import os
import streamlit as st
from groq import Groq
from PyPDF2 import PdfReader
import pandas as pd
from docx import Document

# Set up the Streamlit app configuration
st.set_page_config(page_title="AI Chatbot", layout="wide")

# Initialize the Groq client
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    st.error("API key not found. Make sure it's set as 'GROQ_API_KEY' in the environment variables.")
    st.stop()

client = Groq(api_key=api_key)

# Function to get chatbot response from Groq API
def chat_with_groq(messages):
    api_messages = [{"role": msg["role"], "content": msg["content"]} for msg in messages]
    
    try:
        response = client.chat.completions.create(
            messages=api_messages,
            model="llama3-8b-8192",
        )
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return "Sorry, I couldn't process your request."

# Function to process uploaded files
def process_uploaded_file(file):
    if file.name.endswith(".pdf"):
        reader = PdfReader(file)
        text = "".join([page.extract_text() for page in reader.pages])
        return text
    elif file.name.endswith(".xlsx") or file.name.endswith(".csv"):
        df = pd.read_excel(file) if file.name.endswith(".xlsx") else pd.read_csv(file)
        return df.to_string()
    elif file.name.endswith(".docx"):
        doc = Document(file)
        text = "\n".join([para.text for para in doc.paragraphs])
        return text
    else:
        return "Unsupported file type."

# Initialize chat history if not already set
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Function to format messages for display
def format_message(content):
    formatted_content = content.replace("\n", "<br>")
    return f"<div style='font-size: 16px; font-family: Arial, sans-serif;'>{formatted_content}</div>"

# Display chat history on the left side
def display_chat_history():
    for message in st.session_state.chat_history:
        role = "User" if message["role"] == "user" else "Assistant"
        color = "#4CAF50" if role == "User" else "#FF5733"

        st.markdown(
            f"""
            <div style='text-align: left; margin-bottom: 10px;'>
                <span style='color: {color}; font-weight: bold; font-size: 18px;'>{role}:</span>
                {format_message(message["content"])}
            </div>
            """,
            unsafe_allow_html=True
        )

# Handle user input
def handle_user_input():
    user_message = st.session_state.user_input
    if user_message:
        st.session_state.chat_history.append({"role": "user", "content": user_message})

        response = chat_with_groq(st.session_state.chat_history)
        st.session_state.chat_history.append({"role": "assistant", "content": response})

        st.session_state.user_input = ""

# Streamlit UI layout
st.title("AI Chatbot")
st.subheader("Chat with an intelligent assistant powered by Groq's LLM!")

# File uploader section
uploaded_file = st.file_uploader("Upload a PDF, Excel, or Word file", type=["pdf", "xlsx", "csv", "docx"])

if uploaded_file:
    file_content = process_uploaded_file(uploaded_file)
    st.text_area("File Content", file_content, height=200)

# User input section with callback on submission
st.text_input("You:", key="user_input", on_change=handle_user_input)

# Display chat history with custom styling
st.write("---")
st.subheader("Chat History")
display_chat_history()

# Add footer at the bottom
st.markdown(
    """
    <hr style="border: none; border-top: 1px solid #eee; margin-top: 20px;" />
    <div style="text-align: center; font-size: 14px; color: #888;">
        Chatbot Developed by <b>Shahzad Mahmood</b>
    </div>
    """,
    unsafe_allow_html=True
)
