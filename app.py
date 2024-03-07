import streamlit as st
import requests
import streamlit.components.v1 as components
import bittensor
import socket
import anthropic

hostname = socket.gethostname()
local_ip = socket.gethostbyname(hostname)

st.write(f"Streamlit is running on IP: {local_ip}")
st.title('Handshake τao/ AI Assistant')

st.header('Welcome to your personal AI assistant powered by Corcel and integrated with Bittensor')
st.write("""
         This AI assistant can help you with a variety of tasks.
         It can generate text, create images based on your prompts,
         provide the current $TAO price, $HNS price, fetch Bittensor network status,
         and help generate Bittensor subnet-related subdomains.
         Just enter your Corcel API key to get started.
         """)

           

# Fetch and display the current $TAO price
st.header('Current Bittensor and Handshake Price')
try:
    tao_price_response = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=bittensor&vs_currencies=usd')
    if tao_price_response.status_code == 200:
        tao_price_data = tao_price_response.json()
        tao_price = tao_price_data.get('bittensor', {}).get('usd', 'Price not available')
        
        # Ensure the dollar sign displays correctly by using string formatting
        st.write("The current Bittensor (TAO) price is: ${} USD".format(tao_price))
    else:
        st.error("Failed to fetch the current $TAO price.")
except Exception as e:
    st.error(f"An error occurred: {str(e)}")

# Function to fetch Handshake (HNS) price
def get_hns_price():
    url = "https://api.coingecko.com/api/v3/simple/price?ids=handshake&vs_currencies=usd"
         
    response = requests.get(url)
# User provides their API key for Corcel
# User inputs their Corcel Cortex API key
st.header('Enter your Corcel Cortex API Key')
corcel_api_key = st.text_input('API Key:', type='password')

if corcel_api_key:
    st.header('Ask the Cortex AI Anything')
    user_input = st.text_area('Enter your prompt:')

    if user_input and st.button('Submit'):
        url = "https://api.corcel.io/v1/text/cortext/chat"
        payload = {
            "model": "cortext-ultra",
            "stream": False,
            "prompt": user_input  # Assuming the API expects a 'prompt' field
        }
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "Authorization": f"Bearer {corcel_api_key}"
        }

        response = requests.post(url, json=payload, headers=headers)

        if response.status_code == 200:
            response_data = response.json()
            try:
                # Adjust the following line based on how the response data is structured
                ai_response = response_data.get('text', 'No response returned')
                st.write('Cortex AI says:', ai_response)
            except KeyError:
                st.error('Failed to extract the AI response.')
        elif response.status_code == 401:
            st.error('Authentication failed. Please check your API key.')
        else:
            # More detailed error message from API response
            st.error(f"Error: Received status code {response.status_code}. Details: {response.text}")
else:
    st.warning('Please enter your Corcel Cortex API key.')

# Define a function to fetch Handshake (HNS) price
def get_hns_price():
    url = "https://api.coingecko.com/api/v3/simple/price?ids=handshake&vs_currencies=usd"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        # Ensure 'return' is used within the function scope to return the price
        return data['handshake']['usd']
    else:
        # If something goes wrong, you can return None or raise an exception
        # Here we return None for simplicity
        return None

# User inputs their API key
st.header('Enter your Claude AI API Key')
claude_api_key = st.text_input('API Key:', type='password')

st.header("Let's Chat with Claude AI")
user_message = st.text_area("Your Message:")

if user_message and claude_api_key and st.button('Send'):
    try:
        # Initialize the Anthropic client with the API key
        client = anthropic.Anthropic(api_key=claude_api_key)
        
        # Create a message to Claude AI and capture the response
        message = client.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=1000,
            temperature=0.0,
            system="Respond only in Yoda-speak.",
            messages=[{"role": "user", "content": user_message}]
        )
        
        # Display the response from Claude AI
        st.write('Claude AI says:', message.content)

    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
else:
    if not claude_api_key:
        st.error('Please enter your Claude AI API key.')
             
# Add a section in your Streamlit frontend to fetch and display Bittensor network status
st.header('Bittensor Network Status')

if st.button('Fetch Bittensor Status'):
    # Replace 'backend_url' with the actual URL where your FastAPI backend is hosted
    backend_url = 'http://127.0.0.1:8000/network_status'
    try:
        response = requests.get(backend_url)
        if response.status_code == 200:
            network_status = response.json()
            st.write(network_status)
        else:
            st.error('Failed to fetch network status from the backend.')
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
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

# Adding a custom footer
footer = """
     <style>
     .footer {
         font-size: 44px;
         text-align: center;
     }
     </style>
     <div class="footer"> 
     InnerINetwork/
     </div>
     """
st.markdown(footer, unsafe_allow_html=True)
