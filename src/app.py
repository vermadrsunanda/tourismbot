"""
Main Flask application for Tourism Bot.
"""
import os
from flask import Flask, render_template, request, jsonify, session
from functools import wraps
from config.settings import get_config
from src.logger import setup_logger
from src.mistral_client import MistralTourismBot
from src.validators import validate_and_sanitize_input
from src.external_apis import WeatherAPI, FlightAPI, TourismDataAPI

# Get the project root directory
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
template_folder = os.path.join(project_root, 'templates')

app = Flask(__name__, template_folder=template_folder)
app.config.from_object(get_config())

logger = setup_logger(__name__)


def init_app():
    """Initialize the Flask application."""
    try:
        logger.info("Initializing Tourism Bot application")
        
        # Initialize Mistral client
        try:
            app.mistral_bot = MistralTourismBot()
        except ValueError as e:
            logger.error(f"Failed to initialize Mistral bot: {str(e)}")
            raise
        
        # Initialize external APIs
        app.weather_api = WeatherAPI()
        app.flight_api = FlightAPI()
        
        return app
    except Exception as e:
        logger.error(f"Application initialization failed: {str(e)}")
        raise


def require_json(f):
    """Decorator to ensure request contains JSON and has required fields."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not request.is_json:
            logger.warning("Request received without JSON content type")
            return jsonify({'error': 'Content-Type must be application/json'}), 400
        return f(*args, **kwargs)
    return decorated_function


@app.before_request
def before_request():
    """Set up session for requests."""
    session.permanent = True


@app.route('/', methods=['GET'])
def index():
    """Home page."""
    logger.info("Home page accessed")
    return render_template('index.html')


@app.route('/api/chat', methods=['POST'])
@require_json
def chat():
    """
    Handle tourism bot chat requests.
    
    Expected JSON payload:
    {
        "message": "user's tourism question"
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            logger.warning("Empty JSON payload received")
            return jsonify({'error': 'Invalid request'}), 400
        
        message = data.get('message', '').strip()
        
        # Validate and sanitize input
        sanitized_message = validate_and_sanitize_input(message)
        
        if not sanitized_message:
            logger.warning("Invalid message received")
            return jsonify({'error': 'Invalid message. Please try again.'}), 400
        
        logger.info(f"Processing user query: {sanitized_message[:50]}...")
        
        # Generate response from Mistral
        response = app.mistral_bot.generate_tourism_response(sanitized_message)
        
        return jsonify({
            'success': True,
            'response': response,
            'user_message': sanitized_message
        }), 200
        
    except Exception as e:
        logger.error(f"Error in chat endpoint: {str(e)}")
        return jsonify({'error': 'An error occurred while processing your request'}), 500


@app.route('/api/recommendations', methods=['POST'])
@require_json
def get_recommendations():
    """
    Get destination recommendations based on user preferences.
    
    Expected JSON payload:
    {
        "preferences": "user's travel preferences"
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'Invalid request'}), 400
        
        preferences = data.get('preferences', '').strip()
        
        # Validate and sanitize input
        sanitized_preferences = validate_and_sanitize_input(preferences)
        
        if not sanitized_preferences:
            return jsonify({'error': 'Invalid preferences. Please try again.'}), 400
        
        logger.info(f"Processing recommendation request: {sanitized_preferences[:50]}...")
        
        # Get recommendations
        recommendations = app.mistral_bot.get_destination_recommendations(sanitized_preferences)
        
        return jsonify({
            'success': True,
            'recommendations': recommendations,
            'user_preferences': sanitized_preferences
        }), 200
        
    except Exception as e:
        logger.error(f"Error in recommendations endpoint: {str(e)}")
        return jsonify({'error': 'An error occurred while processing your request'}), 500


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'service': 'Tourism Bot API'
    }), 200


@app.route('/api/weather', methods=['GET'])
def get_weather():
    """
    Get weather data for a destination.
    
    Query params:
    - destination: City name
    """
    try:
        destination = request.args.get('destination', '').strip()
        
        if not destination:
            return jsonify({'error': 'Destination parameter required'}), 400
        
        # Validate destination
        destination = validate_and_sanitize_input(destination, max_length=100)
        if not destination:
            return jsonify({'error': 'Invalid destination'}), 400
        
        logger.info(f"Fetching weather for: {destination}")
        weather_data = app.weather_api.get_weather(destination)
        
        if weather_data:
            return jsonify(weather_data), 200
        else:
            return jsonify({'error': 'Could not fetch weather data'}), 500
            
    except Exception as e:
        logger.error(f"Error in weather endpoint: {str(e)}")
        return jsonify({'error': 'An error occurred'}), 500


@app.route('/api/flights', methods=['GET'])
def search_flights():
    """
    Search for flights.
    
    Query params:
    - origin: Origin city
    - destination: Destination city
    """
    try:
        origin = request.args.get('origin', '').strip()
        destination = request.args.get('destination', '').strip()
        
        if not origin or not destination:
            return jsonify({'error': 'Origin and destination parameters required'}), 400
        
        # Validate inputs
        origin = validate_and_sanitize_input(origin, max_length=100)
        destination = validate_and_sanitize_input(destination, max_length=100)
        
        if not origin or not destination:
            return jsonify({'error': 'Invalid origin or destination'}), 400
        
        logger.info(f"Searching flights from {origin} to {destination}")
        flights_data = app.flight_api.search_flights(origin, destination)
        
        if flights_data:
            return jsonify(flights_data), 200
        else:
            return jsonify({'error': 'Could not fetch flight data'}), 500
            
    except Exception as e:
        logger.error(f"Error in flights endpoint: {str(e)}")
        return jsonify({'error': 'An error occurred'}), 500


@app.route('/api/attractions', methods=['GET'])
def get_attractions():
    """
    Get popular attractions for a city.
    
    Query params:
    - city: City name
    """
    try:
        city = request.args.get('city', '').strip()
        
        if not city:
            return jsonify({'error': 'City parameter required'}), 400
        
        city = validate_and_sanitize_input(city, max_length=100)
        if not city:
            return jsonify({'error': 'Invalid city'}), 400
        
        logger.info(f"Fetching attractions for: {city}")
        attractions_data = TourismDataAPI.get_popular_attractions(city)
        
        return jsonify(attractions_data), 200
            
    except Exception as e:
        logger.error(f"Error in attractions endpoint: {str(e)}")
        return jsonify({'error': 'An error occurred'}), 500


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    logger.warning(f"404 error: {request.path}")
    return jsonify({'error': 'Endpoint not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    logger.error(f"500 error: {str(error)}")
    return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    app = init_app()
    logger.info("Starting Tourism Bot Flask application")
    app.run(debug=app.config['DEBUG'], host='127.0.0.1', port=5000)
