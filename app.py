import streamlit as st
import requests
import base64
import os
import json

# Set the NVIDIA API URL
invoke_url = "https://ai.api.nvidia.com/v1/gr/meta/llama-3.2-90b-vision-instruct/chat/completions"
stream = True

# Load the API key from environment variables or Streamlit secrets
api_key = os.getenv("NVIDIA_API_KEY", "YOUR_API_KEY")

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
                    decoded_line = line.decode("utf-8").strip()

                    # Debugging output to show what is being received
                    st.text(f"Received line: {decoded_line}")

                    # Skip control messages like [DONE] or empty lines
                    if decoded_line == "[DONE]" or not decoded_line:
                        continue

                    # Try to parse the JSON line
                    try:
                        data = json.loads(decoded_line)
                        content = data.get("choices", [{}])[0].get("delta", {}).get("content", "")
                        if content:
                            response_text += content
                            # Update the Streamlit placeholder with the new text
                            response_placeholder.text(response_text)
                    except json.JSONDecodeError as json_error:
                        st.warning(f"Non-JSON line received: {decoded_line}")
                        st.warning(f"JSONDecodeError: {json_error}")

        except requests.exceptions.RequestException as e:
            st.error(f"An error occurred: {e}")
