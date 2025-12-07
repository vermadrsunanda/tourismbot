"""
Streamlit version of Tourism Bot for cloud deployment.
Run with: streamlit run streamlit_app.py
"""
import streamlit as st
import os
from dotenv import load_dotenv
from src.mistral_client import MistralTourismBot
from src.validators import validate_and_sanitize_input
from src.external_apis import WeatherAPI, FlightAPI, TourismDataAPI

# Load environment variables
load_dotenv()

# Configure Streamlit
st.set_page_config(
    page_title="Tourism Bot",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 0;
    }
    .stChatMessage {
        padding: 1rem;
        border-radius: 0.5rem;
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'bot' not in st.session_state:
    try:
        st.session_state.bot = MistralTourismBot()
    except Exception as e:
        st.error(f"Failed to initialize bot: {str(e)}")
        st.stop()

if 'weather_api' not in st.session_state:
    st.session_state.weather_api = WeatherAPI()
if 'flight_api' not in st.session_state:
    st.session_state.flight_api = FlightAPI()

# Sidebar
with st.sidebar:
    st.title("🌍 Tourism Bot Settings")
    
    st.markdown("### Features")
    show_weather = st.checkbox("Show Weather Data", value=True)
    show_flights = st.checkbox("Show Flight Offers", value=True)
    show_attractions = st.checkbox("Show Attractions", value=True)
    
    st.markdown("---")
    st.markdown("### About")
    st.info("""
    **Tourism Bot** is an AI-powered travel assistant powered by Mistral AI.
    
    - Ask about destinations
    - Get travel tips
    - Check real-time weather
    - Search for flights
    - Discover attractions
    """)

# Main page
st.title("🌍 Tourism Bot - Your AI Travel Assistant")
st.markdown("Powered by Mistral AI | Real-time Weather & Flight Data")

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if user_input := st.chat_input("Ask me about travel destinations, tips, or attractions..."):
    # Validate input
    sanitized_input = validate_and_sanitize_input(user_input)
    if not sanitized_input:
        st.error("Invalid input. Please try again.")
    else:
        # Add user message to chat
        st.session_state.messages.append({"role": "user", "content": sanitized_input})
        
        with st.chat_message("user"):
            st.markdown(sanitized_input)
        
        # Generate bot response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    response = st.session_state.bot.generate_tourism_response(sanitized_input)
                    st.markdown(response)
                    st.session_state.messages.append({"role": "assistant", "content": response})
                    
                    # Extract destination and fetch additional data
                    if any(word in sanitized_input.lower() for word in ['weather', 'flight', 'destination', 'travel to', 'visit']):
                        st.divider()
                        
                        # Try to extract destination
                        words = sanitized_input.split()
                        destination = None
                        
                        if 'to' in words:
                            idx = words.index('to')
                            if idx < len(words) - 1:
                                destination = ' '.join(words[idx+1:])
                        elif 'visit' in [w.lower() for w in words]:
                            idx = [i for i, w in enumerate(words) if w.lower() == 'visit']
                            if idx and idx[0] < len(words) - 1:
                                destination = ' '.join(words[idx[0]+1:])
                        
                        # Display additional information
                        col1, col2, col3 = st.columns(3)
                        
                        if destination and show_weather:
                            with col1:
                                st.subheader("🌤️ Weather")
                                weather = st.session_state.weather_api.get_weather(destination)
                                if weather:
                                    st.metric("Temperature", f"{weather['temperature']}°C")
                                    st.write(f"**Condition:** {weather['description']}")
                                    st.write(f"**Humidity:** {weather['humidity']}%")
                        
                        if destination and show_flights:
                            with col2:
                                st.subheader("✈️ Flights")
                                flights = st.session_state.flight_api.search_flights("NYC", destination)
                                if flights and flights.get('flights'):
                                    for flight in flights['flights'][:2]:
                                        st.write(f"**{flight['airline']}** - ${flight['price']}")
                        
                        if destination and show_attractions:
                            with col3:
                                st.subheader("🎯 Attractions")
                                attractions = TourismDataAPI.get_popular_attractions(destination)
                                if attractions.get('attractions'):
                                    for attraction in attractions['attractions'][:3]:
                                        st.write(f"• {attraction}")
                
                except Exception as e:
                    st.error(f"Error: {str(e)}")

# Footer
st.divider()
st.markdown("""
    <div style='text-align: center; color: #888; font-size: 12px; padding: 20px;'>
    Made with ❤️ using Streamlit & Mistral AI | 
    <a href='https://github.com' target='_blank'>GitHub</a> | 
    <a href='https://streamlit.io' target='_blank'>Streamlit</a>
    </div>
    """, unsafe_allow_html=True)
