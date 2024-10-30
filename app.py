import streamlit as st
import requests
from bs4 import BeautifulSoup
from groq import Groq

# Initialize Groq client using the API key from Streamlit secrets
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

def scrape_website(url):
    """Scrapes and extracts key paragraphs from the website."""
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        soup = BeautifulSoup(response.content, "html.parser")

        # Extract and limit the number of paragraphs (e.g., first 5)
        paragraphs = [p.get_text() for p in soup.find_all('p')[:5]]
        return " ".join(paragraphs)[:1500]  # Limit to 1500 characters
    except Exception as e:
        st.error(f"Failed to retrieve data from the website: {e}")
        return ""

def query_groq(prompt, context):
    """Sends a query to Groq API with optimized context."""
    try:
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "Use the following context for answering queries."},
                {"role": "system", "content": context},
                {"role": "user", "content": prompt}
            ],
            model="llama3-8b-8192"
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

# Streamlit UI
st.title("RAG System with Groq API")
st.write("Enter a website URL and ask your question!")

# Input field for website URL and user query
website_url = st.text_input("Enter Website URL:", "")
user_query = st.text_input("Enter Your Query:", "")

# Button to scrape website and query Groq
if st.button("Get Answer"):
    if website_url.strip() and user_query.strip():
        with st.spinner("Fetching data from website..."):
            website_content = scrape_website(website_url)

        if website_content:
            with st.spinner("Generating response..."):
                response = query_groq(user_query, website_content)
                st.text_area("Response from Groq:", response, height=200)
    else:
        st.warning("Please provide both a valid website URL and a query.")
