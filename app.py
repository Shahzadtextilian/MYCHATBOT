import streamlit as st
import os
from groq import Groq

# Initialize Groq client using the API key from Streamlit secrets
client = Groq(
    api_key=st.secrets["GROQ_API_KEY"]
)

def query_groq(prompt):
    """Function to query Groq API with a user prompt."""
    try:
        response = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama3-8b-8192"
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

# Streamlit UI
st.title("RAG System with Groq API")
st.write("Ask a question, and we'll get the best answer for you using Groq!")

# Input field for the user prompt
user_input = st.text_input("Enter your query:", "")

# Button to trigger the API call
if st.button("Generate Response"):
    if user_input.strip():
        with st.spinner("Fetching response..."):
            response = query_groq(user_input)
            st.text_area("Response from Groq:", response, height=200)
    else:
        st.warning("Please enter a valid query.")
