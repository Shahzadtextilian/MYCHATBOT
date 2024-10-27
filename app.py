import streamlit as st
from groq import Groq, GroqError

# Load API key from Streamlit secrets
api_key = st.secrets["GROQ_API_KEY"]

# Initialize the Groq client with error handling
try:
    client = Groq(api_key=api_key)
except GroqError as e:
    st.error(f"Failed to connect to the Groq API: {str(e)}")
    st.stop()

# Function to generate responses using the selected model
def generate_response(prompt, model="llama3-8b-8192"):
    try:
        response = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model=model,
        )
        return response.choices[0].message.content
    except GroqError as e:
        return f"Error generating response: {str(e)}"

# Streamlit UI Layout
st.title("AL Power Chatbot with RAG")

# Sidebar for Model Selection
available_models = ["llama3-70b-8192", "llama3-8b-8192", "llama2-13b-8192"]
selected_model = st.sidebar.selectbox("Select a Model", available_models)

# File Uploader for Document Uploads
uploaded_file = st.file_uploader("Upload a PDF, Image, or Text Document", type=["pdf", "png", "jpg", "txt"])

# Function to Process Uploaded Documents
def process_document(file):
    if file.type == "application/pdf":
        import PyPDF2
        pdf_reader = PyPDF2.PdfReader(file)
        return "".join([page.extract_text() for page in pdf_reader.pages])
    elif file.type in ["image/png", "image/jpeg"]:
        from PIL import Image
        import pytesseract
        img = Image.open(file)
        return pytesseract.image_to_string(img)
    elif file.type == "text/plain":
        return file.read().decode("utf-8")
    else:
        return "Unsupported file type."

# Handling User Interactions
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
