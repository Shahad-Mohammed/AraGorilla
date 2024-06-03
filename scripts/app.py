# import streamlit as st
# import requests

# # Set page configuration
# st.set_page_config(
#     page_title="Ara Gorilla 🦍",
#     page_icon="🦍",
#     layout="centered",
#     initial_sidebar_state="auto",
# )

# # Apply custom CSS for styling
# st.markdown("""
#     <style>
#     .main {
#         background-color: #808080;
#         padding: 20px;
#         border-radius: 10px;
#     }
#     body {
#         background-color: #D3D3D3;
#     }
#     .stButton>button {
#         background-color: #4CAF50;
#         color: white;
#         font-size: 16px;
#         border-radius: 8px;
#         padding: 10px 20px;
#     }
#     .stButton>button:hover {
#         background-color: #45a049;
#     }
#     .chat-box {
#         background-color: #808080;
#         padding: 10px;
#         border-radius: 10px;
#         margin-bottom: 10px;
#     }
#     </style>
# """, unsafe_allow_html=True)

# # Initialize session state for conversation history
# if 'conversation' not in st.session_state:
#     st.session_state.conversation = []

# # Title and description
# st.title('Ara Gorilla 🦍')
# st.write("""
#     ### Welcome to Ara Gorilla!
#     This tool allows you to generate text using a fine-tuned Llama-3 model. 
#     Just enter your prompt below and click "Generate".
# """)

# # User input area
# prompt = st.text_input("Enter your prompt here:")

# # Hugging Face Inference API endpoint URL
# hf_endpoint_url = 'https://iws7g806dprdh6t6.us-east-1.aws.endpoints.huggingface.cloud'

# # Your Hugging Face API token
# hf_api_token = "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"

# headers = {
#     "Authorization": f"Bearer {hf_api_token}"
# }

# # Button to generate text
# if st.button("Generate"):
#     if prompt:
#         with st.spinner("Generating..."):
#             response = requests.post(hf_endpoint_url, headers=headers, json={"inputs": prompt})
#         if response.status_code == 200:
#             try:
#                 generated_text = response.json().get('generated_text', 'No text generated')
#                 # Append the prompt and generated text to the conversation history
#                 st.session_state.conversation.append({"prompt": prompt, "response": generated_text})
#             except KeyError:
#                 st.write("Error: Unexpected response structure:", response.json())
#         else:
#             st.write("Error:", response.json())
#     else:
#         st.write("Please enter a prompt.")

# # Display conversation history
# for entry in st.session_state.conversation:
#     st.markdown(f"""
#         <div class="chat-box">
#             <b>User:</b> {entry['prompt']}<br>
#             <b>Ara Gorilla:</b> {entry['response']}
#         </div>
#     """, unsafe_allow_html=True)


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