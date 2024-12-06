# streamlit_app.py

import streamlit as st
import requests
import plotly.io as pio
import json

# Set the backend API URL
API_URL = 'http://localhost:8000'  # Change this if your backend is hosted elsewhere

st.set_page_config(page_title="Data Analysis App", layout="wide")
st.title("📊 Data Analysis App")

# Initialize session state for uploaded filename and question state
if 'uploaded_filename' not in st.session_state:
    st.session_state.uploaded_filename = None

if 'question_step' not in st.session_state:
    st.session_state.question_step = 0

if 'current_question' not in st.session_state:
    st.session_state.current_question = ''

# ----------------------------
# File Upload Section
# ----------------------------
st.header("📥 Upload CSV File")

uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])

if uploaded_file is not None:
    # Upload the file to the backend
    files = {'file': (uploaded_file.name, uploaded_file.getvalue(), 'text/csv')}
    with st.spinner("Uploading..."):
        response = requests.post(f"{API_URL}/upload_csv/", files=files)

    if response.status_code == 200:
        st.success(f"✅ File '{uploaded_file.name}' uploaded successfully.")
        st.session_state.uploaded_filename = uploaded_file.name
    else:
        st.error(f"⚠️ Failed to upload file. Error: {response.json().get('error', 'Unknown error')}")

# ----------------------------
# Ask Question Section
# ----------------------------
st.header("❓ Ask a Question about Your Data")

if st.session_state.uploaded_filename:
    if st.session_state.question_step == 0:
        question = st.text_input("Enter your question", key="initial_question")

        if st.button("🔍 Get Result Count") and question:
            with st.spinner("Processing your question..."):
                data = {
                    'question': question,
                    'filename': st.session_state.uploaded_filename,
                    'confirm': False
                }
                response = requests.post(f"{API_URL}/ask_question/", data=data)

            if response.status_code == 200:
                count = response.json().get('count', 0)
                st.session_state.current_question = question
                st.session_state.question_step = 1
                st.session_state.query_count = count
            else:
                st.error(f"⚠️ Error: {response.json().get('error', 'Unknown error')}")
    elif st.session_state.question_step == 1:
        count = st.session_state.query_count
        st.write(f"**Number of results:** {count}")

        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("✅ Continue"):
                with st.spinner("Generating answer..."):
                    data = {
                        'question': st.session_state.current_question,
                        'filename': st.session_state.uploaded_filename,
                        'confirm': True
                    }
                    response = requests.post(f"{API_URL}/ask_question/", data=data)

                if response.status_code == 200:
                    answer = response.json().get('response', '')
                    st.write("**📝 Answer:**")
                    st.write(answer)
                    # Reset the question step
                    st.session_state.question_step = 0
                else:
                    st.error(f"⚠️ Error: {response.json().get('error', 'Unknown error')}")
        with col2:
            if st.button("🔄 Try Another Query"):
                st.session_state.question_step = 0
                st.session_state.current_question = ''
        with col3:
            if st.button("** 🤔 New question ** "):
                st.write("You chose to give up on this query.")
                st.session_state.question_step = 0
                st.session_state.current_question = ''
else:
    st.info("Please upload a CSV file to ask questions about your data.")

# ----------------------------
# Visualization Section
# ----------------------------
st.header("📈 Data Visualization")

if st.session_state.uploaded_filename:
    viz_question = st.text_input("Enter your visualization request")

    if st.button("🎨 Generate Visualization") and viz_question:
        with st.spinner("Generating visualization..."):
            data = {'question': viz_question, 'filename': st.session_state.uploaded_filename}
            response = requests.post(f"{API_URL}/visualize/", data=data)

        if response.status_code == 200:
            plotly_json = response.json().get('plotly_json', None)
            if plotly_json:
                try:
                    # Convert JSON string to Plotly figure
                    fig = pio.from_json(plotly_json)
                    st.plotly_chart(fig, use_container_width=True)
                except Exception as e:
                    st.error(f"⚠️ Failed to render Plotly figure. Error: {e}")
            else:
                st.error("⚠️ Failed to retrieve Plotly JSON.")
        else:
            st.error(f"⚠️ Error: {response.json().get('error', 'Unknown error')}")
else:
    st.info("Please upload a CSV file to generate visualizations.")
