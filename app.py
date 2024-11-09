import streamlit as st
import requests
import base64
import os
import json

# Set the NVIDIA API URL
invoke_url = "https://ai.api.nvidia.com/v1/gr/meta/llama-3.2-90b-vision-instruct/chat/completions"
stream = True

# Access the API key from Streamlit secrets
api_key = st.secrets["NVIDIA_API_KEY"]

if not api_key:
    st.error("API key not found in Streamlit secrets.")

# Streamlit UI
st.title("Image Analysis Chatbot with Llama-3.2-90B Vision Model")
st.write("Upload an image and let the chatbot analyze it for you!")

# File uploader for image
uploaded_file = st.file_uploader("Choose an image...", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    # Display the uploaded image
    st.image(uploaded_file, caption='Uploaded Image', use_column_width=True)

    # Read the image and encode it in base64
    image_b64 = base64.b64encode(uploaded_file.read()).decode()

    # Check image size
    if len(image_b64) >= 180_000:
        st.error("The uploaded image is too large. Please upload a smaller image.")
    else:
        # Prepare request headers
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Accept": "text/event-stream" if stream else "application/json"
        }

        # Prepare the payload
        payload = {
            "model": 'meta/llama-3.2-90b-vision-instruct',
            "messages": [
                {
                    "role": "user",
                    "content": f'What is in this image? <img src="data:image/png;base64,{image_b64}" />'
                }
            ],
            "max_tokens": 512,
            "temperature": 1.00,
            "top_p": 1.00,
            "stream": stream
        }

        # Placeholder for streaming response
        response_placeholder = st.empty()
        response_text = ""

        # Send the API request
        try:
            response = requests.post(invoke_url, headers=headers, json=payload, stream=stream)

            # Check for successful response
            response.raise_for_status()

            # Process the streaming response
            st.write("Analyzing image... Please wait.")
            for line in response.iter_lines():
                if line:
                    # Decode the line and parse JSON
                    decoded_line = line.decode("utf-8").strip()
                    if decoded_line != "[DONE]":
                        try:
                            data = json.loads(decoded_line)
                            # Extract content from the response
                            content = data['choices'][0]['delta'].get('content', '')
                            response_text += content
                            # Update the Streamlit placeholder with the new text
                            response_placeholder.text(response_text)
                        except json.JSONDecodeError:
                            st.error("Error decoding the response stream.")

        except requests.exceptions.RequestException as e:
            st.error(f"An error occurred: {e}")
