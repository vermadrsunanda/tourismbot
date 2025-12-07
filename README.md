# Tourism Bot - AI Travel Assistant

A secure, production-ready tourism chatbot powered by Mistral AI and Flask. This application helps users discover travel destinations, get tourism advice, and explore the world with AI-powered recommendations.

## Features

- **AI-Powered Chat**: Interact with Mistral AI for tourism-related queries
- **🤖 AI Agent**: Autonomous agent that uses multiple tools to answer complex questions
- **🎤 Voice Input/Output**: Speak queries and listen to AI responses
- **Real-time Weather Data**: Current weather conditions for destinations
- **✈️ Flight Search**: Search for flights between cities
- **🎯 Attractions Guide**: Get popular attractions for any destination
- **Destination Recommendations**: Get personalized travel suggestions
- **Secure Input Handling**: Comprehensive input validation and sanitization
- **Professional Logging**: Detailed application and error logging
- **RESTful API**: Well-designed API endpoints following REST principles
- **Modern UI**: Responsive, user-friendly web interface with Streamlit version
- **Error Handling**: Robust error handling and recovery
- **Cloud Ready**: Easy deployment to Streamlit Cloud or Vercel

## Project Structure

```
tourism_bot/
├── src/
│   ├── __init__.py
│   ├── app.py              # Main Flask application
│   ├── mistral_client.py   # Mistral AI client wrapper
│   ├── validators.py       # Input validation utilities
│   └── logger.py           # Logging configuration
├── config/
│   └── settings.py         # Application configuration
├── templates/
│   └── index.html          # Web interface
├── tests/
│   └── test_validators.py  # Unit tests
├── requirements.txt        # Python dependencies
├── .env.example            # Environment variables template
├── .gitignore              # Git ignore rules
└── README.md              # This file
```

## Prerequisites

- Python 3.8+
- pip (Python package manager)
- Mistral AI API key

## Installation

1. **Clone or navigate to the project directory**:
   ```bash
   cd "c:\Users\dell\Desktop\JLT VScode\VSCode tourism Bot"
   ```

2. **Create and activate virtual environment** (if not already done):
   ```bash
   # Windows PowerShell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**:
   ```bash
   # Copy the example file
   copy .env.example .env
   
   # Edit .env and add your Mistral API key
   # MISTRAL_API_KEY=your_mistral_api_key_here
   ```

## Configuration

Edit `.env` file with your settings:

```env
MISTRAL_API_KEY=tABUyL4iglC52BT0cwxALaK47blVGou9
FLASK_ENV=development
FLASK_DEBUG=False
SECRET_KEY=your_secret_key_here
LOG_LEVEL=INFO
```

## Running the Application

### Flask Web Version (Development)

1. **Ensure virtual environment is activated**
2. **Start the Flask development server**:
   ```bash
   python -m src.app
   ```
3. **Open your browser** and navigate to:
   ```
   http://127.0.0.1:5000
   ```

### Streamlit Version (Recommended for Cloud Deployment)

1. **Install Streamlit** (if not already installed):
   ```bash
   pip install streamlit
   ```
2. **Run Streamlit app**:
   ```bash
   streamlit run streamlit_app.py
   ```
3. **Access the app**:
   - Streamlit will open automatically in your browser
   - Usually at: `http://localhost:8501`

### Features You Can Try

- **Voice Input**: Click the 🎤 Voice button to speak queries
- **Real-time Weather**: Ask "What's the weather in Paris?"
- **Flight Search**: Ask "Show me flights to Tokyo"
- **Voice Response**: Listen to AI responses (audio output)
- **Attractions**: Get destination information automatically

## API Endpoints

### 1. Chat Endpoint
**POST** `/api/chat`

Send a tourism-related question to the bot.

**Request**:
```json
{
    "message": "Tell me about Paris"
}
```

**Response**:
```json
{
    "success": true,
    "response": "Paris is a wonderful destination...",
    "user_message": "Tell me about Paris"
}
```

### 2. Recommendations Endpoint
**POST** `/api/recommendations`

Get destination recommendations based on preferences.

**Request**:
```json
{
    "preferences": "I love beaches and tropical weather"
}
```

**Response**:
```json
{
    "success": true,
    "recommendations": "Based on your preferences...",
    "user_preferences": "I love beaches and tropical weather"
}
```

### 3. Health Check
**GET** `/api/health`

Check if the application is running.

**Response**:
```json
{
    "status": "healthy",
    "service": "Tourism Bot API"
}
```

### 4. Weather Data
**GET** `/api/weather?destination=Paris`

Get current weather for a destination.

**Response**:
```json
{
    "destination": "Paris",
    "temperature": 12,
    "description": "Partly Cloudy",
    "humidity": 65,
    "wind_speed": 5,
    "success": true
}
```

### 5. Flight Search
**GET** `/api/flights?origin=NYC&destination=Tokyo`

Search for flights between two cities.

**Response**:
```json
{
    "origin": "NYC",
    "destination": "Tokyo",
    "flights": [
        {
            "airline": "Emirates",
            "code": "EK",
            "departure": "NYC 10:00",
            "arrival": "Tokyo 18:00",
            "price": 250,
            "duration": "8h 30m"
        }
    ],
    "success": true
}
```

### 6. Attractions
**GET** `/api/attractions?city=Paris`

Get popular attractions for a city.

**Response**:
```json
{
    "city": "Paris",
    "attractions": [
        "Eiffel Tower",
        "Louvre Museum",
        "Notre-Dame Cathedral"
    ],
    "success": true
}
```

### 7. AI Agent - Submit Query
**POST** `/api/agent/query`

Submit a query to the AI agent. The agent autonomously decides which tools to use.

**Request**:
```json
{
    "query": "What's the weather like in Tokyo and what are the main attractions?"
}
```

**Response**:
```json
{
    "success": true,
    "response": "Tokyo is an amazing destination...",
    "tools_used": [
        {
            "tool": "weather",
            "params": {"city": "Tokyo"},
            "result": {"temperature": 15, "description": "Partly Cloudy"}
        },
        {
            "tool": "attractions",
            "params": {"city": "Tokyo"},
            "result": {"attractions": ["Senso-ji Temple", "Meiji Shrine", "Tokyo Skytree"]}
        }
    ],
    "iterations": 2
}
```

### 8. AI Agent - Status
**GET** `/api/agent/status`

Get the current status and capabilities of the AI agent.

**Response**:
```json
{
    "status": "active",
    "tools_available": ["weather", "flights", "attractions", "travel_tips", "chat"],
    "max_iterations": 5,
    "conversation_length": 3,
    "tools_count": 4
}
```

### 9. AI Agent - Conversation History
**GET** `/api/agent/history`

Get the agent's conversation history.

**Response**:
```json
{
    "success": true,
    "history": [
        {"role": "user", "content": "Tell me about Paris"},
        {"role": "assistant", "content": "Paris is..."}
    ],
    "length": 2
}
```

### 10. AI Agent - Reset
**POST** `/api/agent/reset`

Reset the agent's conversation history.

**Response**:
```json
{
    "success": true,
    "message": "Agent reset successfully"
}
```

## Running Tests

Execute unit tests:

```bash
python -m pytest tests/ -v
```

Or using unittest:

```bash
python -m unittest discover -s tests -p "test_*.py" -v
```

## Security Features

- **Input Validation**: All user inputs are validated and sanitized
- **Secure Session Handling**: HTTP-only cookies with secure flags
- **Error Handling**: Sensitive information is not exposed in error messages
- **Request Validation**: JSON content-type validation
- **Rate Limiting Ready**: Structure supports adding rate limiting middleware
- **Logging**: Comprehensive audit logging of all operations

## Best Practices Implemented

- **Separation of Concerns**: Modular code structure
- **Configuration Management**: Environment-based configuration
- **Logging**: Structured logging with rotation
- **Error Handling**: Comprehensive exception handling
- **Code Organization**: Clear folder structure and naming conventions
- **Documentation**: Inline comments and docstrings
- **Testing**: Unit test framework in place
- **API Design**: RESTful endpoint design
- **Security**: Input validation and sanitization

## Troubleshooting

### Mistral API Key Error
- Ensure `.env` file exists and contains valid `MISTRAL_API_KEY`
- Verify API key has necessary permissions

### Port Already in Use
- Change port in `app.py` or kill process using port 5000:
  ```bash
  netstat -ano | findstr :5000
  taskkill /PID <PID> /F
  ```

### Module Import Errors
- Ensure virtual environment is activated
- Run `pip install -r requirements.txt` again

## Deployment

Tourism Bot can be deployed to multiple cloud platforms for production use.

### Quick Deployment

#### Streamlit Cloud (Recommended - Easiest)
```bash
# 1. Push to GitHub
git push origin main

# 2. Go to https://share.streamlit.io
# 3. Click "New app" and select your repository
# 4. Set main file to `streamlit_app.py`
# 5. Add secrets: MISTRAL_API_KEY=your_key
# 6. Deploy!
```

#### Vercel (Best for Flask API)
```bash
# 1. npm install -g vercel
# 2. vercel --prod
# 3. Set environment variables in dashboard
# 4. Done!
```

#### Railway (Fast & Simple)
```bash
# 1. Connect GitHub repo to railway.app
# 2. Add environment variables
# 3. Auto-deploys on git push
```

For detailed deployment instructions, see [DEPLOYMENT.md](DEPLOYMENT.md)

### Environment Setup for Cloud

Create `.env` file locally (don't commit to Git):
```env
MISTRAL_API_KEY=your_api_key_here
OPENWEATHER_API_KEY=optional_weather_key
FLIGHT_API_KEY=optional_flight_key
FLASK_ENV=production
```

For cloud platforms, add secrets/environment variables through their dashboards.

## Contributing

This is a demonstration project. Feel free to extend it with:
- User authentication
- Database integration (MongoDB/PostgreSQL)
- Caching mechanisms (Redis)
- Advanced error recovery
- Multi-language support
- Analytics and metrics
- Additional travel APIs
- Hotel booking integration
- Restaurant recommendations
- Travel insurance integration

## Tech Stack

- **Backend**: Flask 3.0 + Python 3.8+
- **AI**: Mistral AI API
- **Frontend**: HTML5/CSS3/JavaScript with Web Speech API
- **Cloud**: Streamlit, Vercel, Railway
- **APIs**: OpenWeatherMap, Flight APIs
- **Deployment**: Docker, GitHub Actions (optional)

## Browser Compatibility

- **Chrome/Chromium**: Full support (including voice)
- **Firefox**: Full support (including voice)
- **Safari**: Full support (including voice)
- **Edge**: Full support (including voice)
- **Mobile**: Responsive design, voice on supported browsers

Voice features work best in:
- Chrome 80+
- Firefox 76+
- Safari 14.1+
- Edge 80+

## License

MIT License - See LICENSE file for details

## Support

For issues or questions, please refer to:
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Mistral AI Documentation](https://docs.mistral.ai/)
- [Python Documentation](https://docs.python.org/)

---

**Created**: December 2025
**Framework**: Flask 3.0.0
**AI Service**: Mistral AI
**Python Version**: 3.8+
