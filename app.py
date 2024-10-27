import os
import streamlit as st
from groq import Groq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
API_KEY = os.getenv("GROQ_API_KEY")

# Initialize Groq client
client = Groq(api_key=API_KEY)

# Set available models
AVAILABLE_MODELS = [
    "llama3-70b-8192",
    "llama3-8b-8192",
    "llama2-13b-8192"
]

# Streamlit app layout
st.title("AL Power Chatbot with RAG")
st.sidebar.header("Configuration")

# Model selection
selected_model = st.sidebar.selectbox("Select a Model", AVAILABLE_MODELS)

# File uploader
uploaded_file = st.file_uploader("Upload a PDF, Image, or Document", type=["pdf", "png", "jpg", "txt"])

def process_document(file):
    """Processes uploaded document and returns its content."""
    if file.type == "application/pdf":
        # Process PDF and extract text
        import PyPDF2
        pdf_reader = PyPDF2.PdfReader(file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text
    elif file.type in ["image/png", "image/jpeg"]:
        # Process image using OCR
        from PIL import Image
        import pytesseract
        img = Image.open(file)
        return pytesseract.image_to_string(img)
    elif file.type == "text/plain":
        # Return plain text content
        return file.read().decode("utf-8")
    else:
        return "Unsupported file type."

def generate_response(prompt, model):
    """Generates a response using the Groq API."""
    try:
        response = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model=model,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error generating response: {str(e)}"

# Handle user interaction
if uploaded_file:
    doc_content = process_document(uploaded_file)
    st.write("Document Content:", doc_content)

    user_query = st.text_input("Ask a question based on the document:")
    if st.button("Get Answer"):
        answer = generate_response(user_query, selected_model)
        st.write("Answer:", answer)
else:
    st.write("No document uploaded. You can still chat with the model.")
    user_input = st.text_input("Ask anything:")
    if st.button("Chat"):
        response = generate_response(user_input, selected_model)
        st.write("Response:", response)
