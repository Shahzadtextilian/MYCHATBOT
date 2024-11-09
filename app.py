import os
import base64
import streamlit as st
from groq import Groq
from PIL import Image

# Set up the Groq client with API key
client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

# Streamlit UI layout
st.title("Image Analysis and Text Chatbot ")
st.write("Upload an image or enter text for analysis.")

# Text input
user_input = st.text_area("Enter text for analysis:")

# File uploader
uploaded_file = st.file_uploader("Or upload an image", type=["jpg", "jpeg", "png", "pdf"])

if user_input:
    # Process text input
    st.write("Processing the text for analysis...")

    # Call the Groq API for text analysis
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": user_input,
            }
        ],
        model="llama-3.2-90b-vision-preview",
    )

    # Display the response from the model
    st.write("### Text Analysis Result")
    st.write(chat_completion.choices[0].message.content)

elif uploaded_file is not None:
    # Display the uploaded image
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)

    # Read and encode the image data to base64
    image_bytes = uploaded_file.read()
    image_encoded = base64.b64encode(image_bytes).decode('utf-8')

    st.write("Processing the image for analysis...")

    # Call the Groq API for image analysis
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": f"Analyze this image: {image_encoded}",
            }
        ],
        model="llama-3.2-90b-vision-preview",
    )

    # Display the response from the model
    st.write("### Image Analysis Result")
    st.write(chat_completion.choices[0].message.content)

else:
    st.write("Please enter text or upload an image to start analysis.")
