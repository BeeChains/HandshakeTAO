import streamlit as st
import requests
import subprocess
import shlex

st.title('HandshakeTAO Domain Manager with Bittensor and Corcel Integration')

# Allow users to input their Corcel API key
st.header('Enter your Corcel API Key')
corcel_api_key = st.text_input('Corcel API Key:', type='password')

# Interact with Corcel AI for chat
st.header('Interact with Corcel AI for Chat')
if corcel_api_key:
    user_chat_input = st.text_input('Enter your message for AI chat:')
    if user_chat_input:
        chat_payload = {'input': user_chat_input, 'apiKey': corcel_api_key}
        chat_response = requests.post('https://api.corcel.io/v1/chat', json=chat_payload)
        if chat_response.status_code == 200:
            response_data = chat_response.json()
            ai_response = response_data.get('output', 'No response received')
        else:
            ai_response = f"Error: Received status code {chat_response.status_code}"
        st.write(f"AI Response: {ai_response}")

# Generate Images with Corcel AI
st.header('Generate Images with Corcel AI')
if corcel_api_key:
    user_image_prompt = st.text_input('Enter your prompt for AI image generation:')
    if user_image_prompt:
        image_payload = {'prompt': user_image_prompt, 'apiKey': corcel_api_key}
        image_response = requests.post('https://api.corcel.io/v1/image', json=image_payload)
        if image_response.status_code == 200:
            image_url = image_response.json().get('imageUrl')
            if image_url:
                st.image(image_url)
            else:
                st.write("No image received. Please check your prompt or try again.")
        else:
            st.write(f"Error: Received status code {image_response.status_code}")
else:
    st.warning('Please enter your Corcel API key to use AI features.')

# Placeholder for Bittensor CLI command execution (ensure safe usage)
st.header('Bittensor CLI Interaction')
btcli_command = st.text_input('Enter a safe btcli command to execute:')
if btcli_command:
    # Validate command safety (placeholder function - implement actual validation based on your requirements)
    if 'btcli' in btcli_command and 'transfer' not in btcli_command and btcli_command.startswith('btcli'):
        # Simulating command execution response (replace with actual subprocess execution in a secure environment)
        # response = subprocess.run(shlex.split(btcli_command), capture_output=True, text=True)
        # st.text_area("Command output:", response.stdout if response.stdout else "No output or command is restricted.")
        st.text_area("Command output:", "Simulated response for: " + btcli_command)
    else:
        st.error("Only safe btcli read-only commands are allowed.")
