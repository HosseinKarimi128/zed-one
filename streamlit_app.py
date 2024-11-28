# streamlit_app.py

import streamlit as st
import requests
from PIL import Image
from io import BytesIO

# Set the backend API URL
API_URL = 'http://localhost:8000'  # Adjust this if your backend is hosted elsewhere

st.title("Data Analysis App")

# File Upload Section
st.header("Upload CSV File")
uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])

if uploaded_file is not None:
    # Upload the file to the backend
    files = {'file': (uploaded_file.name, uploaded_file.getvalue())}
    response = requests.post(f"{API_URL}/upload_csv/", files=files)
    if response.status_code == 200:
        st.success(f"File '{uploaded_file.name}' uploaded successfully.")
    else:
        st.error("Failed to upload file.")

# Ask Question Section
st.header("Ask a Question about Your Data")
question = st.text_input("Enter your question")

if uploaded_file is not None and question:
    if st.button("Get Answer"):
        data = {'question': question, 'filename': uploaded_file.name}
        response = requests.post(f"{API_URL}/ask_question/", data=data)
        if response.status_code == 200:
            answer = response.json().get('response', '')
            st.write("**Answer:**", answer)
        else:
            st.error(f"Error: {response.json().get('error', 'Unknown error')}")

# Visualization Section
st.header("Data Visualization")
viz_question = st.text_input("Enter your visualization request")

if uploaded_file is not None and viz_question:
    if st.button("Generate Visualization"):
        data = {'question': viz_question, 'filename': uploaded_file.name}
        response = requests.post(f"{API_URL}/visualize/", data=data)
        if response.status_code == 200:
            image = Image.open(BytesIO(response.content))
            st.image(image, caption='Generated Visualization')
        else:
            st.error(f"Error: {response.json().get('error', 'Unknown error')}")
