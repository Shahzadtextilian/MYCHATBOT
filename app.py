import streamlit as st
from PyPDF2 import PdfReader
import pandas as pd
from docx import Document

st.set_page_config(page_title="Groq AI Chatbot", layout="wide")

# Store chat history in session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

def display_messages():
    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            st.markdown(f"**User:** {msg['content']}")
        else:
            st.markdown(f"**ChatGPT:** {msg['content']}")

def process_uploaded_file(file):
    if file.name.endswith(".pdf"):
        reader = PdfReader(file)
        text = " ".join([page.extract_text() for page in reader.pages])
        return text
    elif file.name.endswith(".xlsx") or file.name.endswith(".csv"):
        df = pd.read_excel(file) if file.name.endswith(".xlsx") else pd.read_csv(file)
        return df.to_string()
    elif file.name.endswith(".docx"):
        doc = Document(file)
        text = " ".join([para.text for para in doc.paragraphs])
        return text
    else:
        return "Unsupported file type."

st.title("🧠 Groq-powered AI Chatbot")
st.subheader("Chat with documents and AI seamlessly!")

uploaded_file = st.file_uploader("Upload a PDF, Excel, or Word file", type=["pdf", "xlsx", "csv", "docx"])

if uploaded_file:
    file_content = process_uploaded_file(uploaded_file)
    st.text_area("File Content", file_content, height=200)

user_input = st.text_input("You:", key="user_input")

if user_input:
    # Append user message to history
    st.session_state.chat_history.append({"role": "user", "content": user_input})

    # Get chatbot response
    response = chat_with_groq(st.session_state.chat_history)

    # Append chatbot message to history
    st.session_state.chat_history.append({"role": "assistant", "content": response})

    # Clear input
    st.session_state.user_input = ""

# Display chat history
st.write("---")
st.subheader("Chat History")
display_messages()
