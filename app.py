import streamlit as st
import requests
import bittensor

st.title('HandshakeTAO AI Assistant')

st.header('Welcome to your personal AI assistant powered by Corcel and integrated with Bittensor')
st.write("""
         This AI assistant can help you with a variety of tasks.
         It can generate text, create images based on your prompts,
         provide the current $TAO price, fetch Bittensor network status,
         and help generate Bittensor subnet-related subdomains.
         Just enter your Corcel API key to get started.
         """)

# User inputs their Corcel API key
corcel_api_key = st.text_input('Enter your Corcel API Key:', type='password')

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

# Bittensor network status section
st.header('Bittensor Network Status')
if st.button('Fetch Bittensor Status'):
    try:
        neuron = bittensor.neuron.Neuron()
        neuron_status = neuron.metagraph.sync()
        st.write("Bittensor Metagraph synced successfully.")
        st.write(f"Metagraph details: {neuron_status}")
    except Exception as e:
        st.error(f"Failed to fetch Bittensor status: {str(e)}")

if corcel_api_key:
    # AI-powered text and image generation with Corcel sections...

    # Bittensor subnet-related subdomain generation
    st.header('Generate Your Bittensor Subnet-related Subdomain')
    user_name = st.text_input('Enter your desired subdomain name (YourName):')
    if user_name and st.button('Generate Subdomain'):
        generated_subdomain = f"{user_name}.τao/"
        st.write(f"Your Bittensor subnet-related subdomain: {generated_subdomain}")

else:
    st.warning('Please enter your Corcel API key to activate the AI assistant features.')
