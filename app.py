import streamlit as st
import requests
import bittensor
import streamlit.components.v1 as components
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

if corcel_api_key:
    # User Query Input
    st.header("Ask Your AI Assistant")
    user_query = st.text_input("Type your question here:")

    if user_query:
        answer_button = st.button('Get Answer')
        if answer_button:
            # Assume you use the same Corcel endpoint for answering user queries
            query_url = "https://api.corcel.io/cortext/text"
            query_payload = {
                "model": "cortext-ultra",
                "prompt": user_query,
                "stream": False,
                "miners_to_query": 1,
                "top_k_miners_to_query": 40,
                "ensure_responses": True
            }
            query_headers = {
                "accept": "application/json",
                "content-type": "application/json",
                "Authorization": corcel_api_key
            }

            # Sending the user's question to Corcel's API
            query_response = requests.post(query_url, json=query_payload, headers=query_headers)

            if query_response.status_code == 200:
                query_data = query_response.json()
                try:
                    answer_content = query_data[0]['choices'][0]['delta']['content']
                    st.write('AI-generated Answer:')
                    st.write(answer_content)
                except (IndexError, KeyError, TypeError):
                    st.error('Failed to extract answer content from the response.')
            else:
                st.error(f"Error: Received status code {query_response.status_code}")
else:
    st.warning('Please enter your Corcel API key to activate the AI assistant features.')

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


