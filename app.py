import streamlit as st
import requests
import bittensor

st.title('HandshakeTAO Domain Manager with Bittensor and Corcel Integration')

st.title('HandshakeTAO AI Assistant')

st.header('Welcome to your personal AI assistant powered by Corcel and integrated with Bittensor')
st.write("""
         This AI assistant can help you with a variety of tasks. 
         It can generate text, create images based on your prompts, 
         provide the current $TAO price, and fetch Bittensor network status. 
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
    # AI-powered text generation with Corcel
    st.header('AI-powered Text Generation')
    text_prompt = st.text_area('What would you like to write about?')
    if text_prompt and st.button('Generate Text'):
        text_url = "https://api.corcel.io/cortext/text"
        text_payload = {
            "model": "cortext-ultra",
            "prompt": text_prompt,
            "stream": False,
            "miners_to_query": 1,
            "top_k_miners_to_query": 40,
            "ensure_responses": True
        }
        text_headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "Authorization": corcel_api_key
        }

        text_response = requests.post(text_url, json=text_payload, headers=text_headers)
        if text_response.status_code == 200:
            text_data = text_response.json()
            try:
                message_content = text_data[0]['choices'][0]['delta']['content']
                st.write('AI-generated Text:')
                st.write(message_content)
            except (IndexError, KeyError, TypeError):
                st.error('Failed to extract message content from the text generation response.')
        else:
            st.error(f"Error during text generation: Received status code {text_response.status_code}")

    # AI-powered image generation with Corcel
    st.header('AI-powered Image Generation')
    image_prompt = st.text_input('What image would you like to create?')
    if image_prompt and st.button('Generate Image'):
        image_url = "https://api.corcel.io/v1/image"
        image_payload = {
            "prompt": image_prompt,
            "apiKey": corcel_api_key
        }

        image_response = requests.post(image_url, json=image_payload)
        if image_response.status_code == 200:
            image_data = image_response.json()
            if 'imageUrl' in image_data and image_data['imageUrl']:
                st.image(image_data['imageUrl'])
            else:
                st.write("Image generation succeeded but no image URL returned.")
        else:
            st.error(f"Error during image generation: Received status code {image_response.status_code}")
else:
    st.warning('Please enter your Corcel API key to activate the AI assistant features.')
