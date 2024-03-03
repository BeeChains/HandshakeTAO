import streamlit as st
import bittensor
import requests

st.title('HandshakeTAO Domain Manager with Bittensor Integration')

# Initialize Bittensor wallet
wallet = bittensor.wallet()

st.header('Bittensor Wallet Information')
st.write(f"Your Bittensor wallet coldkey: {wallet.coldkeypub.ss58_address}")

# Fetch and display the current $TAO price
st.header('Current $TAO Price')
try:
    tao_price_response = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=bittensor&vs_currencies=usd')
    if tao_price_response.status_code == 200:
        tao_price_data = tao_price_response.json()
        tao_price = tao_price_data.get('bittensor', {}).get('usd', 'Price not available')
        st.write(f"The current price of $TAO: ${tao_price} USD")
    else:
        st.error("Failed to fetch the current $TAO price.")
except Exception as e:
    st.error(f"An error occurred: {str(e)}")

# Section for registering a subdomain on τao/
st.header('Register a Subdomain on τao/')
subdomain = st.text_input('Enter the subdomain you wish to register (e.g., yourname):')
if subdomain and st.button('Register Subdomain'):
    # Here you would typically include logic to register the subdomain using your backend system or API
    # For demonstration purposes, we simulate successful registration
    st.success(f"The subdomain {subdomain}.τao has been successfully registered!")

# Corcel API interaction for AI-generated text
st.header('Generate AI Text with Corcel')
corcel_api_key = st.text_input('Enter your Corcel API Key:', type='password')
if corcel_api_key:
    text_prompt = st.text_area('Enter text prompt:')
    if st.button('Generate Text'):
        url = "https://api.corcel.io/cortext/text"
        payload = {
            "model": "cortext-ultra",
            "stream": False,
            "miners_to_query": 1,
            "top_k_miners_to_query": 40,
            "ensure_responses": True,
            "prompt": text_prompt
        }
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "Authorization": corcel_api_key
        }

        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            response_data = response.json()
            try:
                message_content = response_data[0]['choices'][0]['delta']['content']
                st.text('AI-generated Text:')
                st.write(message_content)
            except (IndexError, KeyError, TypeError):
                st.error('Failed to extract message content from the response.')
        else:
            st.error(f"Error: Received status code {response.status_code}")

# Generate Images with Corcel AI
st.header('Generate Images with Corcel AI')
if corcel_api_key:
    user_image_prompt = st.text_input('Enter your prompt for AI image generation:')
    if user_image_prompt and st.button('Generate Image'):
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
