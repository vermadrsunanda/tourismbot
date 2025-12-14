"""
Streamlit version of Tourism Bot for cloud deployment.
Run with: streamlit run streamlit_app.py
"""
import streamlit as st
import os
from dotenv import load_dotenv

# Load environment variables for local development
load_dotenv()

# Handle API key from Streamlit Secrets or environment
if "MISTRAL_API_KEY" in st.secrets:
    os.environ["MISTRAL_API_KEY"] = st.secrets["MISTRAL_API_KEY"]

from src.mistral_client import MistralTourismBot
from src.validators import validate_and_sanitize_input
from src.external_apis import WeatherAPI, FlightAPI, TourismDataAPI
from src.agent import TourismAgent

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
    except ValueError as e:
        if "MISTRAL_API_KEY" in str(e):
            st.error("""
            ❌ **API Key Missing!**
            
            To deploy this app, you need to add your Mistral API key to Streamlit Cloud secrets:
            
            1. Go to **App menu** (⋮) → **Settings** → **Secrets**
            2. Add this line:
               ```
               MISTRAL_API_KEY = "your-actual-mistral-api-key"
               ```
            3. Click **Save** and the app will redeploy automatically
            
            Get your free API key: https://console.mistral.ai/api-keys/
            """)
        else:
            st.error(f"Failed to initialize bot: {str(e)}")
        st.stop()
    except Exception as e:
        st.error(f"Failed to initialize bot: {str(e)}")
        st.stop()

if 'weather_api' not in st.session_state:
    st.session_state.weather_api = WeatherAPI()
if 'flight_api' not in st.session_state:
    st.session_state.flight_api = FlightAPI()
if 'agent' not in st.session_state:
    try:
        st.session_state.agent = TourismAgent()
    except Exception as e:
        st.error(f"Failed to initialize agent: {str(e)}")
        st.stop()
if 'agent_messages' not in st.session_state:
    st.session_state.agent_messages = []

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

# Create tabs for different views
tab1, tab2 = st.tabs(["💬 Chat Assistant", "🤖 AI Agent"])

with tab1:
    st.markdown("### Chat with our Tourism Assistant")
    
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

with tab2:
    st.markdown("### AI Agent - Autonomous Travel Planning")
    st.markdown("""
    The AI Agent independently uses multiple tools to answer your questions.
    It can fetch weather, search for flights, and provide travel recommendations.
    """)
    
    # Display agent conversation history
    for msg in st.session_state.agent_messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            if "tools" in msg:
                with st.expander(f"🔧 Tools Used ({len(msg['tools'])})"):
                    for tool in msg["tools"]:
                        st.json({
                            "tool": tool.get("tool"),
                            "status": "✅ Executed",
                            "params": tool.get("params")
                        })
    
    # Agent input
    agent_input = st.chat_input("Ask the agent anything about travel...", key="agent_input")
    
    if agent_input:
        sanitized_agent_input = validate_and_sanitize_input(agent_input)
        if not sanitized_agent_input:
            st.error("Invalid input. Please try again.")
        else:
            # Add user message
            st.session_state.agent_messages.append({
                "role": "user",
                "content": sanitized_agent_input
            })
            
            with st.chat_message("user"):
                st.markdown(sanitized_agent_input)
            
            # Process with agent
            with st.chat_message("assistant"):
                with st.spinner("Agent is thinking and using tools..."):
                    try:
                        result = st.session_state.agent.agentic_loop(sanitized_agent_input)
                        
                        agent_response = result.get("response", "Sorry, I couldn't process that.")
                        tools_used = result.get("tools_used", [])
                        iterations = result.get("iterations", 0)
                        
                        st.markdown(agent_response)
                        
                        # Store in history with tool info
                        st.session_state.agent_messages.append({
                            "role": "assistant",
                            "content": agent_response,
                            "tools": tools_used,
                            "iterations": iterations
                        })
                        
                        # Show agent execution details
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Iterations", iterations)
                        with col2:
                            st.metric("Tools Used", len(tools_used))
                        with col3:
                            st.metric("Status", "✅ Complete")
                        
                        # Show tool details if any
                        if tools_used:
                            st.divider()
                            st.markdown("### 🔧 Tool Execution Details")
                            for i, tool in enumerate(tools_used, 1):
                                with st.expander(f"Tool {i}: {tool.get('tool')}"):
                                    st.markdown(f"**Parameters:** {tool.get('params')}")
                                    st.json(tool.get('result', {}))
                    
                    except Exception as e:
                        st.error(f"Agent error: {str(e)}")
    
    # Agent controls
    st.divider()
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔄 Reset Conversation", key="agent_reset"):
            st.session_state.agent_messages = []
            st.session_state.agent.reset_conversation()
            st.success("Agent conversation reset!")
            st.rerun()
    
    with col2:
        st.info(f"📊 Messages in history: {len(st.session_state.agent_messages)}")

# Footer
st.divider()
st.markdown("""
    <div style='text-align: center; color: #888; font-size: 12px; padding: 20px;'>
    Made with ❤️ using Streamlit & Mistral AI | 
    <a href='https://github.com' target='_blank'>GitHub</a> | 
    <a href='https://streamlit.io' target='_blank'>Streamlit</a>
    </div>
    """, unsafe_allow_html=True)
