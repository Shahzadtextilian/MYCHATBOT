import streamlit as st
import requests
import base64
import json

# Set the NVIDIA API URL
invoke_url = "https://ai.api.nvidia.com/v1/gr/meta/llama-3.2-90b-vision-instruct/chat/completions"
stream = True

import os

# Access the API key from the environment variable
api_key = os.getenv("NVIDIA_API_KEY")

if not api_key:
    st.error("API key not found. Please set NVIDIA_API_KEY as an environment variable.")


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

    # Check image size (optional)
    if len(image_b64) >= 180_000:
        st.error("The uploaded image is too large. Please upload a smaller image.")
    else:
        # Prepare the API request headers
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Accept": "text/event-stream" if stream else "application/json"
        }

        # Prepare the API payload
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

        # Send the API request
        try:
            response = requests.post(invoke_url, headers=headers, json=payload, stream=stream)

            # Check the response status
            response.raise_for_status()

            # Display the response
            if stream:
                st.write("Analyzing image... Please wait.")
                analysis_result = ""
                for line in response.iter_lines():
                    if line:
                        decoded_line = line.decode("utf-8").strip()
                        if decoded_line:
                            analysis_result += decoded_line + "\n"
                st.text_area("Analysis Result:", analysis_result)
            else:
                result = response.json()
                st.text_area("Analysis Result:", json.dumps(result, indent=2))

        except requests.exceptions.RequestException as e:
            st.error(f"An error occurred: {e}")

