import streamlit as st
import os
import json
from dotenv import load_dotenv
from langchain_groq import ChatGroq


# Load environment variables
load_dotenv()

# Set page configuration
st.set_page_config(page_title="LLM App", page_icon="🤖", layout="centered")

# Sidebar for API Key
st.sidebar.title("Configuration")
groq_api_key = st.sidebar.text_input("Enter Groq API Key", type="password")

# Load JSON data
def load_data():
    try:
        with open("Verifast_assignment_raw_data.json", "r") as f:
            data = json.load(f)
        return data
    except Exception as e:
        st.error(f"Error loading JSON: {e}")
        return []

data = load_data()

# Main interface
st.title("LLM Chatbot")
st.write("Ask questions based on the provided dataset!")

# User input
user_query = st.text_area("Enter your question:")

if st.button("Get Answer"):
    if not groq_api_key:
        st.error("Please enter your Groq API key.")
    elif not user_query.strip():
        st.error("Query cannot be empty.")
    else:
        try:
            # Initialize Groq LLM
            llm = ChatGroq(model_name="llama-3.3-70b-versatile", api_key=groq_api_key)
            
            # Convert data to string format for context
            context = "\n".join([json.dumps(item) for item in data])
            prompt = f"Context: {context}\nQuestion: {user_query}\nAnswer:"
            
            response = llm.generate(input_text=prompt)
            
            # Display response
            st.subheader("AI Response:")
            st.write(response.text)
        except Exception as e:
            st.error(f"Error: {e}")

# Footer
st.markdown("---")
st.markdown("### Made by Rohit Vyavahare")
