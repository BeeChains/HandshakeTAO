import streamlit as st
import requests

st.title('HandshakeTAO Domain Manager with Bittensor and Corcel Integration')

# Fetch and display the current $TAO price
st.header('Current $TAO Price')
try:
    # Replace 'tao' with the actual ID used by the API for $TAO
    tao_price_response = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=bittensor&vs_currencies=usd')
    if tao_price_response.status_code == 200:
        tao_price_data = tao_price_response.json()
        tao_price = tao_price_data.get('tao', {}).get('usd', 'Price not available')
        st.write(f"The current price of $TAO is: ${tao_price}")
    else:
        st.error("Failed to fetch the current $TAO price.")
except Exception as e:
    st.error(f"An error occurred: {str(e)}")

# Section for registering a subdomain on τao/
st.header('Register a Subdomain on τao/')
subdomain = st.text_input('Enter the subdomain you wish to register (e.g., yourname):')
if subdomain:
    register_button = st.button('Register Subdomain')
    if register_button:
        # Here you would include logic to register the subdomain using your backend system or API
        # For demonstration, we simulate successful registration:
        st.success(f"The subdomain {subdomain}.τao has been successfully registered!")


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
            st.write(f"AI Response: {ai_response}")
        else:
            st.error(f"Error: Received status code {chat_response.status_code}")

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
            st.error(f"Error: Received status code {image_response.status_code}")
else:
    st.warning('Please enter your Corcel API key to use AI features.')

# Placeholder for Bittensor CLI command execution (ensure safe usage)
st.header('Bittensor CLI Interaction')
btcli_command = st.text_input('Enter a safe btcli command to execute:')
if btcli_command:
    # Note: Actual execution of btcli commands should be handled carefully
    # This is a placeholder for input - ensure secure handling and execution
    st.text_area("Command output:", "Simulated response for: " + btcli_command)
