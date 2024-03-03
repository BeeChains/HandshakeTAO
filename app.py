import streamlit as st
import requests
import bittensor
import streamlit.components.v1 as components
st.title('Handshake τao/ AI Assistant')

st.header('Welcome to your personal AI assistant powered by Corcel and integrated with Bittensor')
st.write("""
         This AI assistant can help you with a variety of tasks.
         It can generate text, create images based on your prompts,
         provide the current $TAO price, fetch Bittensor network status,
         and help generate Bittensor subnet-related subdomains.
         Just enter your Corcel API key to get started.
         """)

     # User inputs their Corcel API key
if corcel_api_key:
    st.header('Ask the AI Assistant')
    user_question = st.text_input('What would you like to ask?')

    if user_question and st.button('Submit'):
        # Assuming '/cortext/text' is the endpoint for text completions or similar queries
        corcel_url = "https://api.corcel.io/cortext/text"
        payload = {
            "model": "cortext-ultra",
            "prompt": user_question,
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

        response = requests.post(corcel_url, json=payload, headers=headers)

        if response.status_code == 200:
            response_data = response.json()
            try:
                # Assuming the response structure correctly reflects the following path
                ai_response = response_data[0]['choices'][0]['delta']['content']
                st.write('AI Assistant says:', ai_response)
            except (IndexError, KeyError, TypeError):
                st.error('Failed to extract the AI response.')
        else:
            st.error(f"Error: Received status code {response.status_code}")
else:
    st.warning('Please enter your Corcel API key to interact with the AI assistant.')

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
    user_name = st.text_input('Enter your desired subdomain name (YourName.τao/):')
    if user_name and st.button('Generate Subdomain'):
        generated_subdomain = f"{user_name}.τao/"
        st.write(f"Your Bittensor subnet-related subdomain: {generated_subdomain}")

else:
    st.warning('Please enter your Corcel API key to activate the AI assistant features.')

 # Embed Twitter hashtag button for #bittensor
st.markdown('#### Share on Twitter for Bittensor')
tweet_text_bittensor = 'Check out this awesome AI Assistant!'
tweet_hashtag_bittensor = 'bittensor'
tweet_url_bittensor = f"https://twitter.com/intent/tweet?text={tweet_text_bittensor}&hashtags={tweet_hashtag_bittensor}"
components.html(f'<a href="{tweet_url_bittensor}" target="_blank" class="twitter-hashtag-button" data-show-count="false">Tweet #{tweet_hashtag_bittensor}</a>', height=30)

# Embed Twitter hashtag button for #HNS
st.markdown('#### Share on Twitter for HNS')
tweet_text_hns = 'Exploring the Handshake domain with AI!'
tweet_hashtag_hns = 'HNS'
tweet_url_hns = f"https://twitter.com/intent/tweet?text={tweet_text_hns}&hashtags={tweet_hashtag_hns}"
components.html(f'<a href="{tweet_url_hns}" target="_blank" class="twitter-hashtag-button" data-show-count="false">Tweet #{tweet_hashtag_hns}</a>', height=30)

# Twitter follow button for @innerinetco
st.markdown('#### Follow @innerinetco on Twitter')
twitter_user = 'innerinetco'
components.html(f'<a href="https://twitter.com/{twitter_user}?ref_src=twsrc%5Etfw" target="_blank" class="twitter-follow-button" data-show-count="false">Follow @{twitter_user}</a>', height=30)


