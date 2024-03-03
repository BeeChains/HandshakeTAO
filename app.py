import streamlit as st
import requests
import bittensor

st.title('HandshakeTAO Domain Manager with Bittensor and Corcel Integration')

# User inputs their Corcel API key
st.header('Enter your Corcel API Key')
corcel_api_key = st.text_input('Corcel API Key:', type='password')

# Fetch and display the current $TAO price
st.header('Current $TAO Price')
try:
    tao_price_response = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=bittensor&vs_currencies=usd')
    if tao_price_response.status_code == 200:
        tao_price_data = tao_price_response.json()
        tao_price = tao_price_data.get('bittensor', {}).get('usd', 'Price not available')
        st.write(f"The current price of $$TAO: ${tao_price} USD")
    else:
        st.error("Failed to fetch the current $TAO price.")
except Exception as e:
    st.error(f"An error occurred: {str(e)}")

# Bittensor network status section
st.header('Bittensor Network Status')
# Placeholder button to simulate fetching Bittensor status
if st.button('Fetch Bittensor Status'):
    # Simulate fetching network status
    # Actual implementation should query the Bittensor network
    st.write("Bittensor network is up and running. (This is a simulated status.)")

# User interaction section for Corcel AI
st.header('Ask Corcel AI Anything')
if corcel_api_key and user_input:
    text_prompt = st.text_area('Enter your query or statement:')
    if st.button('Get Answer'):
        url = "https://api.corcel.io/cortext/text"
        payload = {
            "model": "cortext-ultra",
            "prompt": text_prompt,
            "stream": False,
            "miners_to_query": 1,
            "top_k_miners_to_query": 40,
            "ensure_responses": True
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
                st.text('AI-generated Response:')
                st.write(message_content)
                st.write('Details:')
                st.write(f"Hotkey: {response_data[0]['hotkey']}")
                st.write(f"Coldkey: {response_data[0]['coldkey']}")
                st.write(f"UID: {response_data[0]['uid']}")
                st.write(f"Incentive: {response_data[0]['incentive']}")
            except (IndexError, KeyError, TypeError):
                st.error('Failed to extract message content and details from the response.')
        else:
            st.error(f"Error: Received status code {response.status_code}")
else:
    st.warning('Please enter your Corcel API key and query to get an answer.')
