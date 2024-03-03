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
        st.write(f"The current price of $TAO: ${tao_price} USD")
    else:
        st.error("Failed to fetch the current $TAO price.")
except Exception as e:
    st.error(f"An error occurred: {str(e)}")

# Bittensor network status section
st.header('Bittensor Network Status')
if st.button('Fetch Bittensor Status'):
    # Assuming the Bittensor wallet is already set up and synched
    try:
        neuron = bittensor.neuron.Neuron()
        neuron_status = neuron.metagraph.sync()
        st.write("Bittensor Metagraph synced successfully.")
        st.write(neuron_status)
    except Exception as e:
        st.error(f"Failed to fetch Bittensor status: {str(e)}")

# Corcel API interaction for AI-generated text
st.header('Ask Corcel AI Anything')
       text_prompt = st.text_area('Enter your query or statement:')
if corcel_api_key and text_prompt:  # Corrected the condition to check 'text_prompt' directly
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
    st.warning('Please enter your Corcel API key and a query to get an answer.')

# Making the API call to Corcel for text generation
        text_response = requests.post(text_url, json=text_payload, headers=text_headers)
        if text_response.status_code == 200:
            try:
                text_data = text_response.json()
                message_content = text_data[0]['choices'][0]['delta']['content']
                st.text('AI-generated Text:')
                st.write(message_content)
            except (IndexError, KeyError, TypeError):
                st.error('Failed to extract message content from the text generation response.')
        else:
            st.error(f"Error during text generation: Received status code {text_response.status_code}")

    # Section for generating images with Corcel
    st.header('Generate Images with Corcel AI')
    image_prompt = st.text_input('Enter your prompt for AI image generation:')
    if image_prompt and st.button('Generate Image'):
        # Specify the Corcel AI Image endpoint and payload
        image_url = "https://api.corcel.io/v1/image"
        image_payload = {
            "prompt": image_prompt,
            "apiKey": corcel_api_key
        }

        # Making the API call to Corcel for image generation
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
    st.warning('Please enter your Corcel API key to use AI features.')
