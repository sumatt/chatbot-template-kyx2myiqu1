import os
import streamlit as st
import openai
import fitz  # PyMuPDF

# Function to extract text from PDF
def extract_text_from_pdf(file):
    document = fitz.open(stream=file.read(), filetype="pdf")
    text = ""
    for page_num in range(document.page_count):
        page = document.load_page(page_num)
        text += page.get_text()
    return text

# Show title and description.
st.title("Pearl AI")
st.write("Ask about cannabis")

# Get OpenAI API key from secrets
openai_api_key = st.secrets.get("OPENAI_API_KEY")
if not openai_api_key:
    st.info("Please add your OpenAI API key to continue.", icon="🗝️")
else:
    # Set the OpenAI API key
    openai.api_key = openai_api_key

    # Create a session state variable to store the chat messages. This ensures that the
    # messages persist across reruns.
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "system", "content": "You are a helpful assistant knowledgeable about cannabis."}
        ]

    # Allow users to upload a PDF document
    uploaded_file = st.file_uploader("Upload a PDF document", type="pdf")
    if uploaded_file is not None:
        pdf_text = extract_text_from_pdf(uploaded_file)
        st.session_state.messages.append({"role": "system", "content": f"Here is some information from the uploaded PDF:\n\n{pdf_text}"})

    # Display the existing chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Create a chat input field to allow the user to enter a message. This will display
    # automatically at the bottom of the page.
    if prompt := st.chat_input("What's on your mind?"):
        # Store and display the current prompt.
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate a response using the OpenAI AP
