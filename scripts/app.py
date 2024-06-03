import streamlit as st
import requests



hf_api_token = "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"

headers = {
    "Authorization": f"Bearer {hf_api_token}"
}

# Replace with your actual Hugging Face endpoint URL
HF_API_URL = "https://iws7g806dprdh6t6.us-east-1.aws.endpoints.huggingface.cloud"

st.title('Ara Gorilla 🦍')

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("What is up?"):
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Send user prompt to Hugging Face model
    response = requests.post(
        HF_API_URL,
        headers = {"Authorization": f"Bearer {hf_api_token}"},
        json={"inputs": prompt}
    )

    # Get the response text
    response_text = response.json()

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.markdown(response_text)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response_text})