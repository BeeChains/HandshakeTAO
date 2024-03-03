
import streamlit as st

st.title('Handshake τao Domain Manager')

st.header('Register Your τao Subdomain')
user_subdomain = st.text_input('Enter your desired subdomain (e.g., YourName)')

if user_subdomain:
    st.success(f"Subdomain '{user_subdomain}.τao' has been registered successfully!")
