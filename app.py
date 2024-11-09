import streamlit as st
import requests
import torch
from PIL import Image
from transformers import MllamaForConditionalGeneration, AutoProcessor
from huggingface_hub import login

# Replace 'your_hf_token' with your actual Hugging Face token
login("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")

# Load the model and processor
model_id = "meta-llama/Llama-3.2-90B-Vision"
model = MllamaForConditionalGeneration.from_pretrained(
    model_id,
    torch_dtype=torch.bfloat16,
    device_map="auto",
)
processor = AutoProcessor.from_pretrained(model_id)

# Define the Streamlit UI
st.title("Multimodal Chatbot with Llama 3.2 Vision")
st.write("Upload an image or a document and ask your query!")

# File uploader for image or document
uploaded_file = st.file_uploader("Choose a file", type=["jpg", "jpeg", "png", "pdf", "docx"])

# User input for the prompt
user_prompt = st.text_input("Enter your question or prompt")

if uploaded_file and user_prompt:
    # Check if the uploaded file is an image
    if uploaded_file.type in ["image/jpeg", "image/png", "image/jpg"]:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)

        # Process the image with the prompt
        prompt = f"<|image|><|begin_of_text|>{user_prompt}"
        inputs = processor(image, prompt, return_tensors="pt").to(model.device)
        output = model.generate(**inputs, max_new_tokens=30)
        response = processor.decode(output[0])

        st.success("Response:")
        st.write(response)

    # Add support for document inputs here (e.g., PDF, DOCX)
    elif uploaded_file.type in ["application/pdf", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"]:
        st.warning("Document processing is not implemented yet.")
