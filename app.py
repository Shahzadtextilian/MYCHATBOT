import os
import streamlit as st
from groq import Groq
from PyPDF2 import PdfReader
import pandas as pd
from docx import Document

# Set up the Streamlit app configuration
st.set_page_config(page_title="My AI Chatbot", layout="wide")

# Initialize the Groq client
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    st.error("API key not found. Make sure it's set as 'GROQ_API_KEY' in the environment variables.")
    st.stop()

client = Groq(api_key=api_key)

# Helper function to communicate with Groq API
def chat_with_groq(messages):
    try:
        response = client.chat.completions.create(
            messages=messages,
            model="llama3-8b-8192",
        )
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return "Sorry, I couldn't process your request."

# Helper function to process uploaded files
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

# Initialize chat history in session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Display chat history
def display_chat_history():
    for message in st.session_state.chat_history:
        role = "User" if message["role"] == "user" else "Assistant"
        st.markdown(f"**{role}:** {message['content']}")

# Streamlit UI
st.title("My AI-Powered Chatbot")
st.subheader("Chat with an intelligent assistant powered by Groq's LLM!")

# File uploader section
uploaded_file = st.file_uploader("Upload a PDF, Excel, or Word file", type=["pdf", "xlsx", "csv", "docx"])

if uploaded_file:
    file_content = process_uploaded_file(uploaded_file)
    st.text_area("File Content", file_content, height=200)

# User input section
user_input = st.text_input("You:", key="user_input")

if user_input:
    # Append user input to chat history
    st.session_state.chat_history.append({"role": "user", "content": user_input})

    # Get response from Groq API
    response = chat_with_groq(st.session_state.chat_history)

    # Append the response to chat history
    st.session_state.chat_history.append({"role": "assistant", "content": response})

    # Clear the input field
    st.session_state.user_input = ""

# Display chat history
st.write("---")
st.subheader("Chat History")
display_chat_history()
